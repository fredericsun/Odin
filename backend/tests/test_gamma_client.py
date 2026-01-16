import httpx
import respx

from app.services.gamma_client import GammaClient


@respx.mock
def test_fetch_markets_returns_list():
    url = "https://gamma-api.polymarket.com/markets"
    respx.get(url).mock(return_value=httpx.Response(200, json=[{"id": "m1"}]))
    client = GammaClient()
    markets = client.fetch_markets(limit=1)
    assert markets == [{"id": "m1"}]
