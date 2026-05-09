"""
Central Hub for router pathing

Variables:
    router (APIRouter): Router object that performs path mapping
    settings (Settings): Turn routes on and off according to settings

TODO: Add routes lol
"""

from fastapi import APIRouter

from . import (
    general_router, 
#    anytype_router
)


#from settings import generate_settings

#settings = generate_settings()
router = APIRouter()

router.include_router(general_router.router, prefix="/general", tags=["general"])

#router.include_router(anytype_router.router, prefix="/anytype", tags=["anytype"])
