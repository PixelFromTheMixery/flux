# region Docs
"""
Module: /app/routers/general_routers.py

Tests:
    health_check

"""

import pytest

from app.data.database import RefDB


@pytest.fixture(name="_mock_db")
async def make_connection(mock_settings):
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
        mock_settings.secrets.mongodb_uri, mock_settings.secrets.field_encryption_key
    )

    yield db_instance

    await db_instance.close()
    RefDB.instance = None


# endregion
@pytest.mark.asyncio
async def test_get_database_data_empty(app_client, _mock_db):
    # region Docs
    """
    Gets database content

    Notes: will be empty as is cleared every run

    Expected result: (Response): (200, [])
    """
    # endregion

    result = await app_client.get("/data/all")

    assert result.status_code == 200
    assert result.json() == []


@pytest.mark.asyncio
async def test_upsert_entry_and_read(app_client, _mock_db):
    # region Docs
    """
    Upsert check

    Expected result: (Response): (202, Object according to Map)
    """
    # endregion

    dict_payload = {
        "incoming": {
            "name": "test tag",
            "group": "tag",
            "int_name": "traggo",
            "int_id": "test",
        }
    }

    result = await app_client.post("/data/upsert", json=dict_payload)

    result_json = result.json()

    print(result_json.keys())

    assert result.status_code == 202

    assert {"id", "name", "group", "integrations"} == set(result_json.keys())

    assert result_json["name"] == "test tag"
    assert result_json["group"] == "tag"
    assert result_json["integrations"]["traggo"] == "test"

    read_result = await app_client.get("data/tag/test tag")

    assert read_result.status_code == 200
    assert read_result.json() == result_json
