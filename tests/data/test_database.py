# region Docs
"""
Module: ./app/data/database.py

Notes:  Any nuances worth mentioning

Tests:
    setup_create_tables_and_columns
    execute_sql_read_and_write
    db_sanity_check
"""
# endregion

import sqlite3

import pytest

from app.data.database import RefDB
from app.settings import generate_settings


@pytest.fixture(name="mock_db")
def manage_db_connection(
    monkeypatch,
    tmp_path,
):
    # region Docs
    """
    Sets up fake database in tmp dir to protect live data.

    Args:
        monkeypatch (pytest-tool): override db file path to use tmp_path
        tmp_path (pytest-tool): creates a temporary directory for files

    Returns:
        RefDB: the fake database, which is held, then closed for resource avoidance
    """
    # endregion

    settings = {
        "db_file": str(tmp_path / "test.db"),
    }

    monkeypatch.setattr(
        "app.data.database.generate_settings", lambda: generate_settings(settings)
    )
    db = RefDB()

    yield db

    db.close()


def test_setup_create_tables_and_columns(monkeypatch, mock_db):
    # region Docs
    """
    Tests if the intended columns are made in the table

    Notes:
    - Since this is done as a part of startup, including the fixture, only looking at columns
    - NOSONAR/pylint applied as the name of the variable IS a class, ans should follow such naming

    Inputs:
        mock_db(RefDB): fake database for interaction
        cols (list[str]): retrieved from row object

    Expected result: (list[str]): name and type should already be present, testing should be created
    """
    # endregion

    table_info = mock_db.execute_sql(
        f"PRAGMA table_info ({mock_db.table_name})", "Collecting table info", read=True
    )

    cols = [row[1] for row in table_info]

    assert "name" in cols
    assert "type" in cols
    assert "traggo" in cols


def test_execute_sql_write_and_read(mock_db):
    # region Docs
    """
    Tests insert, then reads insert

    Notes: Any nuances or references.

    Inputs:
        "query" (str): the output of part one becomes the input part two

    Expected result: (Row): row with project named test
    """
    # endregion

    mock_db.execute_sql(
        "INSERT INTO id_maps (name, type) VALUES (?,?)",
        "test insert of project test",
        ("test", "project"),
    )
    rows = mock_db.execute_sql(
        "SELECT * FROM id_maps WHERE name = ?", "read test row", ("test",), True
    )

    assert len(rows) == 1
    assert rows[0]["name"] == "test"
    assert rows[0]["type"] == "project"


def test_db_sanity_check(mock_db):
    # region Docs
    """
    Prompting a db exception

    Notes: Any nuances or references.

    Inputs:
        "Bad Query" (str): intentional bad SQL

    Expected result: (OperationalError): Obviously
    """
    # endregion

    with pytest.raises(sqlite3.OperationalError) as exc_info:
        mock_db.execute_sql("Bad query", "Bad query")

    assert exc_info.type == sqlite3.OperationalError
