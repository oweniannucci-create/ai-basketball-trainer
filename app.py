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
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = ""

if "history" not in st.session_state:
    st.session_state.history = {}

if "workout" not in st.session_state:
    st.session_state.workout = None

if "tab" not in st.session_state:
    st.session_state.tab = "Home"

# =========================
# DATA
# =========================
quotes = [
    "Greatness is built when no one is watching.",
    "Discipline beats motivation every time.",
    "You don’t rise to talent, you fall to effort.",
    "Comfort kills progress."
]

# =========================
# LOGIN
# =========================
st.title("🏀 D1 AI Trainer Login")

username = st.text_input("Enter your name")

if username:
    st.session_state.user = username

    if username not in st.session_state.history:
        st.session_state.history[username] = []

    st.success(f"Welcome {username} 💪")

# stop app if no user
if not st.session_state.user:
    st.stop()

# =========================
# TAB SYSTEM (manual control for auto-switch)
# =========================
tab = st.radio("Navigation", ["Home", "Workout", "History"], horizontal=True)
st.session_state.tab = tab

# =========================
# HOME TAB
# =========================
if st.session_state.tab == "Home":

    st.header("🏠 Build Your D1 Workout")

    focus = st.text_input("🎯 Focus")
    time_available = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("⚡ Energy", 1, 10, 5)

    partner = st.selectbox("🤝 Partner?", ["No", "Yes"])
    body = st.text_input("🦵 Body Status (sore/injured/etc)")

    # =========================
    # GENERATE BUTTON
    # =========================
    if st.button("🔥 Generate Workout"):

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        prompt = f"""
You are an elite NBA skill development coach.

Create a D1-level basketball workout.

PLAYER INFO:
Focus: {focus}
Time: {time_available}
Court: {court}
Energy: {energy}
Partner: {partner}
Body Status: {body}

REQUIREMENTS:
- Adjust intensity if sore/injured
- Include LIVE READ drill
- Include pressure situations
- Must include sets, reps, or time per drill
- Must be game realistic

FORMAT:
Warm-Up
Skill Work
Pressure Work
Game Simulation
Challenge
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content

        # save workout
        st.session_state.workout = output

        st.session_state.history[st.session_state.user].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "focus": focus,
            "workout": output
        })

        st.success("Workout created! Go to Workout tab 🏀")

        st.session_state.tab = "Workout"
        st.rerun()

# =========================
# WORKOUT TAB
# =========================
if st.session_state.tab == "Workout":

    st.header("🏀 Your D1 Workout")

    if st.session_state.workout:

        sections = st.session_state.workout.split("\n")

        box = ""
        title = ""

        for line in sections:
            if any(x in line.lower() for x in ["warm", "skill", "pressure", "game", "challenge"]):
                if box:
                    st.markdown(f"""
                    <div style="
                        padding:15px;
                        border-radius:10px;
                        background-color:#111;
                        margin-bottom:10px;
                    ">
                    {box}
                    </div>
                    """, unsafe_allow_html=True)
                    box = ""

                title = line
                box += f"<h4>{title}</h4>"
            else:
                box += f"<p>{line}</p>"

        if box:
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background-color:#111;
                margin-bottom:10px;
            ">
            {box}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No workout yet. Go to Home and generate one.")

    st.info(random.choice(quotes))

# =========================
# HISTORY TAB
# =========================
if st.session_state.tab == "History":

    st.header("📊 Workout History")

    user_history = st.session_state.history.get(st.session_state.user, [])

    if len(user_history) == 0:
        st.info("No workouts yet.")
    else:
        for i, w in enumerate(reversed(user_history)):

            st.markdown(f"### 🕒 {w['time']}")
            st.write(f"**Focus:** {w['focus']}")

            st.text_area(
                label="Workout",
                value=w["workout"],
                height=300,
                key=f"history_{i}"
            )

            st.markdown("---")