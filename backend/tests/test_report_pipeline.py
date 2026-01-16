from datetime import date

from sqlmodel import Session

from app.db import get_engine, init_db
from app.models import MarketEvent
from app.services.report_pipeline import create_daily_report


def test_create_daily_report(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add(
            MarketEvent(
                market_id="m1",
                asset_id="t1",
                triggered="odds_jump_abs",
                odds=0.4,
            )
        )
        session.commit()
        report = create_daily_report(session, report_date=date(2026, 1, 16))
        assert report.id is not None
        assert "Daily Report" in report.body
