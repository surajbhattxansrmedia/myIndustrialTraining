from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from playground_fantasymanager.web.api.router import api_router
from playground_fantasymanager.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="playground_fantasymanager",
        version=metadata.version("playground_fantasymanager"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
