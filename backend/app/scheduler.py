from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from app.db import get_engine, init_db
from app.services.report_sender import send_daily_report


def build_scheduler(
    run_once_func, report_sender_func, report_hour_local: int
) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_once_func, "interval", seconds=90, id="run-once")
    scheduler.add_job(
        report_sender_func, "cron", hour=report_hour_local, minute=0, id="daily-report"
    )
    return scheduler


def run_daily_report():
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        send_daily_report(session, sender=_null_sender(), report_date=date.today())


def _null_sender():
    class NullSender:
        def send(self, subject: str, body: str) -> None:
            return None

    return NullSender()
