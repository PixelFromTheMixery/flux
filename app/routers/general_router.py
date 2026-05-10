"""
General endpoints not associated with any service

Health endpoint and detached endpoint, sometimes used for setup

Variables:
    router (APIRouter): object that handles path mapping

Methods:
    get_health_endpoint: Used for docker and sanity checks
"""

from http import HTTPStatus

from fastapi import APIRouter

# from utils.logger import logger

# from settings import generate_settings
# from schedule import scheduler

router = APIRouter()


@router.get("/health", status_code=HTTPStatus.ACCEPTED)
async def get_health_endpoint():
    """
    Endpoint for health check
    Returns:
        dict: status:okay but could be anything
    """

    return {"status": "ok"}
