from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.models import Alert, Settings
from app.repository import save_alert


def _recent_alert_exists(session: Session, asset_id: str, cooldown_minutes: int) -> bool:
    cutoff = datetime.utcnow() - timedelta(minutes=cooldown_minutes)
    recent = (
        session.exec(
            select(Alert)
            .where(Alert.asset_id == asset_id)
            .where(Alert.sent_at >= cutoff)
            .order_by(Alert.sent_at.desc())
        )
        .first()
    )
    return recent is not None


def send_alerts_for_events(
    session: Session,
    settings: Settings,
    events: list[dict],
    sender,
) -> None:
    for event in events:
        asset_id = event.get("asset_id") or "unknown"
        if _recent_alert_exists(session, asset_id, settings.alert_cooldown_minutes):
            continue
        subject = f"Polymarket alert: {asset_id}"
        body = (
            "Triggers: {triggers}\nOdds: {odds}".format(
                triggers=",".join(event.get("triggered", [])),
                odds=event.get("current", {}).get("odds", 0.0),
            )
        )
        sender.send(subject, body)
        save_alert(
            session,
            {
                "event_id": event.get("event_id"),
                "asset_id": asset_id,
                "subject": subject,
                "body": body,
                "status": "sent",
            },
        )
