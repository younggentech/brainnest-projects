import logging
import os.path
from pathlib import Path
from sqlite3 import connect as sqlite_connect
from sqlite3 import Error
from typing import Union
from contextlib import contextmanager

DATA_BASE_NAME = "budget_db.db"


class DataBaseConnector:
    def __init__(self, name=DATA_BASE_NAME):
        """Method for initialization of db"""
        self.db_name = name

    def __establish_connection(
        self, query: str, params: tuple
    ) -> Union[list[tuple], int]:
        """Service method for query execution"""
        try:  # trying to connect to database
            sqlite_connection = sqlite_connect(self.db_name)
            cursor = sqlite_connection.cursor()
        except Exception as e:
            logging.error(f"establish connection error: {e}", exc_info=True)
            return 1

        try:  # trying to execute a query
            logging.info(f"successful connection; QUERY: {query}; Params: {params}")
            cursor.execute(query, params)
            record = cursor.fetchall()
            sqlite_connection.commit()
            return record

        except Error as e:
            logging.error(f"query execution error: {e}", exc_info=True)
            return 1

        finally:
            cursor.close()

    def insert_transaction(
        self, _timestamp: float, _amount: float, type_of_operation: int, habits: str
    ) -> list:
        """Inserts new transaction into budget_trans table"""
        logging.info(
            f"adding a transaction with values: {_timestamp} {_amount} {type_of_operation} {habits}"
        )
        query = (
            f"INSERT INTO budget_trans (timestamp, amount, typeOfOperation, habits) "
            f"VALUES (?, ?, ?, ?)"
        )
        return self.__establish_connection(
            query, (_timestamp, _amount, type_of_operation, habits)
        )

    def insert_goal(self, timestamp: float, goal_amount: float) -> list:
        """Inserts new goal into dataGoal table"""
        logging.info(f"adding a goal with values {timestamp} {goal_amount}")
        query = f"INSERT INTO dataGoal (timestamp, goalAmount) VALUES (?, ?)"
        return self.__establish_connection(query, (timestamp, goal_amount))

    def get_all_transactions(self) -> list:
        """get all transactions
        Select * from budget_trans
        """
        logging.info(f"get_all_transactions")
        query = f"SELECT * FROM budget_trans"
        return self.__establish_connection(query, ())

    def get_current_goal(self) -> list:
        """get the latest goal from db
        Select * with max timestamp
        """
        logging.info(f"get_current_goal")
        query = f"SELECT * FROM dataGoal WHERE timestamp=(SELECT MAX(timestamp) from dataGoal)"
        return self.__establish_connection(query, ())

    def get_spending_transactions(self) -> list:
        """get all the outcome/spending transactions
        Select * from budget_trans where typeOfOperation=1
        """
        logging.info(f"get_spending_transactions")
        query = f"SELECT * FROM budget_trans WHERE typeOfOperation=1"
        return self.__establish_connection(query, ())

    def get_income_transactions(self) -> list:
        """get all the income transactions
        Select * from budget_trans where typeOfOperation=0
        """
        logging.info(f"get_income_transactions")
        query = f"SELECT * FROM budget_trans WHERE typeOfOperation=0"
        return self.__establish_connection(query, ())

    def get_total_spendings(self):
        """
        Get total spendings/outcome
        Selects sum(amount) from budget_trans where typeOfOperation=1
        """
        logging.info(f"get_total_spendings")
        query = f"SELECT SUM(amount) FROM budget_trans WHERE typeOfOperation=1"
        return self.__establish_connection(query, ())

    def get_total_income(self):
        """
        Get total income
        Selects sum(amount) from budget_trans where typeOfOperation=0
        """
        logging.info(f"get_total_income")
        query = f"SELECT SUM(amount) FROM budget_trans WHERE typeOfOperation=0"
        return self.__establish_connection(query, ())


@contextmanager
def open_db(db_name=DATA_BASE_NAME) -> DataBaseConnector:
    if not os.path.exists(db_name):
        db_create_schema(db_name)

    connector = DataBaseConnector(db_name)
    try:
        yield connector
    finally:
        del connector


class DataBaseCreator:
    @classmethod
    def create_db(cls, db_name: str = None):
        if not db_name:
            db_name = DATA_BASE_NAME
        db_path = Path().cwd() / f"{db_name}"
        try:
            if not db_path.exists():
                raise FileNotFoundError

        except FileNotFoundError as e:
            print(e)
            print(f"DB was created at:{str(db_path)}")
            db_path.touch()
        else:
            print("DB already exists")

    @classmethod
    def connect_to_db(cls, path_to_db: str):
        db_path = Path() / path_to_db
        try:
            if not db_path.exists():
                raise FileNotFoundError
            conn = sqlite_connect(db_path)

        except (TypeError, FileNotFoundError) as e:
            print(f"DB to path has not been passed correctly")
        else:
            return conn

    @classmethod
    def close_connection(cls, connector, cursor):
        try:
            cursor.close()
            connector.close()

        except AttributeError:
            print("Cursor and Connector are still open.")

        else:
            print("All DB connection have been terminated")


def db_create_schema(db_name):
    DataBaseCreator().create_db(db_name)
    connector_to_db = DataBaseCreator().connect_to_db(f"{db_name}")
    if not connector_to_db:
        ValueError("DB is not connected")
    cursor = connector_to_db.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS budget_trans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DOUBLE,
            amount DOUBLE,
            typeOfOperation INT2,
            habits NVAR(40)
        );

        CREATE TABLE IF NOT EXISTS dataGoal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DOUBLE,
            goalAmount DOUBLE
        );
        """
    )
    DataBaseCreator().close_connection(connector_to_db, cursor)
    return "DB schemas have been created"
