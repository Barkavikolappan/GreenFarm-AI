"""
Thin wrapper around Gemini 2.5 Flash for all 6 GreenFarm AI modules.
Supports English and Tamil responses.
"""

import json
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL

_client = None


def get_client():
    global _client

    if _client is None:

        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to .streamlit/secrets.toml "
                "or as an environment variable."
            )

        _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


def _generate_json(
    prompt: str,
    image_bytes: bytes = None,
    mime_type: str = "image/jpeg",
    language: str = "English"
) -> dict:
    """
    Send prompt to Gemini and return JSON.
    """

    client = get_client()

    # Tamil instruction
    if language == "தமிழ்":

        prompt += """

IMPORTANT:

Reply completely in Tamil.

Use very simple Tamil that farmers can easily understand.

Avoid difficult English technical words.

Return ONLY valid JSON.

Keep JSON keys in English.

Translate every value into Tamil.

Example:

{
    "disease_name":"ஆரம்ப இலை கருகல்",
    "confidence_percent":92,
    "severity":"high",
    "explanation":"இந்த நோய் இலைகளை பாதிக்கிறது.",
    "treatment_steps":[
        "பாதிக்கப்பட்ட இலைகளை அகற்றவும்",
        "பூஞ்சைநாசினி தெளிக்கவும்"
    ]
}

"""

    contents = []

    if image_bytes:

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    contents.append(prompt)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )

    text = response.text.strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        cleaned = (
            text.replace("```json", "")
                .replace("```", "")
                .strip()
        )

        return json.loads(cleaned)


def diagnose_disease(
    crop: str,
    symptoms: str,
    image_bytes: bytes = None,
    language: str = "English"
) -> dict:

    prompt = f"""You are an agricultural plant pathologist AI for Indian farmers.

Crop: {crop}

Farmer-described symptoms: {symptoms or "none provided, rely on the image"}

Analyze the leaf/plant image (if provided) and symptoms. Respond ONLY as JSON:

{{
  "disease_name": string,
  "confidence_percent": number,
  "severity": "low" | "medium" | "high",
  "explanation": string,
  "treatment_steps": [string],
  "prevention_tips": [string]
}}"""

    return _generate_json(
        prompt,
        image_bytes=image_bytes,
        language=language
    )

def recommend_fertilizer(
    crop: str,
    stage: str,
    area_acres: float,
    soil_n: float,
    soil_p: float,
    soil_k: float,
    language: str = "English"
) -> dict:

    prompt = f"""You are an agronomist AI. Recommend fertilizer dosage for Indian smallholder farming.

Crop: {crop}
Growth stage: {stage}
Field size: {area_acres} acres

Soil test values (kg/ha):
N={soil_n}
P={soil_p}
K={soil_k}

Respond ONLY as JSON:

{{
  "urea_kg": number,
  "dap_kg": number,
  "mop_kg": number,
  "application_notes": ["string"],
  "biofertilizer_suggestion": "string"
}}
"""

    return _generate_json(
        prompt,
        language=language
    )


def weather_advisory(
    crop: str,
    location: str,
    weather_summary: str,
    language: str = "English"
) -> dict:

    prompt = f"""You are a farm weather advisor AI.

Crop: {crop}

Location:
{location}

Current weather data:
{weather_summary}

Respond ONLY as JSON:

{{
  "risk_level": "low" | "medium" | "high",
  "alerts": ["string"],
  "best_spray_window": "string",
  "irrigation_note": "string"
}}
"""

    return _generate_json(
        prompt,
        language=language
    )


def water_conservation_plan(
    crop: str,
    soil_type: str,
    area_acres: float,
    rainfall_mm: float,
    irrigation_method: str,
    language: str = "English"
) -> dict:

    prompt = f"""You are a water conservation advisor AI for Indian farms.

Crop: {crop}
Soil type: {soil_type}
Field size: {area_acres} acres
Rainfall in last 7 days: {rainfall_mm} mm
Current irrigation method: {irrigation_method}

Respond ONLY as JSON:

{{
  "weekly_water_demand_mm": number,
  "irrigation_deficit_mm": number,
  "estimated_water_needed_kilolitres": number,
  "efficiency_tips": [string, ...],
  "recommended_method": string
}}
"""

    return _generate_json(
        prompt,
        language=language
    )


def soil_health_analysis(
    ph: float,
    organic_carbon_pct: float,
    texture: str,
    last_crop: str,
    years_without_rotation: int,
    language: str = "English"
) -> dict:

    prompt = f"""You are a soil health advisor AI.

Soil pH: {ph}
Organic carbon: {organic_carbon_pct}%
Texture: {texture}
Last crop grown: {last_crop}
Years without crop rotation: {years_without_rotation}

Respond ONLY as JSON:

{{
  "status": "healthy" | "monitor" | "attention_needed",
  "findings": [string, ...],
  "rotation_suggestion": string,
  "amendment_suggestion": string
}}
"""

    return _generate_json(
        prompt,
        language=language
    )


def match_schemes(
    state: str,
    land_acres: float,
    farmer_category: str,
    interest: str,
    scheme_catalog: list,
    language: str = "English"
) -> dict:

    catalog_text = "\n".join(
        f"- {s['name']}: {s['desc']} "
        f"(subsidy: {s['subsidy']}, category: {s['cat']})"
        for s in scheme_catalog
    )

    prompt = f"""You are a government agriculture schemes advisor for Indian farmers.

Farmer Profile

State: {state}

Land: {land_acres} acres

Category: {farmer_category}

Interest: {interest}

Available Schemes

{catalog_text}

Select the best 3 to 5 schemes.

Respond ONLY as JSON.

{{
  "eligibility_note": string,
  "matched_schemes":[
      {{
        "name": string,
        "why_relevant": string
      }}
  ]
}}
"""

    return _generate_json(
        prompt,
        language=language
    )