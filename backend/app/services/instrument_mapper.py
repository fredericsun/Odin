def map_instruments(event: dict) -> list[dict]:
    question = event.get("question", "").lower()
    mappings = []
    if "btc" in question or "bitcoin" in question:
        mappings.append({"type": "crypto", "symbol": "BTC-USD"})
    if "eth" in question or "ethereum" in question:
        mappings.append({"type": "crypto", "symbol": "ETH-USD"})
    return mappings
