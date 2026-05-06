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

if "preset" not in st.session_state:
    st.session_state.preset = ""

if "workout_output" not in st.session_state:
    st.session_state.workout_output = ""

# ----------------------------
# DATA
# ----------------------------
bible_verses = [
    "Philippians 4:13 — I can do all things through Christ who strengthens me.",
    "Isaiah 40:31 — Those who hope in the Lord will renew their strength.",
    "Proverbs 3:5 — Trust in the Lord with all your heart.",
]

quotes = [
    "Greatness is built when no one is watching.",
    "Discipline beats motivation every time.",
    "Comfort kills progress."
]

archetypes = [
    "Kobe (Mamba Mentality)",
    "Curry (Shooter)",
    "Ja Morant (Explosive)",
    "LeBron (All-Around)"
]

# ----------------------------
# TABS
# ----------------------------
home, workout_tab, results, history, plans = st.tabs(
    ["🏠 Home", "🏀 Build Workout", "📋 Workout Result", "📊 History", "📅 Weekly Plan"]
)

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    with st.container():
        st.subheader("📖 Daily Verse")
        st.info(random.choice(bible_verses))

    with st.container():
        st.subheader("⚡ Quick Presets")

        col1, col2, col3 = st.columns(3)

        if col1.button("🔥 Scoring"):
            st.session_state.preset = "Scoring"

        if col2.button("🎯 Shooting"):
            st.session_state.preset = "Shooting"

        if col3.button("💪 Explosiveness"):
            st.session_state.preset = "Explosiveness"

    with st.container():
        st.subheader("👤 Archetype Preview")
        st.session_state.archetype = st.selectbox("Pick Style", archetypes)

# =========================================================
# WORKOUT BUILDER TAB
# =========================================================
with workout_tab:
    st.title("🏀 Build Your Training Session")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("🎯 Focus", value=st.session_state.preset)
        energy = st.slider("⚡ Energy", 1, 10, 5)
        difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    with col2:
        time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
        court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    st.divider()

    partner = st.toggle("🤝 Partner Training Mode")

    partner_role = ""
    if partner:
        partner_role = st.selectbox(
            "Partner Role",
            ["Live Defender", "Rebounder Only", "Full 1v1 Opponent"]
        )

    st.divider()

    body_status = st.text_input("🦵 Body Status (sore / injured / good)")

    st.divider()

    generate = st.button("🔥 Generate D1 Workout")

# =========================================================
# PROMPT ENGINE
# =========================================================
def build_prompt():
    return f"""
You are an elite D1 basketball trainer.

PLAYER PROFILE:
- Focus: {focus}
- Energy: {energy}/10
- Difficulty: {difficulty}/10
- Time: {time}
- Court: {court}
- Archetype: {st.session_state.archetype}
- Partner Mode: {partner}
- Partner Role: {partner_role}
- Body Status: {body_status}

RULES:
- If partner is ON → include live reps, 1v1, reactions
- If injured/sore → reduce jumping, avoid stress drills
- If explosive archetype → emphasize speed & finishing
- If shooter → volume + fatigue shooting
- Must include LIVE READ decision drill

FORMAT:
Return in sections:
Warm-Up
Skill Blocks
Pressure Work
Live Read Drill
Game Simulation
Challenge
"""

# =========================================================
# GENERATE WORKOUT
# =========================================================
def generate_workout(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an elite basketball trainer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# =========================================================
# BUTTON ACTION
# =========================================================
if generate:
    with st.spinner("Building your D1 workout..."):
        prompt = build_prompt()
        output = generate_workout(prompt)

        st.session_state.workout_output = output

        # SAVE HISTORY
        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "focus": focus,
            "output": output
        })

        # SWITCH TAB LOGIC
        st.switch_page = "Workout Result"

# =========================================================
# RESULTS TAB (CLEAN UI BOXES)
# =========================================================
with results:
    st.title("📋 Your D1 Workout")

    if st.session_state.workout_output == "":
        st.info("Generate a workout first.")
    else:

        sections = st.session_state.workout_output.split("\n")

        box = st.container()
        with box:
            st.markdown("### 🧱 Training Plan")
            st.write(st.session_state.workout_output)

        st.success(random.choice(quotes))

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout_output,
            file_name="d1_workout.txt"
        )

# =========================================================
# HISTORY TAB
# =========================================================
with history:
    st.title("📊 Workout History")

    for w in reversed(st.session_state.history):
        with st.container():
            st.markdown(f"### 🕒 {w['time']}")
            st.markdown(f"**Focus:** {w['focus']}")
            st.text_area("Workout", w["output"], height=200)
            st.divider()

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plans:
    st.title("📅 Weekly Training Plan")

    goal = st.text_input("Weekly Goal")

    if st.button("Generate Plan"):
        with st.spinner("Building plan..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a D1 strength & skill coach."},
                    {"role": "user", "content": f"Create 7-day plan for: {goal}"}
                ]
            )

            plan = response.choices[0].message.content

            st.write(plan)

            st.download_button("⬇ Download Plan", plan, file_name="weekly_plan.txt")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(random.choice(quotes))