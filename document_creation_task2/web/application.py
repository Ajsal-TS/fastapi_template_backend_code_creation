from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from document_creation_task2.logging import configure_logging
from document_creation_task2.web.api.router import api_router
from document_creation_task2.web.api.users.views import router
from document_creation_task2.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="document_creation_task2",
        version=metadata.version("document_creation_task2"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=router, prefix="/api")
    return app
