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


def workout_card(title, text):
    st.markdown(
        f"""
        <div style="
            background-color:#111;
            padding:15px;
            border-radius:12px;
            margin-bottom:12px;
            border:1px solid #333;
        ">
            <h4 style="color:white;">{title}</h4>
            <pre style="white-space:pre-wrap; color:#ddd;">{text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# UI
# ----------------------------
home_tab, workout_tab, history_tab = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================================================
# HOME TAB
# =========================================================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.info(random.choice(bible_verses))

    st.subheader("Build Your Workout")

    focus = st.text_input("🎯 Focus")
    energy = st.slider("⚡ Energy", 1, 10, 5)
    difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    body = st.text_input("🦵 Body status (sore/injured/etc)")
    partner = st.radio("🤝 Partner?", ["No", "Yes"])

    st.markdown("---")

    if st.button("🔥 Build Workout"):
        prompt = f"""
Create a D1 basketball workout.

Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Body status: {body}
Partner: {partner}

Rules:
- Include warm-up, skill, pressure, game simulation
- If partner = Yes, include 1v1 / reactive drills
- If body is sore/injured, reduce load + add recovery work
- Include LIVE READ drill
- Make it realistic and intense
"""

        st.session_state.workout = generate_workout(prompt)

        st.success("Workout created 💪 Go to Workout tab")

# =========================================================
# WORKOUT TAB
# =========================================================
with workout_tab:
    st.title("🏀 Your Workout")

    if st.session_state.workout:

        workout = st.session_state.workout

        # Split into sections if numbered
        sections = workout.split("\n")

        for i, line in enumerate(sections):
            if line.strip():
                workout_card(f"Drill {i+1}", line)

        st.download_button(
            "⬇ Download Workout",
            workout,
            file_name="d1_workout.txt"
        )

        st.info(random.choice(quotes))

    else:
        st.warning("No workout yet. Go to Home and build one.")

# =========================================================
# HISTORY TAB
# =========================================================
with history_tab:
    st.title("📊 Workout History")

    if st.session_state.workout:
        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "workout": st.session_state.workout
        })

    if len(st.session_state.history) == 0:
        st.info("No workouts yet.")
    else:
        for i, w in enumerate(reversed(st.session_state.history)):
            st.markdown(f"### 🕒 {w['time']}")

            # SAFE CARD (NO text_area = NO duplicate errors)
            workout_card("Workout", w.get("workout", ""))

            st.markdown("---")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption(random.choice(quotes))