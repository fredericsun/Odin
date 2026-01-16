from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.db import get_engine, init_db
from app.models import Alert
from app.repository import get_settings, save_alert
from app.services.alert_pipeline import send_alerts_for_events


class FakeSender:
    def __init__(self):
        self.sent = []

    def send(self, subject: str, body: str) -> None:
        self.sent.append((subject, body))


def test_alert_pipeline_dedupes(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        settings = get_settings(session)
        settings.alert_cooldown_minutes = 60
        session.add(settings)
        session.commit()

        save_alert(
            session,
            {
                "asset_id": "t1",
                "subject": "Old",
                "body": "Old",
                "status": "sent",
                "event_id": None,
            },
        )
        alert = session.exec(select(Alert)).first()
        alert.sent_at = datetime.utcnow() - timedelta(minutes=30)
        session.add(alert)
        session.commit()

        sender = FakeSender()
        events = [
            {
                "asset_id": "t1",
                "market_id": "m1",
                "triggered": ["odds_jump_abs"],
                "current": {"odds": 0.5},
            }
        ]
        send_alerts_for_events(session, settings, events, sender)

        assert sender.sent == []
