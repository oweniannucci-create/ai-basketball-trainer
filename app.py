import streamlit as st
from groq import Groq
from datetime import datetime
import random

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# STATE
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "preset" not in st.session_state:
    st.session_state.preset = ""

if "archetype" not in st.session_state:
    st.session_state.archetype = "Kobe (Mamba Mentality)"

if "workout" not in st.session_state:
    st.session_state.workout = ""

if "tab" not in st.session_state:
    st.session_state.tab = "home"

# ----------------------------
# DATA
# ----------------------------
quotes = [
    "Discipline beats motivation.",
    "Greatness is earned in silence.",
    "Comfort kills progress."
]

# ----------------------------
# TABS
# ----------------------------
home, build, result, history = st.tabs(
    ["🏠 Home", "🏀 Build", "📋 Workout", "📊 History"]
)

# =========================================================
# HOME
# =========================================================
with home:
    st.title("🏀 D1 AI TRAINER")

    st.subheader("⚡ Quick Presets")

    c1, c2, c3 = st.columns(3)

    if c1.button("🔥 Scoring"):
        st.session_state.preset = "Scoring Focus"
        st.success("Scoring preset selected")

    if c2.button("🎯 Shooting"):
        st.session_state.preset = "Shooting Focus"
        st.success("Shooting preset selected")

    if c3.button("💪 Explosiveness"):
        st.session_state.preset = "Explosiveness Focus"
        st.success("Explosiveness preset selected")

    st.divider()

    st.subheader("👤 Archetype (Affects workout style)")

    st.session_state.archetype = st.selectbox(
        "Choose Player Style",
        ["Kobe (Mamba)", "Curry (Shooter)", "Ja Morant (Explosive)", "LeBron (All-Around)"]
    )

    st.info(f"Selected: {st.session_state.archetype}")

# =========================================================
# BUILD TAB
# =========================================================
with build:
    st.title("🏀 Build Your Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("Focus", value=st.session_state.preset)
        energy = st.slider("Energy", 1, 10, 5)

    with col2:
        difficulty = st.slider("Difficulty", 1, 10, 5)
        time = st.selectbox("Time", ["45 min", "60 min", "90 min"])

    court = st.selectbox("Court", ["Driveway", "Half Court", "Full Court"])

    partner = st.checkbox("🤝 Partner Available")

    partner_role = ""
    if partner:
        partner_role = st.selectbox(
            "Partner Role",
            ["Live Defender", "Rebounder", "1v1 Opponent"]
        )

    body = st.text_input("🦵 Body Status (sore, injured, tight?)")

    st.divider()

    if st.button("🔥 Generate Workout"):
        with st.spinner("Building elite D1 workout..."):

            prompt = f"""
You are an elite D1 basketball trainer.

Player:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Court: {court}
Archetype: {st.session_state.archetype}
Partner: {partner}
Partner Role: {partner_role}
Body: {body}

RULES:
- If sore/injured → reduce impact drills
- If partner → add live reads + competition
- Must include detailed dynamic warm-up
- Must include pressure + game simulation

FORMAT EXACTLY:
Warm-Up
Dynamic Stretching
Skill Work
Pressure Work
Live Read Drill
Game Simulation
"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an elite basketball trainer."},
                    {"role": "user", "content": prompt}
                ]
            )

            output = response.choices[0].message.content

            st.session_state.workout = output
            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M"),
                "focus": focus,
                "workout": output
            })

            st.success("Workout Created 🔥 Go to Workout tab")
            st.rerun()

# =========================================================
# RESULT TAB (CLEAN CARDS)
# =========================================================
with result:
    st.title("📋 Your Workout")

    if not st.session_state.workout:
        st.warning("No workout yet")
    else:
        sections = st.session_state.workout.split("\n")

        for line in sections:
            if line.strip() != "":
                st.container().markdown(
                    f"""
                    <div style="
                        padding:12px;
                        margin-bottom:10px;
                        border-radius:10px;
                        background-color:#111;
                        border:1px solid #333;
                        color:white;
                    ">
                    {line}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()
        st.info(random.choice(quotes))

# =========================================================
# HISTORY TAB
# =========================================================
with history:
    st.title("📊 History")

    for w in reversed(st.session_state.history):
        with st.container():
            st.markdown(f"### 🕒 {w['time']}")
            st.write(f"**Focus:** {w['focus']}")

            st.text_area(
                "Workout",
                w.get("workout", ""),
                height=200
            )

            st.divider()