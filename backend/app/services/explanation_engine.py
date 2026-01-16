class ExplanationEngine:
    def __init__(self, llm_client, sources: list[dict]):
        self.llm_client = llm_client
        self.sources = sources

    def explain(self, event: dict) -> dict:
        urls = [s["url"] for s in self.sources if "url" in s]
        if not urls:
            return {"summary": "No sources available.", "confidence": 0, "citations": []}
        summary = self.llm_client.summarize(str(event))
        return {"summary": summary, "confidence": 0.5, "citations": urls[:3]}
