from sqlmodel import Session

from app.db import get_engine, init_db
from app.repository import (
    get_recent_alerts,
    get_recent_reports,
    get_settings,
    save_alert,
    save_event,
    save_explanation,
    save_instrument_mapping,
    save_snapshot,
)


def test_repository_helpers(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        settings = get_settings(session)
        snapshot = save_snapshot(
            session, {"market_id": "m1", "asset_id": "t1", "odds": 0.4}
        )
        event = save_event(
            session,
            {"triggered": ["odds_jump_abs"], "current": {"odds": 0.4, "asset_id": "t1"}},
        )
        alert = save_alert(session, {"asset_id": "t1", "subject": "Test", "body": "Body"})

        assert settings.alert_cooldown_minutes == 30
        assert snapshot.id is not None
        assert event.triggered == "odds_jump_abs"
        assert alert.id is not None

        assert get_recent_alerts(session, limit=1)[0].id == alert.id
        assert get_recent_reports(session, limit=5) == []


def test_repository_saves_enrichment(monkeypatch, tmp_path):
    db_path = tmp_path / "repo.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        explanation = save_explanation(
            session,
            {
                "event_id": 1,
                "summary": "S",
                "confidence": 0.6,
                "citations": ["a"],
            },
        )
        mapping = save_instrument_mapping(
            session,
            {"event_id": 1, "instrument_type": "crypto", "symbol": "BTC-USD"},
        )

        assert explanation.id is not None
        assert mapping.id is not None
        assert explanation.citations == "a"
