from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    NEWS_API_KEY: str | None = os.getenv("NEWS_API_KEY")
    OPENWEATHER_API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY")

settings = Settings()
