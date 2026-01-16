from app.services.enrichment_pipeline import enrich_event


class FakeLLM:
    def summarize(self, prompt: str) -> str:
        return "Cause: Example. Sources: https://example.com"


def test_enrich_event_returns_explanation_and_mappings():
    event = {"question": "Will BTC be above $100k?"}
    sources = [{"title": "Example", "url": "https://example.com"}]

    explanation, mappings = enrich_event(event, FakeLLM(), sources)

    assert explanation["confidence"] > 0
    assert "https://example.com" in explanation["citations"]
    assert {"type": "crypto", "symbol": "BTC-USD"} in mappings
