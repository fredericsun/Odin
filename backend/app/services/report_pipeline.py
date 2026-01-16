from datetime import date

from sqlmodel import Session, select

from app.models import MarketEvent, Report
from app.services.reporting import compile_daily_report


def create_daily_report(session: Session, report_date: date) -> Report:
    events = session.exec(select(MarketEvent)).all()
    body = compile_daily_report(
        [{"market": event.market_id, "score": 0} for event in events]
    )
    report = Report(report_date=report_date, subject="Daily Report", body=body)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
