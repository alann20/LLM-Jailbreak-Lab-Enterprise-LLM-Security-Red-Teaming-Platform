from .config import MODEL_PROVIDER, MODEL_NAME, OPENAI_API_KEY


class LLMClient:

    def __init__(self):

        self.provider = MODEL_PROVIDER.lower()

        if self.provider == "openai":
            self._initialize_openai()

        elif self.provider == "mock":
            self.client = None

        else:
            raise ValueError(
                f"Unsupported MODEL_PROVIDER: "
                f"{self.provider}"
            )

    def _initialize_openai(self):

        if not OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        from openai import OpenAI

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def execute(self, prompt: str) -> str:

        if self.provider == "mock":
            return self._mock_response(prompt)

        if self.provider == "openai":
            return self._openai_response(prompt)

        raise RuntimeError(
            f"Unsupported provider: {self.provider}"
        )

    def _openai_response(self, prompt: str) -> str:

        response = self.client.responses.create(
            model=MODEL_NAME,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise AI assistant. "
                        "Follow applicable safety policies. "
                        "Do not provide harmful operational "
                        "instructions."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.output_text

    def _mock_response(self, prompt: str) -> str:

        safety_response = (
            "I cannot assist with bypassing safety "
            "controls or providing harmful instructions. "
            "I can help evaluate the security behavior "
            "of an AI system in a controlled environment."
        )

        return safety_response