from config import (
    DEFAULT_PROVIDER,
    OLLAMA_MODEL
)

from ollama_provider import OllamaProvider


def get_llm():

    if DEFAULT_PROVIDER == "ollama":

        return OllamaProvider(
            model=OLLAMA_MODEL
        )

    raise ValueError(
        f"Unknown LLM provider: {DEFAULT_PROVIDER}"
    )