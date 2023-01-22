import unittest
from src.db_transactions import DataBaseConnector, open_db


class DataBaseConnectorTest(unittest.TestCase):
    def test_open_the_database(self):
        """Checks if the connection is DataBaseConnector object"""
        with open_db() as con:
            self.assertIsInstance(con, DataBaseConnector)
