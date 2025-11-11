import httpx
from loguru import logger
try:
    from .settings import settings
except ImportError:
    from settings import settings

WEATHER_BASE = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

    async def get_weather(self, city: str) -> dict | None:
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not set.")
            return None
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(WEATHER_BASE, params=params)
            if r.status_code != 200:
                logger.error(f"OpenWeather error {r.status_code}: {r.text}")
                return None
            return r.json()

    @staticmethod
    def format_weather(data: dict) -> str:
        if not data:
            return "Weather data unavailable."
        temp = data.get("main", {}).get("temp")
        desc = data.get("weather", [{}])[0].get("description", "unknown")
        city = data.get("name", "Unknown")
        return f"It's {temp}°C and {desc} in {city} today."
