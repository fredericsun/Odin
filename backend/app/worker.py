from app.services.clob_ws_client import ClobWsClient
from app.services.gamma_client import GammaClient
from app.services.polymarket_universe import (
    extract_clob_token_ids,
    select_top_markets_by_liquidity,
)


def run_once() -> dict:
    client = GammaClient()
    try:
        markets = client.fetch_markets(limit=50)
    except Exception:
        markets = []

    top_markets = select_top_markets_by_liquidity(markets, limit=50)
    token_ids = extract_clob_token_ids(top_markets)

    ws_client = ClobWsClient()
    try:
        ws = ws_client.connect()
        ws_client.subscribe(ws, token_ids)
        ws.close()
    except Exception:
        pass

    return {
        "status": "ok",
        "markets_count": len(markets),
        "token_ids_count": len(token_ids),
    }
