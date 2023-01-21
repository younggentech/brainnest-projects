from pathlib import Path


class DataBaseTransaction:

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
