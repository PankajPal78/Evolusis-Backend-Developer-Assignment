import google.generativeai as genai
from loguru import logger
try:
    from .settings import settings
except ImportError:
    from settings import settings

class GeminiLLM:
    def __init__(self, model: str | None = None):
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set. LLM calls will fail.")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model or settings.GEMINI_MODEL)

    async def complete(self, prompt: str) -> str:
        if not settings.GEMINI_API_KEY:
            return "LLM unavailable (missing GEMINI_API_KEY)."
        try:
            # google-generativeai is sync; we call it directly here
            resp = self.model.generate_content(prompt)
            return (resp.text or "").strip() if resp else "No response."
        except Exception as e:
            logger.exception("Gemini error")
            return f"LLM error: {e}"
