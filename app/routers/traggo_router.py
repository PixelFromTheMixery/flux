from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from ..models.traggo_models import TagUpsert
from ..services.traggo_service import TraggoService
from ..settings import get_settings
from ..utils.logger import logger

router = APIRouter()


async def get_traggo_service(request: Request):
    settings = get_settings()
    key = await request.app.state.db.get_key("traggo")

    return TraggoService(settings.config.integrations.traggo.url, key)


@router.get("/version", status_code=HTTPStatus.OK)
async def get_version(
    service: TraggoService = Depends(get_traggo_service),
) -> dict:
    logger.info("Traggo version endpoint called")

    return await service.connection_check()


@router.get("/tags", status_code=HTTPStatus.OK)
async def get_tags(
    service: TraggoService = Depends(get_traggo_service),
) -> dict:
    logger.info("Traggo tags endpoint called")

    return await service.get_tags()


@router.post("/tag", status_code=HTTPStatus.OK)
async def upsert_tag(
    tag: TagUpsert,
    service: TraggoService = Depends(get_traggo_service),
) -> dict:
    logger.info("Traggo version endpoint called")

    return await service.upsert_tag(tag)
