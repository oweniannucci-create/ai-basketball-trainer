import streamlit as st
from groq import Groq
from datetime import datetime
import time

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="D1 AI Trainer", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# LOGIN (simple)
# ----------------------------
if "user" not in st.session_state:
    st.session_state.user = ""

if st.session_state.user == "":
    st.title("🏀 D1 AI Trainer Login")
    username = st.text_input("Enter your name")

    if st.button("Enter"):
        if username:
            st.session_state.user = username
            st.rerun()
    st.stop()

# ----------------------------
# USER HISTORY STORAGE
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = {}

if st.session_state.user not in st.session_state.history:
    st.session_state.history[st.session_state.user] = []

# ----------------------------
# TABS
# ----------------------------
home, workout, history_tab = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# ----------------------------
# SESSION FLAGS
# ----------------------------
if "latest_workout" not in st.session_state:
    st.session_state.latest_workout = None

if "go_to_workout" not in st.session_state:
    st.session_state.go_to_workout = False


# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    focus = st.text_input("🎯 What are you working on today?")
    time_available = st.selectbox("⏱ Time", ["45–60 min", "60–90 min", "90+ min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("⚡ Energy", 1, 10, 5)

    partner = st.radio("🤝 Do you have a partner?", ["No", "Yes"])
    body = st.text_input("🦵 Body status (sore / injured / fine)")

    if st.button("🔥 Build Workout"):
        st.session_state.go_to_workout = True

        prompt = f"""
You are an elite D1 basketball trainer.

PLAYER INFO:
Focus: {focus}
Time: {time_available}
Court: {court}
Energy: {energy}
Partner: {partner}
Body: {body}

RULES:
- If partner = Yes → include 1v1 or reaction drills
- If sore/injured → reduce intensity + add recovery work
- Must include sets, reps, and timed sections
- Must be realistic game-speed training

FORMAT OUTPUT EXACTLY LIKE:

WARMUP:
- drill name + instructions + sets/reps/time

SKILL WORK:
- drill name + instructions + sets/reps/time

PRESSURE:
- drill + countdown / scoring system

GAME SIM:
- game scenario

FINISHER:
- challenge drill
"""

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a D1 basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        workout = response.choices[0].message.content

        st.session_state.latest_workout = workout

        # save history per user
        st.session_state.history[st.session_state.user].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "workout": workout
        })

        st.success("Workout created! Go to Workout tab 👇")


# auto-switch hint
if st.session_state.go_to_workout:
    st.session_state.go_to_workout = False


# =========================================================
# WORKOUT TAB
# =========================================================
with workout:
    st.title("🏀 Your Training Session")

    if not st.session_state.latest_workout:
        st.info("No workout yet. Build one from Home.")
    else:
        text = st.session_state.latest_workout

        sections = text.split("\n\n")

        for i, sec in enumerate(sections):
            with st.container():
                st.markdown("### 📦 Section")
                st.write(sec)
                st.markdown("---")

        st.download_button(
            "⬇ Download Workout",
            text,
            file_name="d1_workout.txt"
        )


# =========================================================
# HISTORY TAB
# =========================================================
with history_tab:
    st.title("📊 Workout History")

    user_history = st.session_state.history.get(st.session_state.user, [])

    if not user_history:
        st.info("No workouts yet.")
    else:
        for w in reversed(user_history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.text_area("Workout", w["workout"], height=250, key=w["time"])
                st.markdown("---")