# region Docs
"""
Exception Handler for Flux.


Classes:
    ExceptionMiddleware: Encapsulation for method and connecting FastAPI

"""
# endregion

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import requests

from ..utils.logger import logger


class ExceptionMiddleware(BaseHTTPMiddleware):
    # region Docs
    """
    File read and write combo for yaml sync to local instance

    Attributes:
        app (FastAPI): The base app through which we route exception messaging
        settings (dict): Settings instance to load optional pushover notification
    """

    # endregion

    def __init__(self, app) -> None:
        # region Docs
        """
        Loader for exception Middleware

        Args:
            app (FastAPI): app, from main, that exceptions pass through
        """
        # endregion

        super().__init__(app)

    def pushover_message(self, content) -> Response:
        # region Docs
        """
        Sends Pushover message on request error

        Args:
            content (dict): error messaging as detailed by exception parser

        Returns:
            Response: exception of below exception
        Raises:
            Exception: If pushover message failed
        """
        # endregion

        try:
            self.pushover.send_message(f"API Error: {content}")
        except Exception:  # pylint: disable=broad-exception-caught
            return Response(content, 500)

    def exception_parser(self, exc: Exception, request) -> Response:
        # region Docs
        """
        Transform exception into messaging for pushover and Response

        Args:
            exc (Exception): Exception object for parsing from all possible sources
            request (Request): the call made internally

        Returns:
            Response: Response object with error code 500 and parsed content
        Raises:
            Exception: message might not be in Exception, look at 'text' instead.
        """
        # endregion

        error_type = type(exc).__name__
        detail = str(exc)

        if isinstance(exc, requests.exceptions.HTTPError):
            try:
                detail = exc.response.json().get("message", detail)
            except Exception:  # pylint: disable=broad-exception-caught
                detail = exc.response.text[:100]

        logger.error("Unhandled exception at %s: %s", request.url.path, detail)

        exc_content = {
            "status": "error",
            "type": error_type,
            "message": detail,
            "path": f"{request.method} {request.url.path}",
        }
        if self.pushover:
            self.pushover_message(exc_content)

        return Response(exc_content, 500)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # region Docs
        """
        Dispatches Error message through multiple channels

        When an exception does happen, it collects information on which request was made
        Includes info such as endpoint, error type, and message.

        In case there is an error with capturing/sending the error, that is captured too.
        This for when passing through a third-party which has its own error messaging mechanism.

        Optionally, also sends the exception to Pushover if configured.

        Args:
            request (HTTPRequest): Incoming FastAPI request
            callnext? (Callable): Process that happened earlier

        Returns:
            dict: HTTP response from the app or JSON response with the error
        Raises:
            Exception: Any error in the software
            Exception(2): If there's an error with sending the error
            Exception(3): Error with sending pushover notification of the error
        """
        # endregion

        try:
            response = await call_next(request)
            return response
        # except AnytypeException as exc:
        #    logger.error(exc)
        #    return JSONResponse({"Anytype error": exc.message}, exc.status)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self.exception_passover(exc, request)
