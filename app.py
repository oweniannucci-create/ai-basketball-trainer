import streamlit as st
from groq import Groq
from datetime import datetime
import random
import time

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# SESSION STATE
# ----------------------------
if "workouts" not in st.session_state:
    st.session_state.workouts = []

if "generated_workout" not in st.session_state:
    st.session_state.generated_workout = None

if "focus" not in st.session_state:
    st.session_state.focus = ""

if "time" not in st.session_state:
    st.session_state.time = "60 min"

if "court" not in st.session_state:
    st.session_state.court = "Half Court"

if "energy" not in st.session_state:
    st.session_state.energy = 5

if "partner" not in st.session_state:
    st.session_state.partner = "No"

if "injury" not in st.session_state:
    st.session_state.injury = ""

# ----------------------------
# DATA
# ----------------------------
bible_verses = [
    "Philippians 4:13 — I can do all things through Christ who strengthens me.",
    "Isaiah 40:31 — Those who hope in the Lord will renew their strength.",
    "Proverbs 3:5 — Trust in the Lord with all your heart.",
    "Joshua 1:9 — Be strong and courageous."
]

quotes = [
    "Greatness is built when no one is watching.",
    "Discipline beats motivation every time.",
    "You don’t rise to talent, you fall to effort.",
    "Comfort kills progress."
]

# ----------------------------
# TABS
# ----------------------------
home, workout, history = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================================================
# HOME TAB (CLEAN)
# =========================================================
with home:
    st.title("🏀 D1 AI TRAINER")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.markdown("---")

    st.subheader("🔥 Build Your Workout")

    st.session_state.focus = st.text_input("🎯 Focus (shooting, handles, finishing etc.)")

    st.session_state.time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    st.session_state.court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])
    st.session_state.energy = st.slider("⚡ Energy", 1, 10, 5)

    st.session_state.partner = st.selectbox("🤝 Partner?", ["No", "Yes"])
    st.session_state.injury = st.text_input("🦵 Injury / soreness (optional)")

    if st.button("🔥 GENERATE WORKOUT"):

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        prompt = f"""
You are an elite D1 basketball trainer.

Build a structured basketball workout.

PLAYER:
Focus: {st.session_state.focus}
Time: {st.session_state.time}
Court: {st.session_state.court}
Energy: {st.session_state.energy}/10
Partner: {st.session_state.partner}
Injury: {st.session_state.injury}

RULES:
- If partner = Yes → include 1v1 / reaction drills
- If injury → reduce jumping + include recovery/mobility
- Must include sets, reps, and timing
- Must feel like real D1 training

FORMAT:
WARM-UP
SKILL WORK
PRESSURE DRILLS
GAME SIMULATION
FINISHER
COACHING NOTES
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        workout_text = response.choices[0].message.content

        st.session_state.generated_workout = workout_text

        st.session_state.workouts.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "focus": st.session_state.focus,
            "workout": workout_text
        })

        st.success("Workout Created ✔")
        st.info("👉 Go to the Workout tab to view your plan")

# =========================================================
# WORKOUT TAB (BOXED SECTIONS)
# =========================================================
with workout:
    st.title("🏀 YOUR D1 WORKOUT")

    workout = st.session_state.generated_workout

    if not workout:
        st.info("Generate a workout from the Home tab.")
    else:

        sections = {
            "WARM-UP": "",
            "SKILL WORK": "",
            "PRESSURE DRILLS": "",
            "GAME SIMULATION": "",
            "FINISHER": "",
            "COACHING NOTES": ""
        }

        current = None

        for line in workout.split("\n"):
            upper = line.upper()

            if "WARM" in upper:
                current = "WARM-UP"
            elif "SKILL" in upper:
                current = "SKILL WORK"
            elif "PRESSURE" in upper:
                current = "PRESSURE DRILLS"
            elif "GAME" in upper:
                current = "GAME SIMULATION"
            elif "FINISH" in upper:
                current = "FINISHER"
            elif "COACH" in upper:
                current = "COACHING NOTES"

            if current:
                sections[current] += line + "\n"

        for title, content in sections.items():
            with st.container():
                st.markdown(f"### 🧱 {title}")
                st.text(content.strip())
                st.markdown("---")

        st.info(random.choice(quotes))

# =========================================================
# HISTORY TAB
# =========================================================
with history:
    st.title("📊 Workout History")

    if len(st.session_state.workouts) == 0:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.workouts):
            with st.expander(f"{w['time']} — {w['focus']}"):
                st.text(w["workout"])