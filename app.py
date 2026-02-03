import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time

# --- BATTLEGROUNDS COMMAND CONFIG ---
st.set_page_config(page_title="PUBG | Tactical Scout", page_icon="🪂", layout="wide")

# --- HIGH-END TACTICAL CSS (The "Secret Sauce") ---
st.markdown("""
    <style>
    /* Background and Global Font */
    .stApp {
        background: linear-gradient(rgba(12, 15, 18, 0.9), rgba(12, 15, 18, 0.9)), 
                    url("https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/578080/841ea38bc58cabb70aef65365cf50bc2d79329d9/header.jpg?t=1764817633");
        background-size: cover;
        color: #f2a900;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Tactical Input Cards */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(26, 30, 36, 0.85);
        border: 1px solid #444;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Input Fields Customization */
    input {
        background-color: #0c0f12 !important;
        color: #f2a900 !important;
        border: 1px solid #f2a900 !important;
        font-weight: bold;
    }

    /* The "Air Drop" Deploy Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #f2a900 0%, #bf8600 100%);
        color: #0c0f12;
        font-weight: 900;
        font-size: 24px;
        border: 2px solid #0c0f12;
        border-radius: 5px;
        height: 3.5em;
        text-transform: uppercase;
        letter-spacing: 3px;
        transition: 0.4s all;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(242, 169, 0, 0.6);
        color: #fff;
    }

    /* Custom Header Style */
    .pubg-header {
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #f2a900;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Assets
@st.cache_resource
def load_assets():
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

model, scaler = load_assets()

# --- TOP PROMOTIONAL HEADER ---
st.markdown("""
    <div class="pubg-header">
        <h1 style="margin:0; font-size: 50px; letter-spacing: 5px;">PUBG SCOUT TERMINAL</h1>
        <p style="color: #8b949e; letter-spacing: 2px;">IDENTIFYING THE PRO</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: MISSION BRIEFING ---
st.sidebar.image("https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/578080/841ea38bc58cabb70aef65365cf50bc2d79329d9/header.jpg?t=1764817633", use_container_width=True)

st.sidebar.warning("⚠️ **MISSION BRIEFING**")
st.sidebar.write("""
    Enter player stats gathered from the latest match. 
    Our **Logistic Intelligence Engine** will analyze combat efficiency 
    and survival probability.
""")

# --- GRID LAYOUT FOR INPUTS ---
st.markdown("### STATS INPUT")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("⚔️ Combat")
    kills = st.number_input("Confirmed Kills", 0, 100, 5)
    headshots = st.number_input("Headshot Finishes", 0, 50, 1)

with col2:
    st.subheader("🩹 Support")
    revives = st.number_input("Squad Revives", 0, 15, 1)
    heals = st.number_input("First Aid Kits", 0, 30, 2)

with col3:
    st.subheader("🏃 Movement")
    dist = st.number_input("Walk Dist (m)", 0, 15000, 1200)
    boosts = st.number_input("Energy Drinks", 0, 30, 2)

with col4:
    st.subheader("🎒 Loot")
    weap = st.number_input("Weapons Picked", 0, 50, 4)
    damage = st.number_input("Total Damage", 0, 10000, 450)

st.markdown("<br>", unsafe_allow_html=True)

# --- EXECUTION ---
if st.button("RUN TACTICAL EVALUATION"):
    with st.spinner('📡 ANALYZING BATTLEFIELD TELEMETRY...'):
        time.sleep(1.5) # Fake "processing" for effect
    
    # Arrange data
    raw_data = np.array([[kills, damage, boosts, heals, dist, weap, revives, headshots]])
    scaled_data = scaler.transform(raw_data)
    
    # Predict
    prob = model.predict_proba(scaled_data)[0][1] * 100
    prediction = model.predict(scaled_data)[0]
    
    # RESULT INTERFACE
    if prediction == 1:

        banner_color = "#f2a900"
        text_color = "#000"
        title = "WINNER WINNER CHICKEN DINNER!"
        verdict = "PRO LEAGUE CANDIDATE"
    else:
        banner_color = "#ff4b4b"
        text_color = "#fff"
        title = "MISSION FAILED"
        verdict = "RE-TRAINING REQUIRED: AMATEUR STATUS"

    st.markdown(f"""
        <div style="background: {banner_color}; padding: 30px; border-radius: 10px; text-align: center; border: 4px solid #fff;">
            <h1 style="color: {text_color}; margin:0; font-size: 40px;">{title}</h1>
            <h2 style="color: {text_color}; margin:0; letter-spacing: 5px;">{verdict}</h2>
            <p style="color: {text_color}; font-size: 25px; font-weight: bold; margin-top: 10px;">SCOUT CONFIDENCE: {prob:.1f}%</p>
        </div>
    """, unsafe_allow_html=True)

    # Tactical Radar Chart (using Bar for simplicity in Streamlit)
    st.markdown("### 📈 PERFORMANCE RADAR")
    chart_data = pd.DataFrame({
        'Category': ['Aggression', 'Accuracy', 'Team Support', 'Survival'],
        'Value': [(kills*10), (headshots*20), (revives*15), (dist/100)]
    }).set_index('Category')
    st.bar_chart(chart_data)


st.markdown("<p style='text-align:center; color:#555;'>PUBG Scout v2.5 | Authorized by E-Sports Command</p>", unsafe_allow_html=True)