import json
from typing import Callable, Iterator, Optional

import websocket


def build_market_subscription(
    asset_ids: list[str], operation: Optional[str] = "subscribe"
) -> dict:
    payload = {"type": "market", "assets_ids": asset_ids}
    if operation:
        payload["operation"] = operation
    return payload


def _safe_float(value: object) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def _extract_price_from_book(entries: object) -> float:
    if not isinstance(entries, list) or not entries:
        return 0.0
    top = entries[0]
    if isinstance(top, dict):
        return _safe_float(top.get("price") or top.get("p"))
    if isinstance(top, (list, tuple)) and top:
        return _safe_float(top[0])
    return _safe_float(top)


def normalize_market_payload(payload: dict) -> Optional[dict]:
    data = payload.get("market") or payload.get("data") or payload
    if not isinstance(data, dict):
        return None

    odds = data.get("lastTradePrice") or data.get("last_trade_price") or data.get("price")
    if odds is None:
        best_bid = data.get("bestBid") or data.get("best_bid")
        best_ask = data.get("bestAsk") or data.get("best_ask")
        if best_bid is None and best_ask is None:
            best_bid = _extract_price_from_book(data.get("bids"))
            best_ask = _extract_price_from_book(data.get("asks"))
        best_bid_value = _safe_float(best_bid)
        best_ask_value = _safe_float(best_ask)
        if best_bid_value and best_ask_value:
            odds_value = (best_bid_value + best_ask_value) / 2
        else:
            odds_value = best_bid_value or best_ask_value
    else:
        odds_value = _safe_float(odds)

    if not odds_value:
        return None

    volume_value = _safe_float(
        data.get("volume") or data.get("volume24h") or data.get("volume_24h")
    )
    liquidity_value = _safe_float(data.get("liquidity"))
    return {
        "odds": odds_value,
        "volume": volume_value,
        "liquidity": liquidity_value,
        "market_id": data.get("market_id") or data.get("marketId") or data.get("id"),
        "asset_id": data.get("asset_id")
        or data.get("assetId")
        or data.get("tokenId")
        or data.get("clobTokenId"),
    }


def normalize_market_message(message: object) -> Optional[dict]:
    if isinstance(message, bytes):
        message = message.decode("utf-8", errors="ignore")
    if not isinstance(message, str):
        return None
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return normalize_market_payload(payload)


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

    def iter_market_messages(
        self, ws: websocket.WebSocket, max_messages: Optional[int] = None
    ) -> Iterator[dict]:
        received = 0
        while True:
            message = ws.recv()
            normalized = normalize_market_message(message)
            if normalized:
                yield normalized
            received += 1
            if max_messages is not None and received >= max_messages:
                break
