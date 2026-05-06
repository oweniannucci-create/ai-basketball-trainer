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

if "generated_workout" not in st.session_state:
    st.session_state.generated_workout = None

if "tab" not in st.session_state:
    st.session_state.tab = "Home"

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
# AUTO TAB SWITCH
# ----------------------------
def go_to_workout_tab():
    st.session_state.tab = "Workout"

# ----------------------------
# TABS
# ----------------------------
tabs = st.tabs(["🏠 Home", "🏀 Workout", "📊 History", "📅 Weekly Plan"])
home_tab, workout_tab, history_tab, plan_tab = tabs

# =========================================================
# HOME TAB
# =========================================================
with home_tab:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets")

    c1, c2, c3 = st.columns(3)

    def set_preset(value):
        st.session_state.preset = value
        go_to_workout_tab()

    with c1:
        st.button("🔥 Scoring Workout", on_click=set_preset, args=("Scoring",))

    with c2:
        st.button("🏹 Shooting Workout", on_click=set_preset, args=("Shooting",))

    with c3:
        st.button("💪 Explosiveness", on_click=set_preset, args=("Explosiveness",))

    st.markdown("---")

    st.subheader("👤 Player Archetype")

    st.session_state.archetype = st.selectbox(
        "Choose style",
        ["Kobe (Mamba Mentality)", "Curry (Shooter)", "Ja Morant (Explosive)", "LeBron (All-Around)"],
        on_change=go_to_workout_tab
    )

# =========================================================
# WORKOUT TAB
# =========================================================
with workout_tab:
    st.title("🏀 Build Your D1 Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("🎯 Focus", value=st.session_state.preset)
        energy = st.slider("⚡ Energy Level", 1, 10, 5)
        difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    with col2:
        time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
        court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])
        partner = st.selectbox("🤝 Partner", ["No", "Yes"])

    st.markdown("### 🧠 Body Status")

    body = st.text_input("Any pain, soreness, or tightness?")

    st.markdown("---")

    generate = st.button("🔥 Generate Workout")

    if generate:
        with st.spinner("Building your D1 workout..."):

            prompt = f"""
You are an elite D1 basketball trainer.

PLAYER INFO:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Archetype: {st.session_state.archetype}
Partner: {partner}
Body Status: {body}

RULES:
- Adjust if injured or sore
- If partner = Yes, include 1v1 or live reads
- Must include LIVE READ drill
- Must include pressure situations
- Must be game realistic

FORMAT:
Break into sections:
Warm-Up
Skill Work
Pressure Work
Game Simulation
Challenge
Coaching Cues
"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an elite basketball trainer."},
                    {"role": "user", "content": prompt}
                ]
            )

            output = response.choices[0].message.content

            st.session_state.generated_workout = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "archetype": st.session_state.archetype,
                "output": output
            }

            st.session_state.history.append(st.session_state.generated_workout)

            go_to_workout_tab()

            st.success("Workout created! Go to Workout tab 👇")

# =========================================================
# DISPLAY WORKOUT (CLEAN CARD UI)
# =========================================================
with workout_tab:

    if st.session_state.generated_workout:

        w = st.session_state.generated_workout

        st.markdown("## 🧱 Your D1 Training Plan")

        st.container().markdown(f"""
### 🎯 Focus
{w['focus']}

### 👤 Archetype
{w['archetype']}

### 🕒 Time
{w['time']}
""")

        st.markdown("### 📋 Workout")

        st.info(w["output"])

        st.download_button(
            "⬇ Download Workout",
            w["output"],
            file_name="d1_workout.txt"
        )

# =========================================================
# HISTORY TAB
# =========================================================
with history_tab:
    st.title("📊 Workout History")

    if not st.session_state.history:
        st.info("No workouts yet.")
    else:
        for i, w in enumerate(reversed(st.session_state.history)):

            with st.container():
                st.markdown(f"### 🕒 {w.get('time','')}")
                st.write(f"**Focus:** {w.get('focus','')}")
                st.write(f"**Archetype:** {w.get('archetype','')}")
                st.info(w.get("output",""))
                st.markdown("---")

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plan_tab:
    st.title("📅 Weekly Plan")

    goal = st.text_input("Weekly Goal")

    if st.button("Generate Plan"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Build elite basketball weekly plans"},
                {"role": "user", "content": f"Create 7-day plan for: {goal}"}
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