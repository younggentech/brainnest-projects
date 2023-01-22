import pytest
from src.db_transactions import DataBaseCreator
from pathlib import Path


@pytest.fixture
def create_db_object():
    db_transact = DataBaseCreator()
    return db_transact


@pytest.fixture()
def create_db_file(create_db_object):
    create_db_object.create_db("tmp")
    return create_db_object


def test_db_creation(create_db_file):
    file_obj = Path().cwd()
    expected_file = file_obj / "tmp.db"
    file_found = [db_file for db_file in file_obj.iterdir() if db_file == expected_file]
    assert expected_file == file_found[0]


@pytest.mark.xfail(raises=FileNotFoundError)
def test_db_connect_none_file(create_db_file):
    conn = create_db_file.db_connect("tester.db")


def test_db_connection(create_db_file, capsys):
    conn = create_db_file.db_connect("tmp.db")
    cursor = conn.cursor()
    create_db_file.db_close(conn, cursor)
    captured_msg = capsys.readouterr()
    assert captured_msg.out == "All DB connection have been terminated\n"
