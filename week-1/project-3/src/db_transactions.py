from pathlib import Path
from sqlite3 import connect as sql_connect


class DataBaseManager:
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
    db_bugdet = DataBaseManager()
    db_bugdet.create_db(db_name)
    db_conn = db_bugdet.db_connect(f"{db_name}.db")
    if not db_conn:
        ValueError("DB is not connected")
    db_cursor = db_conn.cursor()
    db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS budget_trans(
        id INT PRIMARY KEY, 
        timestamp DATETIME,
        amount DOUBLE,
        typeOfOperation INT2, 
        habits NVAR(40)
        );
        
    CREATE TABLE IF NOT EXISTS dataGoal(
        id INT PRIMARY KEY,
        timestamp DATETIME, 
        goal_amount DOUBLE
    
    );
    
    """)
    db_bugdet.db_close(db_conn, db_cursor)
    return "DB schemas have been created"
