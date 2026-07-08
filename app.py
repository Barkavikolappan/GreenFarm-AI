"""
GreenFarm AI — Sustainable Agriculture Agent
Streamlit frontend + Gemini 2.5 Flash backend.
"""

import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr

from config import (
    APP_TITLE,
    DEFAULT_REGION,
    WEATHER_LIVE,
    SOIL_LIVE
)

from llm import gemini_client as ai
from services.weather_service import get_weather_summary
from services.schemes_data import SCHEME_CATALOG
from services.voiceip import tamil_voice_input
from services.voice import speak_tamil, speak_text
from translations import TEXT


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- LANGUAGE ----------------

language = st.sidebar.selectbox(
    "🌐 Language / மொழி / भाषा",
    [
        "English",
        "தமிழ்",
        "हिन्दी"
    ]
)


# Translation dictionary

T = TEXT[language]


# ---------------- TITLE ----------------

st.title(T["title"])

st.caption(
    "Sustainable Agriculture Agent — powered by Gemini 2.5 Flash"
)


# ---------------- API STATUS ----------------

if not WEATHER_LIVE:
    st.sidebar.info(
        "Weather API key not set — using mock weather data."
    )


if not SOIL_LIVE:
    st.sidebar.info(
        "Soil API key not set — enter soil test values manually."
    )
# ---------------- 1. DISEASE DIAGNOSIS ----------------

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
background:#eef7ee;
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#14532d,#166534,#15803d);
color:white;
}

section[data-testid="stSidebar"] *{
color:white;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] *{
color:#b45309 !important;
font-weight:600;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] input{
color:#b45309 !important;
-webkit-text-fill-color:#b45309 !important;
font-weight:600 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="input"] *{
color:#b45309 !important;
-webkit-text-fill-color:#b45309 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
background:white;
border-radius:8px;
}

section[data-testid="stSidebar"] ul[role="listbox"]{
background:white;
}

section[data-testid="stSidebar"] ul[role="listbox"] li{
color:#14532d !important;
}

