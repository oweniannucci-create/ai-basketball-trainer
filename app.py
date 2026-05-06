import streamlit as st
from groq import Groq
from datetime import datetime
import time
import random

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="D1 AI Trainer", layout="wide", page_icon="🏀")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# STYLE
# ----------------------------
st.markdown("""
<style>
.main {
    background-color: #0b0f1a;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "history" not in st.session_state:
    st.session_state.history = {}

if "workout" not in st.session_state:
    st.session_state.workout = None

# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.logged_in:
    st.title("🏀 D1 AI Trainer Login")

    name = st.text_input("Enter your name")

    if st.button("Enter Gym"):
        if name:
            st.session_state.user = name

            if name not in st.session_state.history:
                st.session_state.history[name] = []

            st.session_state.logged_in = True
            st.rerun()

    st.stop()

# ----------------------------
# NAVIGATION
# ----------------------------
tab = st.radio("Navigation", ["Home", "Workout", "History"], horizontal=True)

# ----------------------------
# BIBLE VERSE
# ----------------------------
verses = [
    "Philippians 4:13 — I can do all things through Christ.",
    "Isaiah 40:31 — They will run and not grow weary.",
    "Proverbs 3:5 — Trust the process.",
]

# =========================================================
# HOME
# =========================================================
if tab == "Home":

    st.markdown("## 🏀 D1 AI TRAINER")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📖 Daily Bible Verse")
    st.write(random.choice(verses))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔥 Ready to Train")
    st.write("Go to Workout tab → build your D1 workout")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# WORKOUT TAB
# =========================================================
if tab == "Workout":

    st.markdown("## 🏀 Build Your Workout")

    focus = st.text_input("🎯 What are you working on today?")
    struggle = st.text_input("📉 What are you struggling with?")
    energy = st.slider("⚡ Energy Level", 1, 10, 6)

    time_available = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    partner = st.selectbox(
        "🤝 Partner Type",
        ["No partner", "Rebounding partner", "Live defender partner"]
    )

    body = st.text_input("🦵 Body status (sore, tight, injury?)")

    # ----------------------------
    # GENERATE BUTTON
    # ----------------------------
    if st.button("🔥 Generate Workout"):

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        prompt = f"""
You are an elite NBA skill trainer.

Create a D1 basketball workout.

PLAYER:
Focus: {focus}
Struggle: {struggle}
Energy: {energy}/10
Time: {time_available}
Court: {court}
Partner: {partner}
Body: {body}

RULES:
- Adjust for injury/soreness if needed
- Include partner drills if partner exists
- Must include LIVE READ decision drill
- Must include sets, reps, or timed work
- Must be detailed and game realistic

FORMAT:

WARM-UP
SKILL WORK
PARTNER WORK (if any)
PRESSURE DRILLS
GAME SIMULATION
FINISHER
COACH NOTES
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a D1 basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        workout = response.choices[0].message.content

        # SAVE
        st.session_state.workout = workout
        st.session_state.history[st.session_state.user].append({
            "time": str(datetime.now()),
            "focus": focus,
            "workout": workout
        })

        st.success("Workout Created 💪")
        st.info("Go to Workout tab to view your plan")

# ----------------------------
# DISPLAY WORKOUT (FIXED)
# ----------------------------
if tab == "Workout" and st.session_state.workout:

    st.markdown("## 🧱 Your Training Plan")

    sections = st.session_state.workout.split("\n\n")

    for sec in sections:
        if sec.strip():
            st.markdown(f"""
            <div class="card">
            {sec}
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# HISTORY TAB
# =========================================================
if tab == "History":

    st.markdown("## 📊 Your Workouts")

    user_history = st.session_state.history.get(st.session_state.user, [])

    if not user_history:
        st.info("No workouts yet")
    else:
        for w in reversed(user_history):

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("🕒", w["time"])
            st.write("🎯", w["focus"])
            st.text_area("Workout", w["workout"], height=250, key=w["time"])
            st.markdown("</div>", unsafe_allow_html=True)