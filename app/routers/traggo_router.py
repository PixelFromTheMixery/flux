from http import HTTPStatus

from fastapi import APIRouter, Depends

from ..services.traggo_service import TraggoService

router = APIRouter()


def get_traggo_service():
    return TraggoService()


@router.get("/version", status_code=HTTPStatus.OK)
async def get_traggo_version(
    service: TraggoService = Depends(get_traggo_service),
) -> dict:
    return service.connection_check()
