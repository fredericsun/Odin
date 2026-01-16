from app.models import Settings
from app.services.scoring import score_event


def score_and_gate(event: dict, settings: Settings) -> tuple[float, bool]:
    weights = {
        "odds": settings.odds_weight,
        "volume": settings.volume_weight,
        "liquidity": settings.liquidity_weight,
    }
    score = score_event(event, weights)
    return score, score >= settings.min_score_threshold
