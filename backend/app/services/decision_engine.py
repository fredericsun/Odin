from app.models import Settings
from app.services.scoring import score_event


def score_and_gate(event: dict, settings: Settings) -> tuple[float, bool]:
    weights = {
        "odds": settings.odds_weight,
        "volume": settings.volume_weight,
        "liquidity": settings.liquidity_weight,
    }
    score = score_event(event, weights)
    score += event.get("llm_confidence", 0.0) * settings.llm_weight
    score += event.get("source_count", 0.0) * settings.sources_weight
    return score, score >= settings.min_score_threshold
