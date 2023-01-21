import pytest
from src.db_transactions import DataBaseTransaction
from pathlib import Path

@pytest.fixture
def create_db_object():
    db_transact = DataBaseTransaction()
    return db_transact


def test_db_creation(create_db_object):
    file_obj = Path().cwd()
    expected_file = file_obj / "db_transaction.db"
    create_db_object.create_db()
    file_found = [
        db_file for db_file in file_obj.iterdir() if db_file == expected_file
    ]
    assert expected_file == file_found[0]




