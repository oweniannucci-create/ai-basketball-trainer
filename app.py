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
# SESSION STATE
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "workout" not in st.session_state:
    st.session_state.workout = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🏠 Home"

if "focus" not in st.session_state:
    st.session_state.focus = ""

# ----------------------------
# DATA
# ----------------------------
quotes = [
    "Discipline beats motivation every time.",
    "Greatness is built in silence.",
    "You don’t rise to talent, you fall to effort.",
    "Comfort kills progress."
]

# ----------------------------
# TABS
# ----------------------------
home, workout, history = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.caption("Build like a college hooper. Train like a pro.")

    st.markdown("---")

    # ----------------------------
    # INPUTS
    # ----------------------------
    focus = st.text_input("🎯 What are you working on today?", value=st.session_state.focus)

    time = st.selectbox("⏱ Time Available", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court Type", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("⚡ Energy Level", 1, 10, 6)

    partner = st.radio("🤝 Partner Available?", ["No", "Yes"])

    body = st.text_input("🦵 Body Status (sore / tight / pain / healthy)")

    st.markdown("---")

    # ----------------------------
    # BUILD WORKOUT BUTTON
    # ----------------------------
    if st.button("🔥 BUILD D1 WORKOUT"):

        st.session_state.focus = focus

        prompt = f"""
You are an elite D1 basketball trainer.

Create a structured workout.

PLAYER INFO:
Focus: {focus}
Time: {time}
Court: {court}
Energy: {energy}/10
Partner: {partner}
Body Status: {body}

RULES:
- If partner = Yes → include 1v1 / live defense drills
- If body = sore/pain → include recovery + mobility focus
- Must include LIVE READ drill
- Must feel like college-level training

FORMAT:
Warm-Up
Skill Work
Pressure Work
Game Simulation
Challenge
"""

        with st.spinner("Building your D1 workout..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a D1 basketball trainer."},
                    {"role": "user", "content": prompt}
                ]
            )

            workout_text = response.choices[0].message.content

            st.session_state.workout = workout_text

            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "workout": workout_text
            })

            # switch tab
            st.session_state.active_tab = "🏀 Workout"

            st.success("Workout created! Go to Workout tab 👇")

# =========================================================
# WORKOUT TAB (CLEAN CARD UI)
# =========================================================
with workout:

    st.title("🏀 Your D1 Workout")

    if not st.session_state.workout:
        st.info("No workout yet. Go to Home and build one.")
    else:

        workout = st.session_state.workout

        # Split into sections
        sections = workout.split("\n")

        st.markdown("### 🧱 Training Plan")

        box = ""
        for line in sections:
            if line.strip() == "" or any(x in line.lower() for x in ["warm", "skill", "pressure", "game", "challenge"]):
                if box:
                    st.markdown(f"""
                    <div style="
                        padding:15px;
                        border-radius:10px;
                        background:#111;
                        margin-bottom:10px;
                        border:1px solid #333;">
                        {box}
                    </div>
                    """, unsafe_allow_html=True)
                    box = ""
                box = f"**{line}**"
            else:
                box += f"<br>{line}"

        if box:
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background:#111;
                margin-bottom:10px;
                border:1px solid #333;">
                {box}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.info(random.choice(quotes))

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout,
            file_name="d1_workout.txt"
        )

# =========================================================
# HISTORY TAB
# =========================================================
with history:

    st.title("📊 Workout History")

    if len(st.session_state.history) == 0:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.history):
            st.markdown(f"""
            <div style="
                padding:10px;
                border-radius:10px;
                background:#0f0f0f;
                border:1px solid #333;
                margin-bottom:10px;">
                <b>{w['time']}</b><br>
                <b>Focus:</b> {w['focus']}<br><br>
                <pre style="white-space:pre-wrap">{w['workout']}</pre>
            </div>
            """, unsafe_allow_html=True)