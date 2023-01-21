from pathlib import Path


class DataBaseTransaction:

    def create_db(self, db_name: str = None):
        if not db_name:
            db_name = "db_transaction.db"
        db_path = Path().cwd() / db_name
        try:
            if not db_path.exists():
                raise FileNotFoundError

        except FileNotFoundError as e:
            print(e)
            print(f"DB was created at:{str(db_path)}")
            db_path.touch()
        else:
            print("DB already exists")
