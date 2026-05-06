import streamlit as st
from groq import Groq
from datetime import datetime
import random
import re

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

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "home"

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
def parse_workout(text):
    sections = re.split(r"\n(?=\d\.)", text)
    return sections

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

# ----------------------------
# TABS
# ----------------------------
home_tab, workout_tab, history_tab = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================================================
# HOME
# =========================================================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.info(f"📖 {random.choice(bible_verses)}")

    st.subheader("Build Your Workout")

    focus = st.text_input("🎯 Focus")
    energy = st.slider("⚡ Energy", 1, 10, 5)
    difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    struggle = st.text_input("📉 Struggle (optional)")
    body = st.text_input("🦵 Body status (optional)")

    partner = st.radio("🤝 Partner today?", ["No", "Yes"])

    st.markdown("---")

    if st.button("🔥 Build Workout"):
        prompt = f"""
Create a D1 basketball workout.

Player Info:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Struggle: {struggle}
Body: {body}
Partner: {partner}

Rules:
- Include warm-up, skill work, pressure, game simulation
- If partner = Yes, include 1v1 or reactive drills
- If body says sore/injured, include recovery + reduced load
- Must include LIVE READ drill
- Make it game realistic

Format clearly with numbered sections.
"""

        st.session_state.workout = generate_workout(prompt)

        st.session_state.active_tab = "workout"
        st.rerun()

# =========================================================
# WORKOUT TAB
# =========================================================
with workout_tab:
    st.title("🏀 Your D1 Workout")

    if st.session_state.workout:

        st.success("Workout Generated 💪")

        sections = parse_workout(st.session_state.workout)

        for i, sec in enumerate(sections):
            st.markdown(
                f"""
                <div style="
                    background-color:#111;
                    padding:15px;
                    border-radius:12px;
                    margin-bottom:10px;
                    border:1px solid #333;
                ">
                {sec}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout,
            file_name="d1_workout.txt"
        )

        st.info(random.choice(quotes))

    else:
        st.warning("No workout yet. Go to Home and generate one.")

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
        for w in reversed(st.session_state.history):
            st.markdown(f"### 🕒 {w['time']}")
            st.text_area("Workout", w.get("workout", ""), height=250)
            st.markdown("---")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption(random.choice(quotes))