import cx_Oracle
from urllib import parse


class OracleConnector:

    def __init__(self, connection_string):
        pcs = self._parse_connection_string(connection_string)
        dsn = self._make_dsn(pcs)
        self._connection, self._cursor = self._establish_db_connection(pcs, dsn)

    def _execute(self, sql, binds=None):
        if binds is None:
            binds = []

        self._cursor.execute(self._get_sql_query(sql), binds)
        response = self._cursor.fetchall()
        return response

    def select_clob(self, sql, binds=None):

        response = self._execute(sql, binds)

        return response[0][0].read()

    def to_records(self, sql, binds=None):
        response = self._execute(sql, binds)
        column_names = [value[0].lower() for value in self._cursor.description]

        response_list = []

        for row in response:
            response_list.append({column_names[i]: row[i] for i in range(len(column_names))})

        return response_list

    def _get_sql_query(self, sql):
        if ".sql" in sql:
            return self._read_sql(sql)
        else:
            return sql

    @staticmethod
    def _read_sql(sql):
        with open(sql, mode="r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def _parse_connection_string(connection_string):
        res = parse.urlparse(connection_string)
        return {
            'user': res.username,
            'password': res.password,
            'host': res.hostname,
            'port': res.port,
            'service_name': res.path[1:]
        }

    @staticmethod
    def _make_dsn(parsed_connection_string):
        dsn = cx_Oracle.makedsn(host=parsed_connection_string['host'],
                                port=parsed_connection_string['port'],
                                service_name=parsed_connection_string['service_name'])
        return dsn

    @staticmethod
    def _establish_db_connection(parsed_connection_string, dsn):
        connection = cx_Oracle.connect(
            user=parsed_connection_string['user'],
            password=parsed_connection_string['password'],
            dsn=dsn,
            encoding='UTF-8'
        )
        return connection, connection.cursor()
