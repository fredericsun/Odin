from app.services.polymarket_client import PolymarketClient


def run_once() -> dict:
    client = PolymarketClient(base_url="https://example.polymarket")
    try:
        client.fetch_markets(limit=1)
    except Exception:
        pass
    return {"status": "ok"}
