# GreenFarm AI

Sustainable agriculture agent: crop disease diagnosis, fertilizer recommendations,
weather-aware advice, water conservation, soil health suggestions, and government
scheme matching — powered by Gemini 2.5 Flash.

## Local setup

```bash
git clone <your-repo-url>
cd greenfarm-ai
pip install -r requirements.txt
cp .env.example .env   # then fill in GEMINI_API_KEY at minimum
```

Run locally:

```bash
export $(cat .env | xargs)   # or use python-dotenv / your OS's method
streamlit run app.py
```

Open `http://localhost:8501`.

## API keys

| Key | Required | Where to get it |
|---|---|---|
| `GEMINI_API_KEY` | Yes | [Google AI Studio](https://aistudio.google.com/apikey) |
| `WEATHER_API_KEY` | No — falls back to mock data | [OpenWeatherMap](https://openweathermap.org/api) |
| `SOIL_API_KEY` | No — falls back to manual input | Your soil data provider (e.g. ISRIC SoilGrids, or a national soil-health-card API) |

## Deployment Option 1 — Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select repo/branch → set main file to `app.py`.
3. Under **Advanced settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   GEMINI_MODEL = "gemini-2.5-flash"
   WEATHER_API_KEY = "your_key_here"   # optional
   SOIL_API_KEY = "your_key_here"      # optional
   ```
4. Deploy. `config.py` reads from `st.secrets` automatically.

## Deployment Option 2 — Google Cloud Run

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/greenfarm-ai

# Deploy
gcloud run deploy greenfarm-ai \
  --image gcr.io/YOUR_PROJECT_ID/greenfarm-ai \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here,GEMINI_MODEL=gemini-2.5-flash \
  --set-env-vars WEATHER_API_KEY=your_key_here \
  --set-env-vars SOIL_API_KEY=your_key_here
```

Cloud Run gives you autoscaling, a custom domain, and better control over
memory/CPU — worth it once you move past prototyping.

## Project structure

```
greenfarm-ai/
├── app.py                    # Streamlit UI — 6 tabs
├── config.py                 # Secrets/env loader
├── llm/gemini_client.py      # Gemini 2.5 Flash wrapper (text + vision)
├── services/
│   ├── weather_service.py    # OpenWeatherMap wrapper, mock fallback
│   ├── soil_service.py       # Soil API wrapper, manual-input fallback
│   └── schemes_data.py       # Static govt scheme dataset
├── requirements.txt
├── Dockerfile
└── .streamlit/config.toml    # Theme
```

## Notes

- All AI outputs are illustrative advisory content — the footer in the app
  reminds users to verify with a local agriculture officer before acting.
- Swap `services/schemes_data.py` for a live government open-data API call
  when one becomes available for your target state.
- To add more crops or diseases, no code changes are needed — Gemini reasons
  over open-ended input, unlike a fixed lookup table.
