import json

from app.services.clob_ws_client import (
    ClobWsClient,
    build_market_subscription,
    normalize_market_payload,
)


def test_build_market_subscription():
    payload = build_market_subscription(["a1", "b2"])
    assert payload == {
        "type": "market",
        "assets_ids": ["a1", "b2"],
        "operation": "subscribe",
    }


def test_subscribe_sends_payload():
    class FakeWebSocket:
        def __init__(self):
            self.sent = []

        def connect(self, _):
            return None

        def send(self, message):
            self.sent.append(message)

    fake_ws = FakeWebSocket()
    client = ClobWsClient(websocket_factory=lambda: fake_ws)
    ws = client.connect()
    client.subscribe(ws, ["a1"])

    assert len(fake_ws.sent) == 1
    assert json.loads(fake_ws.sent[0]) == {
        "type": "market",
        "assets_ids": ["a1"],
        "operation": "subscribe",
    }


def test_normalize_market_payload_last_trade_price():
    payload = {
        "market": {
            "lastTradePrice": "0.42",
            "volume": "100",
            "liquidity": "200",
            "marketId": "m1",
            "assetId": "t1",
        }
    }
    normalized = normalize_market_payload(payload)
    assert normalized == {
        "odds": 0.42,
        "volume": 100.0,
        "liquidity": 200.0,
        "market_id": "m1",
        "asset_id": "t1",
    }


def test_normalize_market_payload_from_book():
    payload = {"data": {"bids": [["0.40", "10"]], "asks": [["0.50", "8"]]}}
    normalized = normalize_market_payload(payload)
    assert normalized["odds"] == 0.45


def test_iter_market_messages_parses_payload():
    class FakeWebSocket:
        def __init__(self):
            self.messages = [
                json.dumps({"market": {"lastTradePrice": "0.12"}}).encode("utf-8")
            ]

        def connect(self, _):
            return None

        def recv(self):
            return self.messages.pop(0)

    fake_ws = FakeWebSocket()
    client = ClobWsClient(websocket_factory=lambda: fake_ws)
    ws = client.connect()
    messages = list(client.iter_market_messages(ws, max_messages=1))
    assert messages == [{"odds": 0.12, "volume": 0.0, "liquidity": 0.0, "market_id": None, "asset_id": None}]
