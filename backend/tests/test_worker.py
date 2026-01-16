from app.services.clob_ws_client import ClobWsClient
from app.services.gamma_client import GammaClient
from app.worker import run_once


def test_run_once_returns_result(monkeypatch):
    def fake_fetch_markets(self, limit=50):
        return [{"id": "m1", "liquidity": 10, "clobTokenIds": ["t1"]}]

    class FakeWebSocket:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    def fake_connect(self):
        return FakeWebSocket()

    def fake_subscribe(self, ws, asset_ids):
        ws.asset_ids = asset_ids

    def fake_iter_messages(self, ws, max_messages=None):
        yield {"odds": 0.1, "asset_id": "t1", "market_id": "m1"}
        yield {"odds": 0.2, "asset_id": "t1", "market_id": "m1"}

    monkeypatch.setattr(GammaClient, "fetch_markets", fake_fetch_markets)
    monkeypatch.setattr(ClobWsClient, "connect", fake_connect)
    monkeypatch.setattr(ClobWsClient, "subscribe", fake_subscribe)
    monkeypatch.setattr(ClobWsClient, "iter_market_messages", fake_iter_messages)

    result = run_once()
    assert result["status"] == "ok"
    assert result["markets_count"] == 1
    assert result["token_ids_count"] == 1
    assert result["events_count"] == 1
