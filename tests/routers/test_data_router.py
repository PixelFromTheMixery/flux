# region Docs
"""
Module: /app/routers/general_routers.py

Tests:
    health_check

"""

from pymongo import AsyncMongoClient
import pytest


@pytest.fixture(autouse=True)
async def clear_database(mongo_conn):
    client = AsyncMongoClient(mongo_conn)

    await client.drop_database("flux_db")

    await client.close()


# endregion
@pytest.mark.asyncio
async def test_get_database_data_empty(app_client):
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
async def test_upsert_entry_and_read(app_client):
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

    assert result.status_code == 202

    assert {"_id", "name", "group", "integrations"} == set(result_json.keys())

    assert result_json["name"] == "test tag"
    assert result_json["group"] == "tag"
    assert result_json["integrations"]["traggo"] == "test"

    read_result = await app_client.get("data/tag/test tag")

    assert read_result.status_code == 200
    assert read_result.json() == result_json

    delete_result = await app_client.delete(f"/data/{result_json['_id']}")

    assert delete_result.status_code == 200
    assert delete_result.json() == result_json
