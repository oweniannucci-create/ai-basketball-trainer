import streamlit as st
from groq import Groq
from datetime import datetime
import random
import time

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# SESSION STATE SAFE INIT
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "workout" not in st.session_state:
    st.session_state.workout = None

if "history" not in st.session_state:
    st.session_state.history = {}

if "tab" not in st.session_state:
    st.session_state.tab = "home"

# =========================
# DATA
# =========================
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

# =========================
# LOGIN SYSTEM
# =========================
if st.session_state.user is None:
    st.title("🏀 D1 AI Trainer Login")

    username = st.text_input("Enter your name")

    if st.button("Enter Training Center"):
        if username.strip() != "":
            st.session_state.user = username.strip()

            if username not in st.session_state.history:
                st.session_state.history[username] = []

            st.rerun()
        else:
            st.warning("Enter a valid name")
    st.stop()

user = st.session_state.user

# =========================
# NAV TABS (CONTROLLED)
# =========================
home_tab, workout_tab, history_tab = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================
# HOME TAB
# =========================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.markdown("### 🏀 Build Your Workout")

    focus = st.text_input("What are you working on today?")
    time_available = st.selectbox("Time Available", ["45 min", "60 min", "90 min"])
    court = st.selectbox("Court Type", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("Energy Level", 1, 10, 5)
    struggle = st.text_input("What are you struggling with?")
    body = st.text_input("Body status (sore / injury / tight / none)")

    def build_workout():
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        prompt = f"""
You are an elite D1 basketball trainer.

Create a structured workout with:
- warmup
- skill work
- pressure drills
- game simulation
- challenge

PLAYER INFO:
Focus: {focus}
Time: {time_available}
Court: {court}
Energy: {energy}
Struggle: {struggle}
Body: {body}

IMPORTANT:
If body says sore or injury, reduce intensity and include recovery movements.

FORMAT EACH SECTION CLEARLY:
- include sets, reps, and timed work (seconds)
- explain how to do each drill
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    if st.button("🔥 Generate Workout"):
        with st.spinner("Building your D1 workout..."):
            workout = build_workout()

            st.session_state.workout = workout

            # save to history
            st.session_state.history[user].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "workout": workout
            })

            st.success("Workout created! Go to Workout tab 🏀")

            st.session_state.tab = "workout"
            st.rerun()

# =========================
# WORKOUT TAB (CLEAN UI BOXES)
# =========================
with workout_tab:
    st.title("🏀 Your D1 Workout")

    if not st.session_state.workout:
        st.info("No workout yet. Go generate one on Home.")
    else:
        sections = st.session_state.workout.split("\n")

        current_box = []
        section_title = "Workout"

        for line in sections:
            if any(keyword in line.lower() for keyword in ["warm", "skill", "pressure", "game", "challenge"]):
                if current_box:
                    with st.container():
                        st.markdown(f"### 🧱 {section_title}")
                        st.markdown("\n".join(current_box))
                        st.markdown("---")
                    current_box = []

                section_title = line.strip()

            current_box.append(line)

        if current_box:
            with st.container():
                st.markdown(f"### 🧱 {section_title}")
                st.markdown("\n".join(current_box))

        st.info(random.choice(quotes))

# =========================
# HISTORY TAB
# =========================
with history_tab:
    st.title("📊 Workout History")

    user_history = st.session_state.history.get(user, [])

    if len(user_history) == 0:
        st.info("No workouts yet.")
    else:
        for w in reversed(user_history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.markdown(w["workout"])
                st.markdown("---")