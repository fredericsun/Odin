import json
from typing import Callable, Optional

import websocket


def build_market_subscription(
    asset_ids: list[str], operation: Optional[str] = "subscribe"
) -> dict:
    payload = {"type": "market", "assets_ids": asset_ids}
    if operation:
        payload["operation"] = operation
    return payload


class ClobWsClient:
    def __init__(
        self,
        ws_url: str = "wss://ws-subscriptions-clob.polymarket.com/ws/market",
        websocket_factory: Optional[Callable[[], websocket.WebSocket]] = None,
    ):
        self.ws_url = ws_url
        self.websocket_factory = websocket_factory or websocket.WebSocket

    def connect(self) -> websocket.WebSocket:
        ws = self.websocket_factory()
        ws.connect(self.ws_url)
        return ws

    def subscribe(self, ws: websocket.WebSocket, asset_ids: list[str]) -> None:
        payload = build_market_subscription(asset_ids)
        ws.send(json.dumps(payload))

    def send_ping(self, ws: websocket.WebSocket) -> None:
        ws.ping()
