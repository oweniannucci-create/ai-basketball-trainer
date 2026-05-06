import streamlit as st
from groq import Groq
from datetime import datetime
import random

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = ""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = {}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "home"

if "workout_output" not in st.session_state:
    st.session_state.workout_output = ""

if "preset" not in st.session_state:
    st.session_state.preset = ""

if "archetype" not in st.session_state:
    st.session_state.archetype = "Kobe"

# ensure user history exists
def get_user_history():
    user = st.session_state.user
    if user not in st.session_state.history:
        st.session_state.history[user] = []
    return st.session_state.history[user]

# =========================
# LOGIN
# =========================
if not st.session_state.logged_in:
    st.title("🏀 D1 AI Trainer Login")

    name = st.text_input("Enter your name")

    if st.button("Enter"):
        if name.strip() != "":
            st.session_state.user = name.strip()
            st.session_state.logged_in = True
            get_user_history()
            st.rerun()

    st.stop()

# =========================
# DATA
# =========================
bible = [
    "Philippians 4:13 — I can do all things through Christ.",
    "Isaiah 40:31 — Renewed strength.",
    "Joshua 1:9 — Be strong and courageous."
]

quotes = [
    "Discipline > Motivation",
    "Greatness is built alone",
    "Comfort kills progress"
]

# =========================
# SIDEBAR NAV
# =========================
st.sidebar.title(f"👤 {st.session_state.user}")

if st.sidebar.button("🏠 Home"):
    st.session_state.active_tab = "home"
if st.sidebar.button("🏀 Workout"):
    st.session_state.active_tab = "workout"
if st.sidebar.button("📊 History"):
    st.session_state.active_tab = "history"

# =========================
# HOME
# =========================
if st.session_state.active_tab == "home":
    st.title("🏀 D1 AI Trainer")

    st.info(random.choice(bible))

    st.subheader("⚡ Quick Setup")

    st.session_state.preset = st.selectbox(
        "Workout Focus",
        ["Scoring", "Shooting", "Explosiveness", "Defense", "Handles"]
    )

    st.session_state.archetype = st.selectbox(
        "Player Style",
        ["Kobe", "Curry", "Ja Morant", "LeBron"]
    )

    if st.button("🔥 Build Workout"):
        st.session_state.active_tab = "workout"
        st.rerun()

# =========================
# WORKOUT TAB
# =========================
if st.session_state.active_tab == "workout":

    st.title("🏀 Build Your D1 Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("Focus", value=st.session_state.preset)
        energy = st.slider("Energy", 1, 10, 5)
        difficulty = st.slider("Difficulty", 1, 10, 5)

    with col2:
        time = st.selectbox("Time", ["45 min", "60 min", "90 min"])
        court = st.selectbox("Court", ["Driveway", "Half Court", "Full Court"])
        partner = st.selectbox("Partner?", ["No", "Yes"])
        injury = st.text_input("Body Status (sore/injured/etc)")

    if st.button("🔥 Generate Workout"):

        progress = st.progress(0)

        prompt = f"""
You are a D1 basketball trainer.

PLAYER:
Focus: {focus}
Energy: {energy}
Difficulty: {difficulty}
Time: {time}
Court: {court}
Archetype: {st.session_state.archetype}
Partner: {partner}
Body: {injury}

RULES:
- If injured/sore, reduce intensity and add recovery
- If partner = yes, include competitive drills
- Include sets, reps, and timed work
- Include LIVE READ drill

FORMAT:
Warm-Up
Skill Work
Pressure
Game Simulation
Challenge
"""

        progress.progress(30)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        progress.progress(80)

        output = response.choices[0].message.content

        st.session_state.workout_output = output

        st.session_state.history[st.session_state.user].append({
            "time": datetime.now().strftime("%H:%M"),
            "focus": focus,
            "workout": output
        })

        progress.progress(100)

        st.session_state.active_tab = "workout"
        st.success("Workout Created 🔥 Scroll down")
        st.rerun()

    # =========================
    # DISPLAY WORKOUT CLEAN
    # =========================
    if st.session_state.workout_output:

        st.markdown("## 🧱 Your D1 Workout")

        sections = st.session_state.workout_output.split("\n\n")

        for s in sections:
            if s.strip():
                st.markdown(f"""
                <div style="
                    padding:15px;
                    border-radius:12px;
                    background:#111;
                    margin-bottom:10px;
                    border:1px solid #333;
                ">
                {s}
                </div>
                """, unsafe_allow_html=True)

        st.info(random.choice(quotes))

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout_output,
            file_name="d1_workout.txt"
        )

# =========================
# HISTORY
# =========================
if st.session_state.active_tab == "history":

    st.title("📊 Workout History")

    history = get_user_history()

    if not history:
        st.info("No workouts yet")
    else:
        for w in reversed(history):
            st.markdown(f"### 🕒 {w['time']}")

            st.markdown(f"""
            <div style="padding:10px;border:1px solid #444;border-radius:10px;">
            <b>Focus:</b> {w['focus']}<br><br>
            <pre style="white-space:pre-wrap">{w['workout']}</pre>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")