import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

_settings = None


@dataclass
class Settings:
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() in ("1", "true")


def get_settings() -> Settings:

    global _settings
    if _settings is None:
        try:
            _settings = Settings()
        except Exception:
            # Defensive fallback in case Settings constructor raises
            _settings = Settings(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8000")),
                debug=os.getenv("DEBUG", "false").lower() in ("1", "true"),
            )
    return _settings


__all__ = ["get_settings", "Settings"]
