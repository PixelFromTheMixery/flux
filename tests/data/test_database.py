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
from app.models.data_models import (
    NewDoc,
    NewKey,
    UpsertRequest,
)


@pytest.fixture(name="mock_db")
async def make_connection(mongo_settings):
    # region Docs
    """
    Sets up fake database in tmp dir to protect live data.
    Table dropped at the start of every run

    Returns:
        RefDB: the fake database, which is held, then closed for resource avoidance
    """
    # endregion

    RefDB.instance = None
    db_instance = await RefDB.db_singleton(
        mongo_settings.secrets.mongodb_uri, mongo_settings.secrets.field_encryption_key
    )

    yield db_instance

    await db_instance.close()
    RefDB.instance = None


@pytest.mark.asyncio
async def test_close_connection(mock_db):
    # region Docs
    """
    Just to check database connection and setup

    Notes: close is a nonfunction used for lifespan mgmt

    Expected result: No Exceptions
    """
    # endregion

    await mock_db.close()


@pytest.mark.asyncio
async def test_upsert_entry_success(mock_db, mock_settings):
    # region Docs
    """
    Insert new entry and then updates said entry

    Notes: Everything is done in one function according to all doc pathways to avoid code duplication.

    Inputs:
        new_doc (NewDoc): a brand new mapping entry
        updated_doc (NewDoc): an update to the new_doc

    Expected result: (obj): A new and updated Mapping Object
    """
    # endregion

    new_doc = NewDoc(name="test tag", group="tag", int_name="traggo", int_id="test")

    mock_entry_result = await mock_db.upsert_entry(UpsertRequest(incoming=new_doc))

    assert mock_entry_result.name == "test tag"
    assert mock_entry_result.group == "tag"
    assert mock_entry_result.integrations.traggo == "test"
    assert mock_entry_result.integrations.anytype is None

    updated_doc = NewDoc(
        name="test tag", group="tag", int_name="traggo", int_id="updated"
    )

    mock_entry_update = await mock_db.upsert_entry(UpsertRequest(incoming=updated_doc))

    # Ensure that we are altering the same 'document'
    assert mock_entry_update.id == mock_entry_result.id
    assert mock_entry_update.integrations.traggo == "updated"


@pytest.mark.asyncio
async def test_upsert_key_success(mock_db, mock_settings):
    # region Docs
    """
    Insert new encrypted key and then updates said key

    Notes: Everything is done in one function according to all key pathways to avoid code duplication.

    Inputs:
        new_doc (NewKey): a brand new key entry
        updated_doc (NewKey): an update to the new_key

    Expected result: (obj): A new and updated Mapping Object
    """
    # endregion

    new_key = NewKey(service="traggo", key="fake_key")

    mock_key_result = await mock_db.upsert_entry(UpsertRequest(incoming=new_key))

    assert mock_key_result.service == "traggo"
    assert isinstance(mock_key_result.encrypted_api_key, bytes)

    decrypted_key = await mock_db.get_key("traggo")

    assert decrypted_key == "fake_key"

    updated_key = NewKey(service="traggo", key="new_fake_key")

    mock_key_update = await mock_db.upsert_entry(UpsertRequest(incoming=updated_key))
    decrypted_key = await mock_db.get_key("traggo")

    # Ensure that we are altering the same 'document'
    assert mock_key_update.id == mock_key_result.id
    assert decrypted_key == "new_fake_key"


@pytest.mark.asyncio
async def test_show_table(mock_db):
    # region Docs
    """
    Sanity check for table

    Notes: Any nuances or references.

    Inputs:
        fake entry (row): A fake entry to read all from

    Expected result: (dict): the fake entry as a dict
    """
    # endregion

    new_doc = NewDoc(name="test tag", group="tag", int_name="traggo", int_id="test")

    await mock_db.upsert_entry(UpsertRequest(incoming=new_doc))

    table_result = await mock_db.show_table()

    assert len(table_result) == 1
    assert table_result[0]["name"] == "test tag"
    assert table_result[0]["group"] == "tag"
    assert table_result[0]["integrations"]["traggo"] == "test"
