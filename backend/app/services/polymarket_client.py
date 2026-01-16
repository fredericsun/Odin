import httpx


class PolymarketClient:
    def __init__(self, base_url: str = "https://polymarket.com"):
        self.base_url = base_url.rstrip("/")

    def fetch_markets(self, limit: int = 50) -> list[dict]:
        url = f"{self.base_url}/api/markets"
        resp = httpx.get(url, params={"limit": limit}, timeout=10)
        resp.raise_for_status()
        return resp.json().get("markets", [])
