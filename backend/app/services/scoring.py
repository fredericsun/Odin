def score_event(event: dict, weights: dict) -> float:
    odds = event.get("odds", 0.0)
    volume = event.get("volume", 0.0) / 10000.0
    liquidity = event.get("liquidity", 0.0) / 10000.0
    return (
        odds * weights.get("odds", 0.0)
        + volume * weights.get("volume", 0.0)
        + liquidity * weights.get("liquidity", 0.0)
    )
