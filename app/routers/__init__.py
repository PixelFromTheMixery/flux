# region Docs
"""
Central Hub for router pathing

Variables:
    router (APIRouter): Router object that performs path mapping
    settings (Settings): Turn routes on and off according to settings

TODO: Add routes lol
"""

from fastapi import APIRouter

from . import (
    data_router,
    general_router,
    traggo_router,
    # anytype_router
)
# endregion

router = APIRouter()

router.include_router(general_router.router, prefix="/general", tags=["general"])

router.include_router(data_router.router, prefix="/data", tags=["data"])

router.include_router(traggo_router.router, prefix="/traggo", tags=["traggo"])

# router.include_router(anytype_router.router, prefix="/anytype", tags=["anytype"])
