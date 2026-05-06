import streamlit as st
from groq import Groq
from datetime import datetime
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="D1 Trainer AI",
    layout="centered"
)

# =========================
# ADVANCED UI STYLE (GYM / NBA AESTHETIC)
# =========================
st.markdown("""
<style>

/* animated dark gym background */
.stApp {
    background: radial-gradient(circle at top, #1a1a1a, #0a0a0a);
    color: white;
    font-family: 'Arial';
}

/* main title glow */
h1, h2, h3 {
    color: #ffffff;
    letter-spacing: 0.5px;
}

/* input fields */
input, textarea, select {
    border-radius: 10px !important;
}

/* buttons */
.stButton > button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    background: linear-gradient(90deg, #ff3d00, #ff9100);
    color: white;
    font-weight: bold;
    font-size: 16px;
    border: none;
}

/* card design */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}

/* section headers */
.section-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
    color: #ffb74d;
}

</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "workout" not in st.session_state:
    st.session_state.workout = None

if "history" not in st.session_state:
    st.session_state.history = {}

# =========================
# LOGIN
# =========================
if st.session_state.user is None:
    st.title("🏀 D1 TRAINER AI")

    name = st.text_input("Enter your name")

    if st.button("Enter Gym"):
        if name.strip():
            st.session_state.user = name.strip()

            if name not in st.session_state.history:
                st.session_state.history[name] = []

            st.rerun()

    st.stop()

user = st.session_state.user

# =========================
# TABS
# =========================
home, workout, history = st.tabs(["🏠 Home", "🏀 Workout", "📊 History"])

# =========================
# HOME TAB
# =========================
with home:
    st.title("🏀 D1 TRAINER AI")

    st.markdown("### 📖 Daily Focus")
    st.info("Philippians 4:13 — I can do all things through Christ who strengthens me.")

    st.markdown("### 🧠 Build Your Workout")

    focus = st.text_input("What are you working on today?")
    struggle = st.text_input("What are you struggling with?")
    body = st.text_input("Body status (sore / injury / good)")
    time_available = st.selectbox("Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("Court", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("Energy", 1, 10, 5)

    partner = st.selectbox(
        "Training Partner",
        ["No partner", "Rebounding partner", "Live defender partner"]
    )

    # =========================
    # AI WORKOUT GENERATOR
    # =========================
    def generate_workout():
        bar = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)

        prompt = f"""
You are an elite NBA skill development trainer.

PLAYER:
Focus: {focus}
Struggle: {struggle}
Body: {body}
Time: {time_available}
Court: {court}
Energy: {energy}
Partner: {partner}

RULES:
- Adjust based on focus + struggle
- If injury/sore → reduce intensity
- Partner changes drills completely
- Include reps, sets, seconds
- VERY CLEAR structure

FORMAT EXACTLY:

WARM-UP:
SKILL WORK:
PARTNER WORK:
PRESSURE WORK:
GAME SIMULATION:
FINISHER:
"""

        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Elite NBA trainer creating structured workouts."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    if st.button("🔥 GENERATE WORKOUT"):
        with st.spinner("Building your D1 workout..."):
            st.session_state.workout = generate_workout()

            st.session_state.history[user].append({
                "time": datetime.now().strftime("%H:%M"),
                "workout": st.session_state.workout
            })

            st.success("Workout ready → Go to Workout tab 🏀")

# =========================
# WORKOUT TAB (CLEAN SEPARATED CARDS)
# =========================
with workout:
    st.title("🏀 YOUR WORKOUT")

    if not st.session_state.workout:
        st.info("No workout yet.")
    else:

        sections = {
            "WARM-UP": "",
            "SKILL WORK": "",
            "PARTNER WORK": "",
            "PRESSURE WORK": "",
            "GAME SIMULATION": "",
            "FINISHER": ""
        }

        current = None

        for line in st.session_state.workout.split("\n"):
            line_upper = line.strip().upper()

            if line_upper in sections:
                current = line_upper
                continue

            if current:
                sections[current] += line + "\n"

        for title, content in sections.items():
            if content.strip():
                st.markdown(f"""
                <div class="card">
                    <div class="section-title">{title}</div>
                    <pre style="white-space:pre-wrap; color:white;">{content}</pre>
                </div>
                """, unsafe_allow_html=True)

# =========================
# HISTORY TAB
# =========================
with history:
    st.title("📊 HISTORY")

    data = st.session_state.history.get(user, [])

    if not data:
        st.info("No workouts yet.")
    else:
        for w in reversed(data):
            st.markdown(f"""
            <div class="card">
                <b>🕒 {w['time']}</b>
                <pre style="white-space:pre-wrap;">{w['workout']}</pre>
            </div>
            """, unsafe_allow_html=True)