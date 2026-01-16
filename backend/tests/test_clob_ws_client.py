import json

from app.services.clob_ws_client import ClobWsClient, build_market_subscription


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
