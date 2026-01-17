import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini", openai_factory=OpenAI):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai_factory(api_key=api_key)
        self.model = model

    def summarize(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