.hero{
background:linear-gradient(135deg,#14532d,#16a34a);
padding:35px;
border-radius:18px;
color:white;
box-shadow:0px 10px 25px rgba(0,0,0,.2);
margin-bottom:20px;
}

.card{
background:#fdf9f0;
padding:22px;
border-radius:16px;
box-shadow:0px 5px 20px rgba(0,0,0,.08);
margin-bottom:20px;
color:#14532d;
}

.card *{
color:#14532d;
}

.metric-card{
background:#f7fff7;
padding:18px;
border-radius:15px;
border-left:6px solid #22c55e;
box-shadow:0px 3px 12px rgba(0,0,0,.08);
text-align:center;
}

.big-title{
font-size:42px;
font-weight:bold;
}

.subtitle{
font-size:18px;
opacity:.9;
}

.stButton>button{
background:#16a34a;
color:white;
border:none;
border-radius:10px;
padding:10px 25px;
font-weight:bold;
}

.stButton>button:hover{
background:#15803d;
}

hr{
margin-top:35px;
margin-bottom:35px;
}

</style>
""",unsafe_allow_html=True)

# ---------------- Hero ----------------

st.markdown("""
<div class="hero">

<div class="big-title">
🌿 GreenFarm AI
</div>

<div class="subtitle">
AI Powered Smart Agriculture Assistant
</div>

</div>
""",unsafe_allow_html=True)

# ---------------- Sidebar ----------------

st.sidebar.title("🌾 GreenFarm AI")

page=st.sidebar.radio(
"Navigation",
[
"🏠 Dashboard",
"🔬 Disease Diagnosis",
"🧪 Fertilizer",
"🌦 Weather",
"💧 Water",
"🌱 Soil Health",
"🏛 Government Schemes"
]
)

st.sidebar.markdown("---")

if not WEATHER_LIVE:
    st.sidebar.warning("⚠ Weather API not configured")

if not SOIL_LIVE:
    st.sidebar.warning("⚠ Soil API not configured")

# ---------------- Dashboard ----------------

if page=="🏠 Dashboard":

    st.markdown("## Farm Overview")

    c1,c2,c3,c4=st.columns(4)

    c1.metric("🌾 Crops","6")
    c2.metric("🌦 Weather","Live")
    c3.metric("🤖 AI","Gemini")
    c4.metric("🌱 Soil","Healthy")

    st.markdown("")

    a,b=st.columns([2,1])

    with a:

        st.markdown("""
        <div class="card">

        <h3>Welcome 👋</h3>

        GreenFarm AI helps farmers with

        ✔ Disease Detection

        ✔ Fertilizer Recommendation

        ✔ Weather Advisory

        ✔ Water Planning

        ✔ Soil Health

        ✔ Government Schemes

        </div>
        """,unsafe_allow_html=True)

    with b:

        st.markdown("""
        <div class="card">

        🌱 Smart Farming

        📈 AI Analytics

        🌧 Live Weather

        💧 Irrigation

        🚜 Sustainable Agriculture

        </div>
        """,unsafe_allow_html=True)

# ---------------- Disease ----------------

# ---------------- Disease ----------------

# ---------------- Disease Diagnosis ----------------

elif page == "🔬 Disease Diagnosis":

    st.markdown(f"## 🔬 {T['disease']}")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    left, right = st.columns(2)

    uploaded_img = None
    symptoms = ""
    crop = ""


    with left:

        crop_names_ta = {

            "தக்காளி": "Tomato",
            "நெல்": "Rice",
            "பருத்தி": "Cotton",
            "கோதுமை": "Wheat",
            "மிளகாய்": "Chili",
            "கரும்பு": "Sugarcane"

        }

        crop_names_hi = {

            "टमाटर": "Tomato",
            "चावल": "Rice",
            "कपास": "Cotton",
            "गेहूं": "Wheat",
            "मिर्च": "Chili",
            "गन्ना": "Sugarcane"

        }


        # Tamil / Hindi / English crop selection

        if language == "தமிழ்":

            selected_crop = st.selectbox(
                "🌾 பயிரை தேர்வு செய்யவும்",
                list(crop_names_ta.keys())
            )

            crop = crop_names_ta[selected_crop]


        elif language == "हिन्दी":

            selected_crop = st.selectbox(
                "🌾 फसल चुनें",
                list(crop_names_hi.keys())
            )

            crop = crop_names_hi[selected_crop]


        else:

            crop = st.selectbox(
                "🌾 Select Crop",
                list(crop_names_ta.values())
            )


        voice_labels = {
            "தமிழ்": ("🎤 Speak in Tamil", "ta-IN"),
            "हिन्दी": ("🎤 हिंदी में बोलें", "hi-IN"),
            "English": ("🎤 Speak in English", "en-IN")
        }

        mic_label, recognize_lang = voice_labels.get(
            language, ("🎤 Speak", "en-IN")
        )

        st.write(f"### {mic_label}")


        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            format="wav",
            key="tamil_mic"
        )

        voice_text = ""


        if audio and "bytes" in audio:

            st.audio(audio["bytes"])  # 🔊 playback test — listen to what mic captured

            try:

                # audio["bytes"] is already real WAV data (confirmed via
                # RIFF/WAVE header), so just save it directly — no
                # WebM-to-WAV conversion needed.
                with open("voice.wav", "wb") as f:
                    f.write(audio["bytes"])

            except Exception as conv_err:

                st.error(
                    f"❌ Could not save recorded audio: {conv_err}"
                )

            else:

                recognizer = sr.Recognizer()


                with sr.AudioFile("voice.wav") as source:

                    audio_data = recognizer.record(source)


                try:

                    voice_text = recognizer.recognize_google(
                        audio_data,
                        language=recognize_lang
                    )

                    st.success("Voice Detected:")
                    st.write(voice_text)

                except Exception:

                    st.error(
                        "Could not recognize voice."
                    )


        symptoms = st.text_area(
            "📝 Describe Symptoms",
            value=voice_text,
            placeholder="Example: Yellow spots with brown edges..."
        )


    with right:

        uploaded_img = st.file_uploader(
            "📷 Upload Plant Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )


        if uploaded_img:

            st.image(
                uploaded_img,
                use_container_width=True
            )


    st.markdown("</div>", unsafe_allow_html=True)



    if st.button(
        "🔍 Analyze Disease",
        use_container_width=True
    ):


        if not symptoms and uploaded_img is None:

            st.warning(
                "Please upload an image or enter symptoms."
            )


        else:

            try:

                with st.spinner(
                    "🤖 Gemini AI is analyzing..."
                ):


                    img_bytes = None


                    if uploaded_img:

                        img_bytes = uploaded_img.read()


                    result = ai.diagnose_disease(

                        crop,

                        symptoms,

                        image_bytes=img_bytes,

                        language=language

                    )


                st.success(
                    "Diagnosis Completed"
                )


                c1, c2, c3 = st.columns(3)


                c1.metric(
                    "Disease",
                    result["disease_name"]
                )


                c2.metric(
                    "Confidence",
                    f"{result['confidence_percent']}%"
                )


                c3.metric(
                    "Severity",
                    result["severity"].capitalize()
                )


                st.markdown(
                    "### 📖 Explanation"
                )

                st.info(
                    result["explanation"]
                )


                # Tamil / Hindi Voice Output

                if language in ("தமிழ்", "हिन्दी"):

                    speak_button_label = (
                        "🔊 பதிலை கேளுங்கள்"
                        if language == "தமிழ்"
                        else "🔊 उत्तर सुनें"
                    )

                    if st.button(speak_button_label):

                        audio_path = speak_text(
                            result["explanation"],
                            language
                        )

                        st.audio(
                            audio_path,
                            format="audio/mp3"
                        )


                st.markdown(
                    "### 💊 Treatment"
                )


                for step in result["treatment_steps"]:

                    st.success(step)



                if result.get("prevention_tips"):

                    st.markdown(
                        "### 🌱 Prevention Tips"
                    )


                    for tip in result["prevention_tips"]:

                        st.warning(tip)



            except Exception as e:

                st.error(
                    f"❌ {e}"
                )
# ---------------- 2. FERTILIZER ----------------
# ---------------- Fertilizer ----------------
# ---------------- Fertilizer ----------------

elif page == "🧪 Fertilizer":

    st.markdown("## 🧪 Fertilizer Recommendation")


    c1, c2, c3 = st.columns(3)


    if language == "தமிழ்":

        crop_list = [
            "தக்காளி",
            "நெல்",
            "கோதுமை",
            "மக்காச்சோளம்",
            "வேர்க்கடலை"
        ]

    elif language == "हिन्दी":

        crop_list = [
            "टमाटर",
            "चावल",
            "गेहूं",
            "मक्का",
            "मूंगफली"
        ]

    else:

        crop_list = [
            "Tomato",
            "Rice",
            "Wheat",
            "Maize",
            "Groundnut"
        ]


    with c1:

        f_crop = st.selectbox(
            T["crop"],
            crop_list
        )


    with c2:

        f_stage = st.selectbox(
            "🌱 Growth Stage",
            [
                "Sowing",
                "Vegetative",
                "Flowering",
                "Fruiting"
            ]
        )


    with c3:

        f_area = st.number_input(
            "📏 Field Size (Acres)",
            min_value=0.1,
            value=1.0
        )


    st.markdown("### Soil Nutrients")


    n1, n2, n3 = st.columns(3)


    with n1:

        f_n = st.number_input(
            "Nitrogen (N)",
            value=180.0
        )


    with n2:

        f_p = st.number_input(
            "Phosphorus (P)",
            value=20.0
        )


    with n3:

        f_k = st.number_input(
            "Potassium (K)",
            value=110.0
        )



    if st.button(
        "🧪 Get Recommendation",
        use_container_width=True
    ):


        with st.spinner(
            "Calculating recommendation..."
        ):


            try:

                result = ai.recommend_fertilizer(
                    f_crop,
                    f_stage,
                    f_area,
                    f_n,
                    f_p,
                    f_k
                )


                m1, m2, m3 = st.columns(3)


                m1.metric(
                    "🌿 Urea",
                    f"{result['urea_kg']} kg"
                )


                m2.metric(
                    "🌾 DAP",
                    f"{result['dap_kg']} kg"
                )


                m3.metric(
                    "🪴 MOP",
                    f"{result['mop_kg']} kg"
                )


                st.markdown(
                    "### Application Notes"
                )


                for note in result["application_notes"]:

                    st.success(note)



                st.info(
                    f"Biofertilizer Tip: {result['biofertilizer_suggestion']}"
                )


            except Exception as e:

                st.error(
                    f"❌ {e}"
                )
# ---------------- 3. WEATHER ----------------
# ---------------- Weather ----------------

elif page=="🌦 Weather":

    st.markdown(f"## 🌦 {T.get('weather','Smart Weather Advisory')}")

    c1, c2 = st.columns(2)


    with c1:

        w_loc = st.text_input(
            "📍 Location",
            value=DEFAULT_REGION
        )


    with c2:

        if language == "தமிழ்":

            weather_crop_names = {
                "நெல்": "Rice",
                "தக்காளி": "Tomato",
                "பருத்தி": "Cotton",
                "வேர்க்கடலை": "Groundnut"
            }


            selected_crop = st.selectbox(
                "🌾 பயிரை தேர்வு செய்யவும்",
                list(weather_crop_names.keys())
            )


            w_crop = weather_crop_names[selected_crop]


        elif language == "हिन्दी":

            weather_crop_names = {
                "चावल": "Rice",
                "टमाटर": "Tomato",
                "कपास": "Cotton",
                "मूंगफली": "Groundnut"
            }


            selected_crop = st.selectbox(
                "🌾 फसल चुनें",
                list(weather_crop_names.keys())
            )


            w_crop = weather_crop_names[selected_crop]


        else:

            w_crop = st.selectbox(
                "🌾 Crop",
                [
                    "Rice",
                    "Tomato",
                    "Cotton",
                    "Groundnut"
                ]
            )


    if st.button(
        "🌦 Get Weather Advisory",
        use_container_width=True
    ):


        with st.spinner(
            "Fetching weather and generating AI advisory..."
        ):


            try:

                weather = get_weather_summary(w_loc)


                weather_summary = (
                    f"{weather['temperature_c']}°C, "
                    f"{weather['humidity_pct']}% humidity, "
                    f"{weather.get('conditions','Unknown')}, "
                    f"Rain Chance {weather.get('rain_chance_pct','0')}%"
                )


                result = ai.weather_advisory(
                    w_crop,
                    w_loc,
                    weather_summary,
                    language=language       # ⭐ Tamil support added
                )


                st.success(
                    "Weather Advisory Generated"
                )


                m1, m2, m3 = st.columns(3)


                m1.metric(
                    "🌡 Temperature",
                    f"{weather['temperature_c']}°C"
                )


                m2.metric(
                    "💧 Humidity",
                    f"{weather['humidity_pct']}%"
                )


                m3.metric(
                    "⚠ Risk",
                    result["risk_level"].capitalize()
                )


                st.markdown("---")


                st.markdown("### ☁ Current Weather")


                st.info(
                    f"""
📍 **Location:** {w_loc}

🌡 **Temperature:** {weather['temperature_c']}°C

💧 **Humidity:** {weather['humidity_pct']}%

🌤 **Condition:** {weather.get('conditions','Unknown')}

🌧 **Rain Chance:** {weather.get('rain_chance_pct','0')}%

📡 **Source:** {weather['source']}
"""
                )


                st.markdown("### 🚨 Alerts")


                for alert in result["alerts"]:

                    st.warning(alert)



                st.markdown("### 🧴 Best Spray Time")


                st.success(
                    result["best_spray_window"]
                )



                st.markdown("### 💧 Irrigation Advice")


                st.info(
                    result["irrigation_note"]
                )


            except Exception as e:

                st.error(f"❌ {e}")
# ---------------- 4. WATER CONSERVATION ----------------
# ---------------- Water Conservation ----------------

elif page=="💧 Water":

    st.markdown("## 💧 Smart Water Conservation")

    c1, c2, c3 = st.columns(3)

    with c1:
        wt_crop = st.selectbox(
            "🌾 Crop",
            [
                "Rice",
                "Tomato",
                "Sugarcane",
                "Cotton",
                "Groundnut"
            ]
        )

    with c2:
        wt_soil = st.selectbox(
            "🌱 Soil Type",
            [
                "Clay",
                "Loam",
                "Sandy"
            ]
        )

    with c3:
        wt_area = st.number_input(
            "📏 Field Size (Acres)",
            min_value=0.1,
            value=1.0,
            step=0.1
        )

    r1, r2 = st.columns(2)

    with r1:
        wt_rain = st.number_input(
            "🌧 Rainfall Last 7 Days (mm)",
            value=12.0
        )

    with r2:
        wt_method = st.selectbox(
            "🚿 Irrigation Method",
            [
                "Flood",
                "Drip",
                "Sprinkler",
                "None"
            ]
        )

    if st.button(
        "💧 Generate Water Plan",
        use_container_width=True
    ):

        with st.spinner("Calculating water conservation plan..."):

            try:

                result = ai.water_conservation_plan(
                    wt_crop,
                    wt_soil,
                    wt_area,
                    wt_rain,
                    wt_method
                )

                st.success("Water Conservation Plan Ready")

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "💦 Weekly Demand",
                        f"{result['weekly_water_demand_mm']} mm"
                    )

                with m2:
                    st.metric(
                        "📉 Water Deficit",
                        f"{result['irrigation_deficit_mm']} mm"
                    )

                with m3:
                    st.metric(
                        "🚰 Water Needed",
                        f"{result['estimated_water_needed_kilolitres']} kL"
                    )

                st.markdown("---")

                st.markdown("### 🚿 Recommended Irrigation")

                st.success(
                    result["recommended_method"]
                )

                st.markdown("### 🌱 Water Saving Tips")

                for tip in result["efficiency_tips"]:
                    st.info(tip)

            except Exception as e:

                st.error(f"❌ {e}")

# ---------------- 5. SOIL HEALTH ----------------
# ---------------- Soil Health ----------------

elif page=="🌱 Soil Health":

    st.markdown("## 🌱 AI Soil Health Analysis")

    c1, c2, c3 = st.columns(3)

    with c1:
        s_ph = st.number_input(
            "🧪 Soil pH",
            value=6.2,
            step=0.1
        )

    with c2:
        s_oc = st.number_input(
            "🌿 Organic Carbon (%)",
            value=0.4,
            step=0.1
        )

    with c3:
        s_texture = st.selectbox(
            "🌾 Soil Texture",
            [
                "Clay",
                "Loam",
                "Sandy",
                "Silty"
            ]
        )

    c4, c5 = st.columns(2)

    with c4:
        s_lastcrop = st.text_input(
            "🌾 Previous Crop",
            value="Rice"
        )

    with c5:
        s_years = st.number_input(
            "🔄 Years Without Crop Rotation",
            min_value=0,
            value=3
        )

    if st.button(
        "🌱 Analyze Soil",
        use_container_width=True
    ):

        with st.spinner("Analyzing soil using Gemini AI..."):

            try:

                result = ai.soil_health_analysis(
                    s_ph,
                    s_oc,
                    s_texture,
                    s_lastcrop,
                    s_years
                )

                st.success("Soil Analysis Completed")

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "🧪 Soil pH",
                        s_ph
                    )

                with m2:
                    st.metric(
                        "🌿 Organic Carbon",
                        f"{s_oc}%"
                    )

                with m3:
                    st.metric(
                        "📊 Status",
                        result["status"].capitalize()
                    )

                st.markdown("---")

                st.markdown("### 🔍 Soil Findings")

                for finding in result["findings"]:
                    st.info(finding)

                st.markdown("### 🌾 Crop Rotation")

                st.success(
                    result["rotation_suggestion"]
                )

                st.markdown("### 🌱 Soil Amendment")

                st.success(
                    result["amendment_suggestion"]
                )

            except Exception as e:

                st.error(f"❌ {e}")

# ---------------- 6. GOVT SCHEMES ----------------
# ---------------- Government Schemes ----------------

elif page=="🏛 Government Schemes":

    st.markdown("## 🏛 Government Agriculture Schemes")

    c1, c2, c3 = st.columns(3)

    with c1:
        g_state = st.selectbox(
            "📍 State",
            [
                "Tamil Nadu",
                "Punjab",
                "Maharashtra",
                "Karnataka",
                "Uttar Pradesh"
            ]
        )

    with c2:
        g_land = st.number_input(
            "🌾 Land Holding (Acres)",
            value=2.0,
            min_value=0.1
        )

    with c3:
        g_cat = st.selectbox(
            "👨‍🌾 Farmer Category",
            [
                "Small/Marginal",
                "Large",
                "Tenant"
            ]
        )

    g_interest = st.selectbox(
        "🎯 Primary Interest",
        [
            "Income support",
            "Irrigation subsidy",
            "Crop insurance",
            "Organic farming",
            "Equipment/machinery"
        ]
    )

    if st.button(
        "🔍 Find Eligible Schemes",
        use_container_width=True
    ):

        with st.spinner("Searching AI recommendations..."):

            try:

                result = ai.match_schemes(
                    g_state,
                    g_land,
                    g_cat,
                    g_interest,
                    SCHEME_CATALOG
                )

                st.success("Matching Schemes Found")

                st.info(result["eligibility_note"])

                catalog = {
                    s["name"]: s
                    for s in SCHEME_CATALOG
                }

                for match in result["matched_schemes"]:

                    scheme = catalog.get(match["name"])

                    with st.container(border=True):

                        st.subheader("🌿 " + match["name"])

                        if scheme:

                            st.write("**Description**")
                            st.write(scheme["desc"])

                            st.write("**Subsidy**")
                            st.success(scheme["subsidy"])

                            st.write("**Official Website**")
                            st.code(scheme["link"])

                        st.write("**Why Recommended**")
                        st.info(match["why_relevant"])

            except Exception as e:

                st.error(f"❌ {e}")

# ---------------- Footer ----------------

st.divider()

st.markdown(
"""
<center>

### 🌿 GreenFarm AI

Smart Agriculture Assistant powered by Gemini AI

Designed for Sustainable Farming 🚜🌱

</center>
""",
unsafe_allow_html=True
)