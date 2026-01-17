from fastapi import FastAPI

from app.api.alerts import router as alerts_router
from app.api.health import router as health_router
from app.api.reports import router as reports_router
from app.api.settings import router as settings_router
from app.scheduler import build_scheduler, run_daily_report
from app.worker import run_once


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router, prefix="/api")
    app.include_router(settings_router, prefix="/api")
    app.include_router(alerts_router, prefix="/api")
    app.include_router(reports_router, prefix="/api")

    @app.post("/api/run-once")
    def run_once_endpoint():
        return run_once()

    scheduler = build_scheduler(run_once, run_daily_report, report_hour_local=7)

    @app.on_event("startup")
    def start_scheduler():
        scheduler.start()

    @app.on_event("shutdown")
    def stop_scheduler():
        scheduler.shutdown()

    return app
