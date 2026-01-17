from datetime import date

from sqlmodel import Session

from app.db import get_engine, init_db
from app.models import MarketEvent
from app.services.report_sender import send_daily_report


class FakeSender:
    def __init__(self):
        self.sent = []

    def send(self, subject: str, body: str) -> None:
        self.sent.append((subject, body))


def test_send_daily_report(monkeypatch, tmp_path):
    db_path = tmp_path / "reports.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add(
            MarketEvent(
                market_id="m1", asset_id="t1", triggered="odds_jump_abs", odds=0.4
            )
        )
        session.commit()
        sender = FakeSender()
        report = send_daily_report(session, sender, report_date=date(2026, 1, 16))
        assert report.id is not None
        assert sender.sent
