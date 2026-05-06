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
# TAB LAYOUT
# ----------------------------
home, workout_tab, history_tab, plan_tab = st.tabs([
    "🏠 Home", "🏀 Workout", "📊 History", "📅 Weekly Plan"
])

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.markdown("## 🔥 Build Your Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("🎯 What are you working on today?")
        time = st.selectbox("⏱ Time Available", ["45 min", "60 min", "90 min"])
        court = st.selectbox("🏀 Court Type", ["Driveway", "Half Court", "Full Court"])

    with col2:
        energy = st.slider("⚡ Energy Level", 1, 10, 5)
        struggle = st.text_input("📉 Struggle (optional)")
        body = st.text_input("🦵 Body status (sore, tight, pain?)")

    def build_workout():
        prompt = f"""
You are an elite D1 basketball trainer.

Create a structured basketball workout.

PLAYER INFO:
Focus: {focus}
Time: {time}
Court: {court}
Energy: {energy}/10
Struggle: {struggle}
Body Status: {body}

RULES:
- If sore or injured, adjust intensity
- Must include LIVE READ drill
- Must include pressure situations
- Must feel like real college training

FORMAT EXACTLY:
Warm-Up:
Skill Work:
Pressure Work:
Game Simulation:
Challenge:
Coaching Cues:
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    if st.button("🔥 Build Workout"):
        with st.spinner("Building your D1 workout..."):

            workout = build_workout()

            st.session_state.workout = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "workout": workout
            }

            st.session_state.history.append(st.session_state.workout)

            st.success("Workout created! Go to Workout tab 👇")

# =========================================================
# WORKOUT TAB (CLEAN CARD BREAKDOWN)
# =========================================================
with workout_tab:

    st.title("🏀 Your D1 Workout")

    if not st.session_state.workout:
        st.info("No workout yet. Go to Home and build one.")
    else:

        w = st.session_state.workout["workout"]

        def extract_section(title, text):
            try:
                return text.split(title + ":")[1].split("\n")[0].strip()
            except:
                return "Not generated properly"

        sections = {
            "🔥 Warm-Up": "Warm-Up",
            "🏀 Skill Work": "Skill Work",
            "⚡ Pressure Work": "Pressure Work",
            "🎮 Game Simulation": "Game Simulation",
            "🏆 Challenge": "Challenge",
            "🧠 Coaching Cues": "Coaching Cues"
        }

        st.markdown("## 🧱 Workout Breakdown")

        for label, key in sections.items():

            st.container().markdown(f"""
### {label}

{extract_section(key, w)}
""")

        st.markdown("---")

        st.info(random.choice(quotes))

        st.download_button(
            "⬇ Download Workout",
            w,
            file_name="d1_workout.txt"
        )

# =========================================================
# HISTORY TAB
# =========================================================
with history_tab:

    st.title("📊 Workout History")

    if not st.session_state.history:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.write(f"**Focus:** {w['focus']}")
                st.info(w["workout"])
                st.markdown("---")

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plan_tab:

    st.title("📅 Weekly Training Plan")

    goal = st.text_input("What is your weekly goal?")

    if st.button("Generate Weekly Plan"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite basketball trainer."},
                {"role": "user", "content": f"Create a 7-day training plan for: {goal}"}
            ]
        )

        plan = response.choices[0].message.content

        st.write(plan)

        st.download_button(
            "⬇ Download Plan",
            plan,
            file_name="weekly_plan.txt"
        )

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(random.choice(quotes))