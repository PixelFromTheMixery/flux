from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from ..services.traggo_service import TraggoService
from ..settings import get_settings
from ..utils.logger import logger

router = APIRouter()


async def get_traggo_service(request: Request):
    settings = get_settings()
    traggo_key = await request.app.state.db.get_key("traggo")

    return TraggoService(settings.config.integrations.traggo.url, traggo_key)


@router.get("/version", status_code=HTTPStatus.OK)
async def get_traggo_version(
    service: TraggoService = Depends(get_traggo_service),
) -> dict:
    logger.info("Traggo version endpoint called")

    return service.connection_check()
