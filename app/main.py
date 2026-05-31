# region Docs
"""
Main entry point for AnyTYpe Automation API

Base FastAPI application with scheduled tasks, exception middleware.

Variables:
    app (FastAPI): Server which runs the API

Methods:
    create_app: Build-time Configuration

TODO: Move exception middleware here?
"""
# endregion

from http import HTTPStatus

from fastapi import FastAPI

# from .middlewares.exception_middleware import ExceptionMiddleware
from .settings import generate_settings
from .utils.docs import DESCRIPTION, TAGS
from .utils.logger import logger
from . import routers

from .lifespan import lifespan


def create_app() -> FastAPI:
    # region Docs
    """
    Configures the base settings for the app, connecting routes and middlewares

    Returns:
        fastapi_app: configured application for usage
    """
    # endregion

    fastapi_app = FastAPI(
        title="Flux",
        description=DESCRIPTION,
        summary="API endpoints for the Flux Central hub",
        openapi_tags=TAGS,
        lifespan=lifespan,
    )

    #     fastapi_app.add_middleware(ExceptionMiddleware)

    fastapi_app.state.settings = generate_settings()

    fastapi_app.include_router(routers.router)

    @fastapi_app.get("/", tags=["general"], status_code=HTTPStatus.OK)
    async def get_root() -> dict:
        """Root Endpoint"""
        logger.info("Root endpoint called")
        return {"Flux": "Fluctuating data to create synergies"}

    return fastapi_app


app = create_app()
