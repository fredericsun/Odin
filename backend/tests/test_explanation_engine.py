from app.services.explanation_engine import ExplanationEngine


class FakeLLM:
    def summarize(self, prompt: str) -> str:
        return "Cause: Example headline. Sources: https://example.com"


def test_explanation_requires_citation():
    engine = ExplanationEngine(FakeLLM(), sources=[{"url": "https://example.com", "title": "Example"}])
    result = engine.explain({"market": "m1"})
    assert result["confidence"] > 0
    assert result["citations"] == ["https://example.com"]
