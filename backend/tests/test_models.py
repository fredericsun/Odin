from datetime import date

from sqlmodel import Session, select

from app.db import get_engine, init_db
from app.models import MarketEvent, MarketSnapshot, Report


def test_models_can_insert_rows(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add(
            MarketSnapshot(
                market_id="m1",
                asset_id="t1",
                odds=0.4,
                volume=10,
                liquidity=20,
            )
        )
        session.add(
            MarketEvent(
                market_id="m1",
                asset_id="t1",
                triggered="odds_jump_abs",
                odds=0.4,
            )
        )
        session.add(Report(report_date=date(2026, 1, 16), subject="Daily", body="Hello"))
        session.commit()

        snapshots = session.exec(select(MarketSnapshot)).all()
        events = session.exec(select(MarketEvent)).all()
        reports = session.exec(select(Report)).all()

    assert len(snapshots) == 1
    assert len(events) == 1
    assert len(reports) == 1
