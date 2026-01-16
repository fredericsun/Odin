from app.services.polymarket_universe import (
    extract_clob_token_ids,
    select_top_markets_by_liquidity,
)


def test_select_top_markets_by_liquidity():
    markets = [
        {"id": "m1", "liquidity": 100},
        {"id": "m2", "liquidity": 50},
        {"id": "m3", "liquidity": 200},
    ]
    top = select_top_markets_by_liquidity(markets, limit=2)
    assert [market["id"] for market in top] == ["m3", "m1"]


def test_extract_clob_token_ids_dedupes():
    markets = [
        {"clobTokenIds": ["t1", "t2"]},
        {"clobTokenIds": ["t2", "t3"]},
        {"clobTokenIds": None},
    ]
    assert extract_clob_token_ids(markets) == ["t1", "t2", "t3"]
