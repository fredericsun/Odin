def select_top_markets_by_liquidity(markets: list[dict], limit: int) -> list[dict]:
    def liquidity_value(market: dict) -> float:
        try:
            return float(market.get("liquidity", 0.0) or 0.0)
        except (TypeError, ValueError):
            return 0.0

    sorted_markets = sorted(markets, key=liquidity_value, reverse=True)
    return sorted_markets[:limit]


def extract_clob_token_ids(markets: list[dict]) -> list[str]:
    token_ids: list[str] = []
    seen: set[str] = set()
    for market in markets:
        for token_id in market.get("clobTokenIds") or []:
            if token_id not in seen:
                token_ids.append(token_id)
                seen.add(token_id)
    return token_ids
