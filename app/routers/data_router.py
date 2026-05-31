# region Docs
"""
Data endpoints for database interactions via API

Variables:
    router (APIRouter): object that handles path mapping

Methods:
    get_health_endpoint: Used for docker and sanity checks
"""
# endregion

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from ..data.database import RefDB
from ..models.data_models import UpsertRequest
from ..utils.helper import transformer

router = APIRouter()


async def database_ref(request: Request):
    return request.app.state.db


@router.get("/all", status_code=HTTPStatus.OK)
async def get_database_data(db: RefDB = Depends(database_ref)):
    # region Docs
    """
    Endpoint for fetching database data
    Returns:
        dict: database contents
    """
    # endregion

    return await db.show_table()


@router.post("/upsert", status_code=HTTPStatus.ACCEPTED)
async def upsert_entry(
    db: Annotated[RefDB, Depends(database_ref)], upsert: UpsertRequest
) -> dict:
    result = await db.upsert_entry(upsert)
    return transformer(result)


@router.get("/{group}/{name}", status_code=HTTPStatus.OK)
async def get_entry(
    db: Annotated[RefDB, Depends(database_ref)], group: str, name: str
) -> dict:
    return await db.get_entry(group, name)


@router.delete("/{doc_id}", status_code=HTTPStatus.OK)
async def delete_entry(
    db: Annotated[RefDB, Depends(database_ref)], doc_id: str
) -> dict:
    return await db.delete_entry(doc_id)
