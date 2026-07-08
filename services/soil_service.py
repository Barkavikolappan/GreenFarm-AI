"""
Optional soil data lookup (e.g. SoilGrids/ISRIC or a national soil-health-card API).
Without SOIL_API_KEY, the app simply relies on the farmer's manually entered
soil test values in the UI — this module is a placeholder integration point.
"""
import requests

from config import SOIL_API_KEY, SOIL_LIVE


def get_soil_estimate(lat: float, lon: float) -> dict:
    """
    Example integration point for a soil data provider.
    Returns None values if no live source is configured — the UI should
    then just use the farmer's manually entered soil test card values.
    """
    if not SOIL_LIVE:
        return {"source": "manual_input_required", "ph": None, "organic_carbon_pct": None}

    try:
        # Placeholder call — replace with your actual soil data provider's endpoint.
        resp = requests.get(
            "https://rest.isric.org/soilgrids/v2.0/properties/query",
            params={"lat": lat, "lon": lon, "property": ["phh2o", "ocd"]},
            timeout=10,
        ).json()
        return {
            "source": "live",
            "ph": resp.get("phh2o"),
            "organic_carbon_pct": resp.get("ocd"),
        }
    except Exception as e:
        return {"source": f"error: {e}", "ph": None, "organic_carbon_pct": None}
