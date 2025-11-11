import httpx
from loguru import logger
try:
    from .settings import settings
except ImportError:
    from settings import settings

NEWS_BASE = "https://newsapi.org/v2/everything"

class NewsService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY

    async def search(self, topic: str, page_size: int = 6, language: str = "en") -> list[dict]:
        if not self.api_key:
            logger.warning("NEWS_API_KEY not set.")
            return []
        params = {
            "q": topic,
            "apiKey": self.api_key,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "language": language
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(NEWS_BASE, params=params)
            if r.status_code != 200:
                logger.error(f"NewsAPI error {r.status_code}: {r.text}")
                return []
            data = r.json()
            return data.get("articles", [])

    @staticmethod
    def format_for_llm(arts: list[dict]) -> str:
        if not arts:
            return "No recent articles found."
        lines = []
        for a in arts:
            title = a.get("title", "Untitled")
            src = a.get("source", {}).get("name", "Unknown")
            date = a.get("publishedAt", "")[:10]
            url = a.get("url", "")
            lines.append(f"- {title} — {src} ({date}) {url}")
        return "\n".join(lines)
