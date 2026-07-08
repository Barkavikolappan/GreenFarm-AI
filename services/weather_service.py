"""
Optional live weather via OpenWeatherMap.
Falls back to a clearly-labeled mock reading if WEATHER_API_KEY is not set,
so the app stays fully functional without any external key.
"""
import random
import requests

from config import WEATHER_API_KEY, WEATHER_LIVE


def get_weather_summary(location: str) -> dict:
    if WEATHER_LIVE:
        try:
            geo_url = "http://api.openweathermap.org/geo/1.0/direct"
            geo_resp = requests.get(
                geo_url, params={"q": location, "limit": 1, "appid": WEATHER_API_KEY}, timeout=8
            ).json()
            if not geo_resp:
                raise ValueError("Location not found")
            lat, lon = geo_resp[0]["lat"], geo_resp[0]["lon"]

            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            data = requests.get(
                weather_url,
                params={"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric"},
                timeout=8,
            ).json()

            return {
                "source": "live",
                "temperature_c": data["main"]["temp"],
                "humidity_pct": data["main"]["humidity"],
                "rain_chance_pct": None,  # needs One Call API tier for forecast probability
                "conditions": data["weather"][0]["description"],
            }
        except Exception as e:
            return _mock_weather(error=str(e))
    return _mock_weather()


def _mock_weather(error: str = None) -> dict:
    return {
        "source": "mock" if not error else f"mock (live fetch failed: {error})",
        "temperature_c": round(28 + random.random() * 6, 1),
        "humidity_pct": round(55 + random.random() * 30),
        "rain_chance_pct": round(random.random() * 100),
        "conditions": "partly cloudy",
    }
