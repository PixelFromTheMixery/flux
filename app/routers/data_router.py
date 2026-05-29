# region Docs
"""
Data endpoints for database interactions via API

Variables:
    router (APIRouter): object that handles path mapping

Methods:
    get_health_endpoint: Used for docker and sanity checks
"""
# endregion

from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends

from ..data.database import RefDB
from ..models.data_models import NewDoc
from ..settings import generate_settings

router = APIRouter()


def database_ref():
    return RefDB(generate_settings())


@router.get("/all", status_code=HTTPStatus.OK)
async def get_database_data(db: Annotated[RefDB, Depends(database_ref)]) -> list:
    # region Docs
    """
    Endpoint for fetching database data
    Returns:
        dict: database contents
    """
    # endregion

    return db.show_table()


@router.post("/upsert")
async def upsert_entry(
    db: Annotated[RefDB, Depends(database_ref)], entry: NewDoc
) -> dict:
    new_entry_id = db.upsert_entry(**entry.model_dump())
    return db.get_mapping(doc_id=new_entry_id)
