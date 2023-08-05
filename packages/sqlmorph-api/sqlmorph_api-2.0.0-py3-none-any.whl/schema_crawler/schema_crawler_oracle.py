#!/usr/bin/python
#
#    Copyright 2020, phData, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys
import re
from pathlib import Path

# cx_Oracle is a heavyweight package so we should not require it
CX_ORACLE_IMPORT_SUCCESS = True
try:
    import cx_Oracle
except Exception as e:
    sys.stderr.write("WARNING: Unable to import cx_Oracle: {}\n".format(e))
    CX_ORACLE_IMPORT_SUCCESS = False

# Represents a database connection url
class DbURL(object):
    def __init__(self, user, password, host, port, service):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service = service

    def __repr__(self):
        return "{}/XXXXXX@//{}:{}/{}".format(self.user, self.host, self.port, self.service)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# easy to access map, should replace with a real object where used
class Struct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    def __str__(self):
        return str(self.__dict__)

GET_ALL_TABLES_SQL = """
SELECT OWNER, TABLE_NAME, DBMS_METADATA.GET_DDL('TABLE', TABLE_NAME, OWNER)
FROM ALL_TABLES WHERE OWNER LIKE '{schema}' AND TABLE_NAME LIKE '{table}'
"""

GET_SECONDARY_INDEXES_SQL = """
SELECT DBMS_METADATA.GET_DEPENDENT_DDL('INDEX',TABLE_NAME, TABLE_OWNER) FROM (
    SELECT table_name, table_owner, INDEX_NAME FROM all_indexes
    WHERE table_owner = '{schema}' AND table_name = '{table}'
    AND index_name NOT IN (
        SELECT constraint_name FROM sys.all_constraints
        WHERE table_name = table_name AND constraint_type = 'P'
    ) AND ROWNUM = 1
)
"""

GET_PRIMARY_KEYS_SQL = """
SELECT DBMS_METADATA.GET_DDL('CONSTRAINT', CONSTRAINT_NAME, OWNER)
FROM ALL_CONSTRAINTS c WHERE CONSTRAINT_TYPE = 'P' AND INDEX_OWNER = '{schema}' AND TABLE_NAME = '{table}'
"""

GET_COMMENTS_SQL = """
SELECT DBMS_METADATA.GET_DEPENDENT_DDL('COMMENT', TABLE_NAME, OWNER)
FROM ALL_TABLES WHERE OWNER = '{schema}' AND TABLE_NAME = '{table}'
"""

# Responsible for crawling the oracle schema
class OracleSchemaCrawler(object):
    def __init__(self, host, port, service, user, password):
        self.dsn = cx_Oracle.makedsn(
            host,
            port,
            service_name=service
        )
        self.conn = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=self.dsn
        )
        self.c = self.conn.cursor()

    def close(self):
        self.conn.close()

    def __exec(self, sql):
        sys.stderr.write("EXECUTING: %s\n" % sql)
        self.c.execute(sql)
        rows = []
        try:
          for row in self.c:
              rows.append(row)
        except Exception as e:
          s = str(e)
          # Should be only
          # cx_Oracle.DatabaseError: ORA-31608: specified object of type COMMENT not found
          # but oracle codes are reliable
          if re.search("specified object of type [A-z]+ not found", s):
              sys.stderr.write("Ignoring %s\n" % (s))
              pass
          else:
              raise e
        return rows

    def __populate_dependent_ddl(self, table):
        # INDEXES
        for row in self.__exec(GET_SECONDARY_INDEXES_SQL.format(schema=table.schema, table=table.name)):
            table.post_ddl += _oracle_split_create_index(row[0].read())
        # PRIMARY KEYS
        for row in self.__exec(GET_PRIMARY_KEYS_SQL.format(schema=table.schema, table=table.name)):
            table.post_ddl += [row[0].read()]
        # COMMENTS
        for row in self.__exec(GET_COMMENTS_SQL.format(schema=table.schema, table=table.name)):
            table.post_ddl += _oracle_split_comments(row[0].read())


    def collect_ddl(self, schema_pattern, table_pattern, outputPath):
        tables = []
        results = []
        outputPath.mkdir(parents=True, exist_ok=True)
        for row in self.__exec(GET_ALL_TABLES_SQL.format(schema=schema_pattern, table=table_pattern)):
            tables.append(Struct(schema=row[0], name=row[1], object_type='TABLE', table_ddl=row[2].read(), pre_ddl=[], post_ddl=[]))
        for table in tables:
            self.__populate_dependent_ddl(table)
        for table in tables:
            outputFile = outputPath.joinpath("TABLE-AND-DEPENDENTS-{}-{}.sql".format(table.schema, table.name).upper())
            with outputFile.open('w') as fh:
                for ddl in table.pre_ddl:
                    fh.write(ddl)
                    fh.write(";\n")
                fh.write(table.table_ddl)
                fh.write(";\n")
                for ddl in table.post_ddl:
                    fh.write(ddl)
                    fh.write(";\n")
            results.append(outputFile)
        return results

# Parses Oracle's EZConnect syntax
def _oracle_parse_url(url):
    m = re.match("^([^/]+)/([^@]+)@(/{2})?([^:/]+)(:[^/]+)?/(.*)", url)
    if m and len(m.groups()) == 6:
        user = m.group(1)
        password = m.group(2)
        host = m.group(4)
        port = m.group(5)
        if not port: port = '1521'
        if port[0] == ':': port = port[1:]
        service = m.group(6)
        return DbURL(user, password, host, port, service)
    else:
        raise Exception("Invalid db url %s, expected format USER/PASSWORD@//hostname:port/service_name" % (url))

def _oracle_split_lob_by_regex(regex, sql):
    buff = []
    result = []
    for line in sql.split("\n"):
        if not line: continue
        if not buff:
            buff.append(line)
        elif re.search(regex, line, re.IGNORECASE):
            result.append("\n".join(buff))
            buff = []
            buff.append(line)
        else:
            buff.append(line)
    result.append("\n".join(buff))
    return result

# Parse oracle's strange create index syntax. See tests for example
def _oracle_split_create_index(sql):
    return _oracle_split_lob_by_regex("^\s*CREATE\s+(UNIQUE\s+)?INDEX", sql)

# Parse oracle's strange comment syntax. See tests for example
def _oracle_split_comments(sql):
    return _oracle_split_lob_by_regex("^\s*COMMENT\s+ON", sql)

def oracle_collect_sql(url, schema, table, outputPath):
    url = _oracle_parse_url(url)
    sys.stderr.write("Connecting to: %s\n" % (url))
    sc = OracleSchemaCrawler(url.host, url.port, url.service, url.user, url.password)
    sc.collect_ddl(schema, table, outputPath)
    sc.close()

