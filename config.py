"""
Central config loader.
Reads from Streamlit secrets first (for Streamlit Community Cloud),
then falls back to environment variables (for Cloud Run / local .env).
"""
import os

try:
    import streamlit as st
    _SECRETS = st.secrets
except Exception:
    _SECRETS = {}


def _get(key: str, default: str = "") -> str:
    if key in _SECRETS:
        return _SECRETS[key]
    return os.environ.get(key, default)


GEMINI_API_KEY = _get("GEMINI_API_KEY")
GEMINI_MODEL = _get("GEMINI_MODEL", "gemini-2.5-flash")

WEATHER_API_KEY = _get("WEATHER_API_KEY")          # OpenWeatherMap key (optional)
SOIL_API_KEY = _get("SOIL_API_KEY")                # Soil data provider key (optional)

APP_TITLE = "GreenFarm AI"
DEFAULT_REGION = "Tamil Nadu, India"

# Feature flags — auto-disable an integration if its key is missing,
# so the app degrades gracefully to manual input / mock data instead of crashing.
WEATHER_LIVE = bool(WEATHER_API_KEY)
SOIL_LIVE = bool(SOIL_API_KEY)
