from sqlmodel import Session

from app.db import get_engine, init_db
from app.repository import (
    get_recent_alerts,
    get_recent_reports,
    get_settings,
    save_alert,
    save_event,
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
