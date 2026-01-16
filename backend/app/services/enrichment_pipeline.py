from app.services.explanation_engine import ExplanationEngine
from app.services.instrument_mapper import map_instruments


def enrich_event(event: dict, llm_client, sources: list[dict]) -> tuple[dict, list[dict]]:
    engine = ExplanationEngine(llm_client, sources)
    explanation = engine.explain(event)
    mappings = map_instruments(event)
    return explanation, mappings
