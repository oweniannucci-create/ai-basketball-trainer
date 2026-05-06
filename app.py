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
# LOGIN
# =========================
if st.session_state.user is None:
    st.title("🏀 D1 AI Trainer Login")

    username = st.text_input("Enter your name")

    if st.button("Enter Training Center"):
        if username.strip():
            st.session_state.user = username.strip()

            if username not in st.session_state.history:
                st.session_state.history[username] = []

            st.rerun()
        else:
            st.warning("Please enter a name")

    st.stop()

user = st.session_state.user

# =========================
# TABS
# =========================
home_tab, workout_tab, history_tab = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================
# HOME TAB
# =========================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.markdown("## 🏀 Build Your Workout")

    focus = st.text_input("What are you working on today?")
    struggle = st.text_input("What are you struggling with?")
    time_available = st.selectbox("Time Available", ["45 min", "60 min", "90 min"])
    court = st.selectbox("Court Type", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("Energy Level", 1, 10, 5)
    body = st.text_input("Body status (sore / injury / tight / none)")

    partner = st.selectbox(
        "Do you have a partner?",
        ["No partner", "Rebounding partner", "Live defender partner"]
    )

    # =========================
    # WORKOUT GENERATION
    # =========================
    def build_workout():
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        prompt = f"""
You are an elite D1 basketball trainer.

PLAYER INFO:
Focus: {focus}
Struggle: {struggle}
Time: {time_available}
Court: {court}
Energy: {energy}
Body: {body}
Partner: {partner}

RULES:
- Adapt everything to focus and struggle
- If injury/sore → reduce intensity + add recovery work
- Partner must change drill structure
- Include sets, reps, and timed work (seconds)
- Explain HOW to do each drill

FORMAT:

WARM-UP:
- detailed movement prep

SKILL WORK:
- structured drills with reps + coaching cues

PARTNER WORK:
- adapted to selected partner type

PRESSURE WORK:
- timed or score-based

GAME SIMULATION:
- live decision scenarios

FINISHER:
- competitive challenge
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite NBA skill development trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    if st.button("🔥 Generate Workout"):
        with st.spinner("Building your D1 workout..."):
            workout = build_workout()

            st.session_state.workout = workout

            st.session_state.history[user].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "workout": workout
            })

            st.success("Workout created! Go to Workout tab 🏀")

# =========================
# WORKOUT TAB (CLEAN UI BOXES)
# =========================
with workout_tab:
    st.title("🏀 Your D1 Workout")

    if not st.session_state.workout:
        st.info("No workout yet. Generate one from Home.")
    else:
        sections = st.session_state.workout.split("\n")

        current_section = []
        title = "Workout"

        def render_box(title, content):
            with st.container():
                st.markdown(f"### 🧱 {title}")
                st.markdown("\n".join(content))
                st.markdown("---")

        for line in sections:
            if any(x in line.lower() for x in ["warm", "skill", "partner", "pressure", "game", "finish"]):
                if current_section:
                    render_box(title, current_section)
                    current_section = []
                title = line.strip()

            current_section.append(line)

        if current_section:
            render_box(title, current_section)

        st.info(random.choice(quotes))

# =========================
# HISTORY TAB
# =========================
with history_tab:
    st.title("📊 Workout History")

    user_history = st.session_state.history.get(user, [])

    if not user_history:
        st.info("No workouts yet.")
    else:
        for w in reversed(user_history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.markdown(w["workout"])
                st.markdown("---")