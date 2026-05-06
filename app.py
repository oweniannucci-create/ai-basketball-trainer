import streamlit as st
from groq import Groq
from datetime import datetime
import random
import time
import re

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# LOGIN SYSTEM
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------------------
# SESSION STATE
# ----------------------------
if "workout" not in st.session_state:
    st.session_state.workout = None

if "history" not in st.session_state:
    st.session_state.history = {}

# ----------------------------
# LOGIN UI
# ----------------------------
if not st.session_state.logged_in:
    st.title("🏀 D1 AI Trainer Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login / Create Account"):
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success(f"Welcome {user} 💪")
            st.rerun()
    st.stop()

# ----------------------------
# DATA
# ----------------------------
quotes = [
    "Greatness is built when no one is watching.",
    "Discipline beats motivation every time.",
    "You don’t rise to talent, you fall to effort.",
    "Comfort kills progress."
]

# ----------------------------
# HELPERS
# ----------------------------
def generate_workout(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an elite D1 basketball skill development coach."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def section_card(title, content):
    st.markdown(
        f"""
        <div style="
            background:#111;
            padding:16px;
            border-radius:12px;
            margin-bottom:12px;
            border:1px solid #333;
        ">
        <h3 style="color:white;">{title}</h3>
        <pre style="white-space:pre-wrap; color:#ddd;">{content}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

def extract_sections(text):
    pattern = r"(Warm-Up|Skill Work|Pressure Work|Game Simulation|Challenge|Coaching Cues)"
    parts = re.split(pattern, text)

    sections = []
    i = 1

    while i < len(parts) - 1:
        title = parts[i].strip()
        content = parts[i + 1].strip()
        sections.append((title, content))
        i += 2

    return sections

# ----------------------------
# TABS
# ----------------------------
home, workout, history = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================================================
# HOME
# =========================================================
with home:
    st.title(f"🏀 D1 AI Trainer - {st.session_state.username}")

    focus = st.text_input("🎯 Focus")
    energy = st.slider("⚡ Energy", 1, 10, 5)
    difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    time_available = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    body = st.text_input("🦵 Body status (sore/injured/etc)")
    partner = st.radio("🤝 Partner?", ["No", "Yes"])

    st.markdown("---")

    if st.button("🔥 Generate Workout"):

        prompt = f"""
Create a D1 basketball workout.

PLAYER INFO:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time_available}
Court: {court}
Body: {body}
Partner: {partner}

REQUIREMENTS:
- Every drill MUST include:
  • Sets
  • Reps OR Time (seconds)
  • Step-by-step instructions
  • Coaching cues
  • Game translation

- Warm-Up MUST include mobility + activation
- Timed drills must use seconds
- Reps must include sets (example: 3x10)

FORMAT:
Warm-Up:
Skill Work:
Pressure Work:
Game Simulation:
Challenge:
Coaching Cues:
"""

        # LOADING BAR
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        st.session_state.workout = generate_workout(prompt)

        # SAVE HISTORY PER USER
        user = st.session_state.username

        if user not in st.session_state.history:
            st.session_state.history[user] = []

        st.session_state.history[user].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "workout": st.session_state.workout
        })

        st.success("Workout Created 💪 Go to Workout Tab")

# =========================================================
# WORKOUT
# =========================================================
with workout:
    st.title("🏀 Your D1 Workout")

    if st.session_state.workout:

        sections = extract_sections(st.session_state.workout)

        if not sections:
            section_card("Full Workout", st.session_state.workout)
        else:
            for title, content in sections:
                section_card(title, content)

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout,
            file_name="d1_workout.txt"
        )

        st.info(random.choice(quotes))

    else:
        st.warning("No workout yet. Go to Home and generate one.")

# =========================================================
# HISTORY
# =========================================================
with history:
    st.title("📊 Your History")

    user_history = st.session_state.history.get(st.session_state.username, [])

    if not user_history:
        st.info("No workouts yet.")
    else:
        for w in reversed(user_history):
            st.markdown(f"### 🕒 {w['time']}")
            section_card("Workout", w["workout"])

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption(random.choice(quotes))