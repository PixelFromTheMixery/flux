"""Exception Middleware for managing errors"""

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import requests

# from utils.exception import AnytypeException
from ..utils.logger import logger

# from .utils.pushover import PushoverUtils

from ..settings import generate_settings


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    File read and write combo for yaml sync to local instance

    Attributes:
        app (FastAPI): The base app through which we route exception messaging
        settings (dict): Settings instance to load optional pushover notification
    """

    def __init__(self, app):
        """
        Loader for exception Middleware

        Args:
            app (FastAPI): app, from main, that exceptions pass through
        """

        super().__init__(app)
        settings = generate_settings()
        # if not settings.config.local:
        #   self.pushover = PushoverUtils()

    async def dispatch(self, request, call_next):
        """
        Dispatches Error message through multiple channels

        Args:
            request (#TODO): I assume it's the next exception in the queue
            callnext? (#TODO): I assume it's a... no clue
             ():

        Returns:
            dict: error messaging
        Raises:
            Exception: Any error in the software
            Exception(2): If there's an error with sending the error
            Exception(3): Error with sending pushover notification of the error
        """

        try:
            response = await call_next(request)
            return response
        # except AnytypeException as exc:
        #    logger.error(exc)
        #    return JSONResponse({"Anytype error": exc.message}, exc.status)
        except Exception as exc:
            error_type = type(exc).__name__
            detail = str(exc)

            if isinstance(exc, requests.exceptions.HTTPError):
                try:
                    detail = exc.response.json().get("message", detail)
                except Exception:
                    detail = exc.response.text[:100]

            logger.error(f"Unhandled exception at {request.url.path}: {detail}")

            content = {
                "status": "error",
                "type": error_type,
                "message": detail,
                "path": f"{request.method} {request.url.path}",
            }

            try:
                self.pushover.send_message(
                    f"API Error: {error_type}", detail, priority=1
                )
            except:
                return JSONResponse(content, 500)
