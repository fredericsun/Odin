from app.services.scoring import score_event


def test_score_event_weighted_sum():
    event = {"odds": 0.5, "volume": 2000, "liquidity": 8000}
    weights = {"odds": 0.4, "volume": 0.3, "liquidity": 0.3}
    score = score_event(event, weights)
    assert round(score, 2) == 0.50
