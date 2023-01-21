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

        except (TypeError, FileNotFoundError) as e:
            print(f"DB to path has not been passed correctly:\n\n {e}")
        else:
            conn = sql_connect(db_path)
            return conn

    def db_close(self, connector, cursor):
        try:
            cursor.close()
            connector.close()

        except AttributeError:
            print("Cursor and Connector are still open.")

        else:
            print("All DB connection have been terminated")
