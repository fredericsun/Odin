from datetime import date

from sqlmodel import Session, select

from app.db import get_engine, init_db
from app.models import (
    Explanation,
    InstrumentMapping,
    MarketEvent,
    MarketSnapshot,
    Report,
)


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


def test_models_store_explanations_and_mappings(monkeypatch, tmp_path):
    db_path = tmp_path / "models.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        event = MarketEvent(
            market_id="m1",
            asset_id="t1",
            triggered="odds_jump_abs",
            odds=0.4,
            score=0.3,
        )
        session.add(event)
        session.commit()

        session.add(
            Explanation(
                event_id=event.id,
                summary="S",
                confidence=0.7,
                citations="a,b",
            )
        )
        session.add(
            InstrumentMapping(
                event_id=event.id,
                instrument_type="crypto",
                symbol="BTC-USD",
                rationale="match",
            )
        )
        session.add(Report(report_date=date(2026, 1, 16), subject="Daily", body="Hello"))
        session.commit()

        explanations = session.exec(select(Explanation)).all()
        mappings = session.exec(select(InstrumentMapping)).all()

    assert explanations[0].summary == "S"
    assert mappings[0].symbol == "BTC-USD"
