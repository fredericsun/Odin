from typing import Optional

from sqlmodel import Session

from app.db import get_engine, init_db
from app.repository import get_settings, save_event, save_snapshot
from app.services.alert_pipeline import send_alerts_for_events
from app.services.clob_ws_client import ClobWsClient
from app.services.gamma_client import GammaClient
from app.services.polymarket_universe import (
    extract_clob_token_ids,
    select_top_markets_by_liquidity,
)
from app.services.signal_engine import RingBuffer, SignalEngine


def process_market_stream(
    ws_client: ClobWsClient,
    ws,
    max_messages: Optional[int] = None,
    odds_jump_abs: float = 0.05,
) -> tuple[list[dict], list[dict]]:
    buffers: dict[str, RingBuffer] = {}
    engine = SignalEngine(odds_jump_abs=odds_jump_abs)
    events: list[dict] = []
    snapshots: list[dict] = []

    for update in ws_client.iter_market_messages(ws, max_messages=max_messages):
        asset_id = update.get("asset_id") or update.get("market_id") or "unknown"
        buffer = buffers.setdefault(asset_id, RingBuffer())
        event = engine.detect(buffer, update)
        buffer.append(update)
        snapshots.append(update)
        if event:
            event["asset_id"] = asset_id
            event["market_id"] = update.get("market_id")
            events.append(event)

    return events, snapshots


def run_once(engine=None, max_messages: Optional[int] = 5) -> dict:
    client = GammaClient()
    try:
        markets = client.fetch_markets(limit=50)
    except Exception:
        markets = []

    top_markets = select_top_markets_by_liquidity(markets, limit=50)
    token_ids = extract_clob_token_ids(top_markets)

    ws_client = ClobWsClient()
    events: list[dict] = []
    snapshots: list[dict] = []
    ws = None
    try:
        ws = ws_client.connect()
        ws_client.subscribe(ws, token_ids)
        events, snapshots = process_market_stream(
            ws_client, ws, max_messages=max_messages, odds_jump_abs=0.05
        )
    except Exception:
        pass
    finally:
        if ws is not None:
            try:
                ws.close()
            except Exception:
                pass

    engine = engine or get_engine()
    init_db(engine)
    with Session(engine) as session:
        settings = get_settings(session)
        for snapshot in snapshots:
            save_snapshot(session, snapshot)
        event_records = []
        for event in events:
            event_records.append(save_event(session, event))
        for event, record in zip(events, event_records):
            event["event_id"] = record.id
        send_alerts_for_events(session, settings, events, sender=_make_sender(settings))

    return {
        "status": "ok",
        "markets_count": len(markets),
        "token_ids_count": len(token_ids),
        "events_count": len(events),
    }


def _make_sender(settings):
    from app.services.alerting import EmailAlertSender
    import smtplib

    smtp_user = getattr(settings, "gmail_smtp_user", None)
    smtp_password = getattr(settings, "gmail_smtp_password", None)

    if not smtp_user or not smtp_password:
        class NullSender:
            def send(self, subject: str, body: str) -> None:
                return None

        return NullSender()

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(smtp_user, smtp_password)
    return EmailAlertSender(
        smtp_client=smtp, from_addr=smtp_user, to_addr=smtp_user
    )
