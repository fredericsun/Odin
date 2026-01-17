from datetime import date

from sqlmodel import Session

from app.services.report_pipeline import create_daily_report


def send_daily_report(session: Session, sender, report_date: date):
    report = create_daily_report(session, report_date=report_date)
    sender.send(report.subject, report.body)
    return report
