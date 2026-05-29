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

import pytest

from app.data.database import RefDB


@pytest.fixture(name="mock_db")
def manage_db_connection(
    mock_settings,
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

    db_class = RefDB(mock_settings)

    try:
        yield db_class
    finally:
        db_class.close()


def test_upsert_and_entry_success(mock_db):
    # region Docs
    """
    Insert new entry, read, updates said entry, reads again

    Notes: Everything is done in one function according to all pathways to avoid code duplication.

    Inputs:
        test (str): The tester integration fake id
        testing (str) : The tester integration updated fake id

    Expected result: (dict): A new and updated dict.
    """
    # endregion

    mock_entry_id = mock_db.upsert_entry("test", "tag", "tester", "test")

    # Tested insert, called directly
    result = mock_db.table.get(doc_id=mock_entry_id)

    assert result.doc_id == 1
    assert result["name"] == "test"
    assert result["type"] == "tag"
    assert result["integrations"] == {"tester": "test"}

    # Tested insert, called via class
    mock_result = mock_db.get_mapping("test", "tag")

    assert mock_result["id"] == 1
    assert mock_result["name"] == "test"
    assert mock_result["type"] == "tag"
    assert mock_result["integrations"] == {"tester": "test"}

    mock_db.upsert_entry("test", "tag", "tester", "testing")

    # Tested update, called directly as update performs in-class read
    result = mock_db.table.get(doc_id=mock_entry_id)

    assert result["integrations"]["tester"] == "testing"


def test_show_table(mock_db):
    # region Docs
    """
    Sanity check for table

    Notes: Any nuances or references.

    Inputs:
        fake entry (row): A fake entry to read all from

    Expected result: (dict): the fake entry as a dict
    """
    # endregion

    mock_db.upsert_entry("test", "tag", "tester", "test")

    table_result = mock_db.show_table()

    assert len(table_result) == 1
    assert table_result[0]["name"] == "test"
    assert table_result[0]["type"] == "tag"
    assert table_result[0]["integrations"] == {"tester": "test"}
