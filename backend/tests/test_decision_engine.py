from app.models import Settings
from app.services.decision_engine import score_and_gate


def test_score_and_gate_uses_threshold():
    settings = Settings(
        min_score_threshold=0.2,
        odds_weight=1.0,
        volume_weight=0.0,
        liquidity_weight=0.0,
    )
    event = {
        "odds": 0.3,
        "volume": 0.0,
        "liquidity": 0.0,
        "llm_confidence": 0.0,
        "source_count": 0,
    }

    score, passes = score_and_gate(event, settings)

    assert score == 0.3
    assert passes is True
