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

if "archetype" not in st.session_state:
    st.session_state.archetype = "Kobe (Mamba Mentality)"

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
home_tab, workout_tab, result_tab, history_tab, plan_tab = st.tabs(
    ["🏠 Home", "🏀 Build", "📋 Workout", "📊 History", "📅 Plan"]
)

# =========================================================
# HOME
# =========================================================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets")

    c1, c2, c3 = st.columns(3)

    if c1.button("🔥 Scoring"):
        st.session_state.preset = "Scoring"
        st.rerun()

    if c2.button("🎯 Shooting"):
        st.session_state.preset = "Shooting"
        st.rerun()

    if c3.button("💪 Explosiveness"):
        st.session_state.preset = "Explosiveness"
        st.rerun()

    st.subheader("👤 Archetype")

    st.session_state.archetype = st.selectbox(
        "Choose Style",
        archetypes
    )

# =========================================================
# BUILD WORKOUT
# =========================================================
with workout_tab:
    st.title("🏀 Build Your Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("Focus", value=st.session_state.preset)
        energy = st.slider("Energy", 1, 10, 5)
        difficulty = st.slider("Difficulty", 1, 10, 5)

    with col2:
        time = st.selectbox("Time", ["45 min", "60 min", "90 min"])
        court = st.selectbox("Court", ["Driveway", "Half Court", "Full Court"])

    partner = st.checkbox("🤝 Partner Mode")

    partner_role = ""
    if partner:
        partner_role = st.selectbox(
            "Partner Role",
            ["Live Defender", "Rebounder", "Full 1v1"]
        )

    body = st.text_input("🦵 Body Status (sore, injured, etc.)")

    generate = st.button("🔥 Generate Workout")

# =========================================================
# PROMPT BUILDER
# =========================================================
def build_prompt():
    return f"""
You are an elite D1 basketball trainer.

PLAYER:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Archetype: {st.session_state.archetype}
Partner Mode: {partner}
Partner Role: {partner_role}
Body Status: {body}

RULES:
- Adjust if injured or sore
- If partner is ON → include live reads & competition
- Must feel like real college training
- Must include pressure + game scenarios

FORMAT:
Warm-Up
Skill Work
Pressure Work
Live Read Drill
Game Simulation
Challenge
"""

# =========================================================
# AI CALL
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
# GENERATE
# =========================================================
if generate:
    with st.spinner("Building your D1 workout..."):

        output = generate_workout(build_prompt())

        st.session_state.workout_output = output

        # FIXED HISTORY FORMAT (NO ERRORS EVER)
        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "focus": focus,
            "output": output
        })

        st.success("Workout Created 🔥")
        st.info("👉 Go to the 'Workout' tab to view your session")

        st.rerun()

# =========================================================
# RESULT TAB (CLEAN UI)
# =========================================================
with result_tab:
    st.title("📋 Your Workout")

    if not st.session_state.workout_output:
        st.warning("No workout yet. Generate one first.")
    else:
        st.success("D1 Training Session Ready 💪")

        st.markdown("### 🧱 Workout Breakdown")
        st.text(st.session_state.workout_output)

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout_output,
            file_name="d1_workout.txt"
        )

        st.info(random.choice(quotes))

# =========================================================
# HISTORY TAB (FIXED SAFE ACCESS)
# =========================================================
with history_tab:
    st.title("📊 History")

    if not st.session_state.history:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"### 🕒 {w.get('time','')}")
                st.write(f"**Focus:** {w.get('focus','')}")
                st.text_area("Workout", w.get("output",""), height=200)
                st.divider()

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plan_tab:
    st.title("📅 Weekly Plan")

    goal = st.text_input("Weekly Goal")

    if st.button("Generate Plan"):
        with st.spinner("Building plan..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a D1 basketball coach."},
                    {"role": "user", "content": f"Create a 7-day plan: {goal}"}
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