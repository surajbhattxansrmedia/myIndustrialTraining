"""Exception handlers for the application."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from playground_fantasymanager.exceptions.base import AppError

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> Response:
    """
    Handle custom application exceptions.

    :param request: FastAPI request object
    :param exc: Application exception
    :return: JSON response with error details
    """
    if not isinstance(exc, AppError):
        # This shouldn't happen if properly registered, but handle gracefully
        logger.error("Non-AppError passed to app_exception_handler: %s", type(exc))
        return await general_exception_handler(request, exc)

    logger.warning(
        "Application exception occurred: %s",
        exc.message,
        extra={
            "status_code": exc.status_code,
            "description": exc.description,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "code": exc.code,
            "error": exc.__class__.__name__,
            "message": exc.message,
            "description": exc.description if exc.description else exc.message,
        },
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> Response:
    """
    Handle unexpected exceptions.

    :param request: FastAPI request object
    :param exc: General exception
    :return: JSON response with generic error message
    """
    logger.error(
        "Unexpected exception occurred: %s",
        str(exc),
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
            "code": "INTERNAL_SERVER_ERROR",
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "description": "Please contact support if this error persists",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register exception handlers with the FastAPI application.

    :param app: FastAPI application instance
    """
    app.add_exception_handler(AppError, app_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
