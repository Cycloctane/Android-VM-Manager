from fastapi import FastAPI

app_metadata = {
    "title": "Android VM Controller",
    "summary": "TODO",
    "description": """
TODO
"""
}


def create_app() -> FastAPI:
    app = FastAPI(redoc_url=None, **app_metadata) # type: ignore

    from .routers.main_router import router as main_router
    app.include_router(main_router, prefix="")

    from .routers.api_router import router as api_router
    app.include_router(api_router, prefix="/api/v0")

    return app

