import logging
from pathlib import Path
from sqlite3 import connect as sql_connect
from sqlite3 import Error
from typing import Union


class DataBaseManager:
    pass


class DataBaseConnector:
    def __init__(self, name="budget_db.db"):
        """Method for inizialization of db"""
        self.db_name = name

    def __establish_connection(self, query: str, params: tuple) -> Union[tuple, int]:
        """Service method for query execution"""
        try:  # trying to connect to database
            sqlite_connection = sql_connect(self.db_name)
            cursor = sqlite_connection.cursor()
        except Exception as e:
            logging.error(f"establish connection error: {e}", exc_info=True)
            return 1

        try:  # trying to execute a query
            logging.info("successful connection; QUERY: {query}; Params: {params}")
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
            f"adding a trx {_timestamp} {_amount} {type_of_operation} {habits}"
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
        logging.info(f"adding a trx {timestamp} {goal_amount}")
        query = f"INSERT INTO dataGoal (timestamp, goalAmount) " f"VALUES (?, ?)"
        return self.__establish_connection(query, (timestamp, goal_amount))

    def get_all_trx(self) -> list:
        """Select * from budget_trans"""
        logging.info(f"get_all_trx")
        query = f"SELECT * FROM budget_trans"
        return self.__establish_connection(query, ())

    def get_current_goal(self) -> list:
        """Select * with max timestamp"""
        logging.info(f"get_current_goal")
        query = f"SELECT * FROM dataGoal WHERE timestamp=MAX(SELECT timestamp from dataGoal)"
        return self.__establish_connection(query, ())

    def get_spending_trx(self) -> list:
        """Select * from budget_trans where typeOfOperation=1"""
        logging.info(f"get_spending_trx")
        query = f"SELECT * FROM budget_trans WHERE typeOfOperation=1"
        return self.__establish_connection(query, ())

    def get_income_trx(self) -> list:
        """Select * from budget_trans where typeOfOperation=0"""
        logging.info(f"get_income_trx")
        query = f"SELECT * FROM budget_trans WHERE typeOfOperation=0"
        return self.__establish_connection(query, ())


class DataBaseCreator:
    def create_db(self, db_name: str = None):
        if not db_name:
            db_name = "db_transaction"
        db_path = Path().cwd() / f"{db_name}.db"
        try:
            if not db_path.exists():
                raise FileNotFoundError

        except FileNotFoundError as e:
            print(e)
            print(f"DB was created at:{str(db_path)}")
            db_path.touch()
        else:
            print("DB already exists")

    def db_connect(self, path_to_db: str):
        db_path = Path() / path_to_db
        try:
            if not db_path.exists():
                raise FileNotFoundError
            conn = sql_connect(db_path)

        except (TypeError, FileNotFoundError) as e:
            print(f"DB to path has not been passed correctly")
        else:
            return conn

    def db_close(self, connector, cursor):
        try:
            cursor.close()
            connector.close()

        except AttributeError:
            print("Cursor and Connector are still open.")

        else:
            print("All DB connection have been terminated")


def db_create_schema():
    db_name = "budget_db"
    db_bugdet = DataBaseCreator()
    db_bugdet.create_db(db_name)
    db_conn = db_bugdet.db_connect(f"{db_name}.db")
    if not db_conn:
        ValueError("DB is not connected")
    db_cursor = db_conn.cursor()
    db_cursor.executescript(
        """
    CREATE TABLE IF NOT EXISTS budget_trans(
        id INT PRIMARY KEY,
        timestamp DOUBLE,
        amount DOUBLE,
        typeOfOperation INT2,
        habits NVAR(40)
        );

    CREATE TABLE IF NOT EXISTS dataGoal(
        id INT PRIMARY KEY,
        timestamp DOUBLE,
        goalAmount DOUBLE
    );

    """
    )
    db_bugdet.db_close(db_conn, db_cursor)
    return "DB schemas have been created"
