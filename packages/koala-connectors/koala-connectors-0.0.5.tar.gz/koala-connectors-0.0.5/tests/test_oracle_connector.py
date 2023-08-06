import unittest

from koala_connectors.connectors.oracle_connector import OracleConnector

username = "usr"
password = "psw"
host = "test_host"
port = 8000
sid = "test_sid"

test_connection_string = f"oracle://{username}:{password}@{host}:{port}/{sid}"


class TestOracleConnector(unittest.TestCase):

    def test_parse_connection_string(self):
        parsed_connection_string = OracleConnector._parse_connection_string(test_connection_string)
        self.assertEqual(username, parsed_connection_string["user"])
        self.assertEqual(password, parsed_connection_string["password"])
        self.assertEqual(host, parsed_connection_string["host"])
        self.assertEqual(port, parsed_connection_string["port"])
        self.assertEqual(sid, parsed_connection_string["service_name"])

    # TODO: Test _make_dsn
