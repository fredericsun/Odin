from sqlmodel import Session, select

from app.models import (
    Alert,
    Explanation,
    InstrumentMapping,
    MarketEvent,
    MarketSnapshot,
    Report,
    Settings,
)


def get_settings(session: Session) -> Settings:
    settings = session.exec(select(Settings)).first()
    if settings is None:
        settings = Settings()
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return settings


def save_snapshot(session: Session, payload: dict) -> MarketSnapshot:
    snapshot = MarketSnapshot(
        market_id=payload.get("market_id"),
        asset_id=payload.get("asset_id"),
        odds=payload.get("odds", 0.0),
        volume=payload.get("volume", 0.0),
        liquidity=payload.get("liquidity", 0.0),
    )
    session.add(snapshot)
    session.commit()
    session.refresh(snapshot)
    return snapshot


def save_event(session: Session, payload: dict) -> MarketEvent:
    current = payload.get("current") or {}
    triggered = payload.get("triggered") or []
    triggered_str = ",".join(triggered)
    event = MarketEvent(
        market_id=payload.get("market_id") or current.get("market_id"),
        asset_id=payload.get("asset_id") or current.get("asset_id"),
        triggered=triggered_str,
        odds=current.get("odds", 0.0),
        volume=current.get("volume", 0.0),
        liquidity=current.get("liquidity", 0.0),
        score=payload.get("score", 0.0),
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def save_alert(session: Session, payload: dict) -> Alert:
    alert = Alert(
        event_id=payload.get("event_id"),
        asset_id=payload.get("asset_id"),
        status=payload.get("status", "sent"),
        subject=payload.get("subject", ""),
        body=payload.get("body", ""),
    )
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert


def save_explanation(session: Session, payload: dict) -> Explanation:
    citations = payload.get("citations") or []
    explanation = Explanation(
        event_id=payload.get("event_id"),
        summary=payload.get("summary", ""),
        confidence=payload.get("confidence", 0.0),
        citations=",".join(citations),
    )
    session.add(explanation)
    session.commit()
    session.refresh(explanation)
    return explanation


def save_instrument_mapping(session: Session, payload: dict) -> InstrumentMapping:
    mapping = InstrumentMapping(
        event_id=payload.get("event_id"),
        instrument_type=payload.get("instrument_type", ""),
        symbol=payload.get("symbol", ""),
        rationale=payload.get("rationale", ""),
        price_context=payload.get("price_context", ""),
    )
    session.add(mapping)
    session.commit()
    session.refresh(mapping)
    return mapping


def get_recent_alerts(session: Session, limit: int = 50) -> list[Alert]:
    return session.exec(select(Alert).order_by(Alert.sent_at.desc()).limit(limit)).all()


def get_recent_reports(session: Session, limit: int = 30) -> list[Report]:
    return session.exec(select(Report).order_by(Report.report_date.desc()).limit(limit)).all()
