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

if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

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
home, workout_tab, results_tab, history_tab, plan_tab = st.tabs(
    ["🏠 Home", "🏀 Build Workout", "📋 Workout Result", "📊 History", "📅 Weekly Plan"]
)

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.container().info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets (Click to Auto-Fill)")

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

    st.subheader("👤 Player Archetype")

    old_archetype = st.session_state.archetype

    st.session_state.archetype = st.selectbox(
        "Pick Style",
        archetypes
    )

    # If changed → refresh
    if old_archetype != st.session_state.archetype:
        st.rerun()

# =========================================================
# WORKOUT BUILDER
# =========================================================
with workout_tab:
    st.title("🏀 Build Your Training Session")

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
            ["Live Defender", "Rebounder", "Full 1v1 Opponent"]
        )

    body = st.text_input("🦵 Body Status")

    st.divider()

    generate = st.button("🔥 Generate Workout")

# =========================================================
# PROMPT
# =========================================================
def build_prompt():
    return f"""
You are an elite D1 basketball trainer.

Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Archetype: {st.session_state.archetype}
Partner: {partner}
Partner Role: {partner_role}
Body Status: {body}

RULES:
- Adjust for injury/soreness if needed
- If partner ON → include live reads & 1v1
- If shooter → high volume shooting
- If explosive → speed + finishing

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
# GENERATE BUTTON (FIXED FLOW)
# =========================================================
if generate:
    with st.spinner("Building your D1 workout..."):

        output = generate_workout(build_prompt())
        st.session_state.workout_output = output

        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "focus": focus,
            "output": output
        })

        st.success("Workout Created 🔥")
        st.info("👉 Go to the 'Workout Result' tab to view your session")

        # THIS IS THE KEY UX FIX
        st.rerun()

# =========================================================
# RESULTS TAB (CLEAN UI)
# =========================================================
with results_tab:
    st.title("📋 Your Workout")

    if st.session_state.workout_output == "":
        st.info("No workout yet. Generate one first.")
    else:

        st.success("🔥 D1 Training Session Ready")

        st.markdown("### 🧱 Workout Breakdown")
        st.text(st.session_state.workout_output)

        st.download_button(
            "⬇ Download Workout",
            st.session_state.workout_output,
            file_name="d1_workout.txt"
        )

        st.info(random.choice(quotes))

# =========================================================
# HISTORY TAB
# =========================================================
with history_tab:
    st.title("📊 History")

    if len(st.session_state.history) == 0:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.write(f"**Focus:** {w['focus']}")
                st.text_area("Workout", w["output"], height=200)
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
                    {"role": "user", "content": f"Create 7 day plan: {goal}"}
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