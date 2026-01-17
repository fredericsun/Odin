from app.services.openai_client import OpenAIClient


class FakeOpenAI:
    class Responses:
        def create(self, **kwargs):
            class FakeOutput:
                output_text = "Summary"

            return FakeOutput()

    def __init__(self, api_key: str):
        self.responses = self.Responses()


def test_openai_client_summarize(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    client = OpenAIClient(openai_factory=FakeOpenAI)
    assert client.summarize("hello") == "Summary"
