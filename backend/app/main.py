from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.settings import router as settings_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router, prefix="/api")
    app.include_router(settings_router, prefix="/api")
    return app
