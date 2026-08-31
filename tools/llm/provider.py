class LLMProvider:

    def chat(self, messages):
        raise NotImplementedError(
            "LLM provider must implement chat()."
        )