from loguru import logger
try:
    from .intents import detect_intent
    from .llm_gemini import GeminiLLM
    from .news_service import NewsService
    from .weather_service import WeatherService
    from .memory import ShortTermMemory
except ImportError:
    from intents import detect_intent
    from llm_gemini import GeminiLLM
    from news_service import NewsService
    from weather_service import WeatherService
    from memory import ShortTermMemory

SYSTEM_STYLE = (
    "You are a helpful, concise assistant. "
    "Cite concrete facts from provided data when available, avoid hallucinations."
)

class Agent:
    def __init__(self):
        self.llm = GeminiLLM()
        self.news = NewsService()
        self.weather = WeatherService()
        self.memory = ShortTermMemory(capacity=5)

    async def answer(self, query: str) -> tuple[str, str, list[str]]:
        used_tools: list[str] = []
        intent, topic = detect_intent(query)
        logger.info(f"Detected intent: {intent} | topic: {topic}")

        reasoning = [f"Detected intent: {intent}"]

        if intent == "news":
            articles = await self.news.search(topic or query)
            used_tools.append("newsapi")
            reasoning.append("Fetched recent articles using NewsAPI.")
            formatted = self.news.format_for_llm(articles)
            prompt = (
                f"{SYSTEM_STYLE}\n"
                f"User asked: '{query}'.\n"
                f"Recent articles:\n{formatted}\n\n"
                f"Task: Produce a short, neutral summary (3-6 sentences). "
                f"If no articles, say so."
            )
            answer = await self.llm.complete(prompt)
            self.memory.push(query, answer)
            return "\n".join(reasoning), answer, used_tools

        if intent == "weather":
            weather_data = await self.weather.get_weather(topic or "Paris")
            used_tools.append("openweather")
            reasoning.append("Fetched weather data from OpenWeather API and combined it with reasoning from GPT.")
            formatted = self.weather.format_weather(weather_data)
            prompt = (
                f"{SYSTEM_STYLE}\n"
                f"User asked: '{query}'.\n"
                f"Weather data: {formatted}\n\n"
                f"Task: Provide a concise weather summary."
            )
            answer = await self.llm.complete(prompt)
            self.memory.push(query, answer)
            return "\n".join(reasoning), answer, used_tools

        # default: LLM-only
        reasoning.append("No external data required; answered with LLM.")
        mem_text = self.memory.as_text()
        prompt = (
            f"{SYSTEM_STYLE}\n"
            f"User asked: {query}\n\n"
            f"Recent short-term memory:\n{mem_text}\n\n"
            f"Answer helpfully in 2-6 sentences."
        )
        answer = await self.llm.complete(prompt)
        self.memory.push(query, answer)
        return "\n".join(reasoning), answer, used_tools
