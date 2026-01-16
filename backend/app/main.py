from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.settings import router as settings_router
from app.worker import run_once


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router, prefix="/api")
    app.include_router(settings_router, prefix="/api")

    @app.post("/api/run-once")
    def run_once_endpoint():
        return run_once()

    return app
