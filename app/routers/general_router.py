# region Docs
"""
General endpoints not associated with any service

Health endpoint and detached endpoint, sometimes used for setup

Variables:
    router (APIRouter): object that handles path mapping

Methods:
    get_health_endpoint: Used for docker and sanity checks
"""
# endregion

from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=HTTPStatus.OK)
async def get_health_endpoint() -> dict:
    # region Docs
    """
    Endpoint for health check
    Returns:
        dict: status:okay but could be anything
    """
    # endregion

    return {"status": "ok"}
