"""General endpoints not associated with any service"""
from http import HTTPStatus

from fastapi import APIRouter

# from utils.logger import logger

#from settings import generate_settings
#from schedule import scheduler

router = APIRouter()


@router.get("/health", status_code=HTTPStatus.ACCEPTED)
async def get_health_endpoint():
    """
    Endpoint for health check
    Returns:
        dict: status:okay but could be anything
    """

    """Health Endpoint, should always return 200 OK"""
    return {"status": "ok"}
