import re

NEWS_KEYWORDS = [
    "news", "headline", "headlines", "latest", "breaking", "update", "updates", "today",
    "summarize the news", "recent", "current events"
]

WEATHER_KEYWORDS = [
    "weather", "temperature", "forecast", "rain", "sunny", "cloudy", "wind", "humidity",
    "what's the weather", "how's the weather", "is it raining", "is it sunny"
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())

def detect_intent(query: str) -> tuple[str, str | None]:
    """
    Returns (intent, topic)
    intent ∈ {"news", "weather", "llm"}
    topic: extracted topic for news/weather queries, else None
    """
    q = normalize(query)
    # if any news-y word appears, treat as news query
    if any(k in q for k in NEWS_KEYWORDS):
        # try to extract a topic after "about/on/of" etc.
        topic = None
        m = re.search(r"(news|latest|headlines|updates|about|on)\s+(.*)", q)
        if m:
            topic = m.group(2).strip(" ?.,")
        # fallback: whole query as topic
        topic = topic or q
        return "news", topic
    # if any weather-y word appears, treat as weather query
    if any(k in q for k in WEATHER_KEYWORDS):
        # try to extract city after "in/for" etc.
        topic = None
        m = re.search(r"(weather|temperature|forecast|in|for)\s+(.*)", q)
        if m:
            topic = m.group(2).strip(" ?.,")
        # fallback: assume a default city or whole query
        topic = topic or "Paris"  # default city if not specified
        return "weather", topic
    return "llm", None
