import ollama

from provider import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model="llama3.2:3b"
    ):

        self.model = model

    def chat(self, messages):

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": 0
            }
        )

        return response["message"]["content"]