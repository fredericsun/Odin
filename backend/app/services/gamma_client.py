import httpx


class GammaClient:
    def __init__(self, base_url: str = "https://gamma-api.polymarket.com"):
        self.base_url = base_url.rstrip("/")

    def fetch_markets(self, limit: int = 50) -> list[dict]:
        url = f"{self.base_url}/markets"
        resp = httpx.get(url, params={"limit": limit}, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            return payload.get("markets", [])
        return []
