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
# TABS
# ----------------------------
home, workout, history, plans = st.tabs(["🏠 Home", "🏀 Workout", "📊 History", "📅 Weekly Plan"])

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🔥 Scoring Workout"):
            st.session_state.preset = "Scoring"

    with c2:
        if st.button("🏹 Shooting Workout"):
            st.session_state.preset = "Shooting"

    with c3:
        if st.button("💪 Explosiveness"):
            st.session_state.preset = "Explosiveness"

    st.markdown("---")

    st.subheader("👤 Player Archetype")

    st.session_state.archetype = st.selectbox(
        "Choose style",
        ["Kobe (Mamba Mentality)", "Curry (Shooter)", "Ja Morant (Explosive)", "LeBron (All-Around)"]
    )

# =========================================================
# WORKOUT TAB
# =========================================================
with workout:
    st.title("🏀 Build Your D1 Workout")

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input("🎯 Focus", value=st.session_state.preset)
        energy = st.slider("⚡ Energy Level", 1, 10, 5)
        difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    with col2:
        time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
        court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    st.markdown("### Optional Context")

    struggle = st.text_input("📉 Struggle (optional)")
    body = st.text_input("🦵 Body status (optional)")

    st.markdown("---")

    colA, colB = st.columns(2)

    generate = colA.button("🔥 Generate Workout")
    regen = colB.button("🔁 Regenerate")

    # ----------------------------
    # PROMPT
    # ----------------------------
    prompt = f"""
You are an elite D1 basketball trainer.

Create a structured basketball workout.

STYLE:
- NBA trainer vibe
- TikTok engaging but still serious
- Card-based feel

PLAYER INFO:
Focus: {focus}
Energy: {energy}/10
Difficulty: {difficulty}/10
Time: {time}
Court: {court}
Archetype: {st.session_state.archetype}
Struggle: {struggle}
Body: {body}

REQUIREMENTS:
- Must include LIVE READ drill
- Must include pressure situations
- Must feel like real D1 training
- Must include coaching cues

FORMAT:
1. Warm-Up
2. Skill Work
3. Pressure Work
4. Game Simulation
5. Challenge
6. Coaching Cues
"""

    def generate_workout():
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite basketball skill development coach building D1-level workouts."
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    if generate or regen:
        with st.spinner("Building D1 workout..."):

            output = generate_workout()

            st.success("Workout Ready 💪")

            st.markdown("## 🧱 Your D1 Training Plan")

            st.markdown(f"""
### 📋 Workout

{output}

""")

""")

            st.markdown("---")

            st.info(f"💬 {random.choice(quotes)}")

            # SAVE HISTORY
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "workout": output
            })

            st.download_button(
                "⬇ Download Workout",
                output,
                file_name="d1_workout.txt"
            )

# =========================================================
# HISTORY TAB
# =========================================================
with history:
    st.title("📊 Workout History")

    if len(st.session_state.history) == 0:
        st.info("No workouts yet.")
    else:
        for w in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"### 🕒 {w['time']}")
                st.write(f"**Focus:** {w['focus']}")
                st.text_area("Workout", w["workout"], height=250)
                st.markdown("---")

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plans:
    st.title("📅 Weekly Training Plan Generator")

    goal = st.text_input("What is your weekly goal?")

    if st.button("Generate Weekly Plan"):
        with st.spinner("Building weekly plan..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an elite basketball trainer building weekly development plans."
                    },
                    {
                        "role": "user",
                        "content": f"Create a 7-day basketball training plan for: {goal}"
                    }
                ]
            )

            plan = response.choices[0].message.content

            st.write(plan)

            st.download_button(
                "⬇ Download Weekly Plan",
                plan,
                file_name="weekly_plan.txt"
            )

# =========================================================
# FOOTER MOTIVATION
# =========================================================
st.markdown("---")
st.caption(random.choice(quotes))









