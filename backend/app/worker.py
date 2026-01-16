from app.services.clob_ws_client import ClobWsClient
from app.services.gamma_client import GammaClient
from app.services.polymarket_universe import (
    extract_clob_token_ids,
    select_top_markets_by_liquidity,
)
from typing import Optional

from app.services.signal_engine import RingBuffer, SignalEngine


def process_market_stream(
    ws_client: ClobWsClient,
    ws,
    max_messages: Optional[int] = None,
    odds_jump_abs: float = 0.05,
) -> list[dict]:
    buffers: dict[str, RingBuffer] = {}
    engine = SignalEngine(odds_jump_abs=odds_jump_abs)
    events: list[dict] = []

    for update in ws_client.iter_market_messages(ws, max_messages=max_messages):
        asset_id = update.get("asset_id") or update.get("market_id") or "unknown"
        buffer = buffers.setdefault(asset_id, RingBuffer())
        event = engine.detect(buffer, update)
        buffer.append(update)
        if event:
            event["asset_id"] = asset_id
            event["market_id"] = update.get("market_id")
            events.append(event)

    return events


def run_once(max_messages: Optional[int] = 5) -> dict:
    client = GammaClient()
    try:
        markets = client.fetch_markets(limit=50)
    except Exception:
        markets = []

    top_markets = select_top_markets_by_liquidity(markets, limit=50)
    token_ids = extract_clob_token_ids(top_markets)

    ws_client = ClobWsClient()
    events: list[dict] = []
    ws = None
    try:
        ws = ws_client.connect()
        ws_client.subscribe(ws, token_ids)
        events = process_market_stream(
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

    return {
        "status": "ok",
        "markets_count": len(markets),
        "token_ids_count": len(token_ids),
        "events_count": len(events),
    }
