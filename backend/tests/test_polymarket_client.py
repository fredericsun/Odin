import httpx
import respx

from app.services.polymarket_client import PolymarketClient


@respx.mock
def test_fetch_markets_returns_list():
    url = "https://example.polymarket/api/markets"
    respx.get(url).mock(return_value=httpx.Response(200, json={"markets": [{"id": "m1"}]}))
    client = PolymarketClient(base_url="https://example.polymarket")
    markets = client.fetch_markets(limit=1)
    assert markets == [{"id": "m1"}]
