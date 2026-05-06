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

if "go_to_workout" not in st.session_state:
    st.session_state.go_to_workout = False

if "generated_workout" not in st.session_state:
    st.session_state.generated_workout = None

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

tabs = st.tabs(["🏠 Home", "🏀 Workout", "📊 History", "📅 Weekly Plan"])

home, workout, history, plans = tabs

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.subheader("📖 Daily Bible Verse")
    st.info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets")

    c1, c2, c3 = st.columns(3)

    def set_preset(value):
        st.session_state.preset = value
        st.session_state.go_to_workout = True

    with c1:
        if st.button("🔥 Scoring Workout"):
            set_preset("Scoring")

    with c2:
        if st.button("🏹 Shooting Workout"):
            set_preset("Shooting")

    with c3:
        if st.button("💪 Explosiveness"):
            set_preset("Explosiveness")

    st.markdown("---")

    st.subheader("👤 Player Archetype")

    archetype = st.selectbox(
        "Choose style",
        ["Kobe (Mamba Mentality)", "Curry (Shooter)", "Ja Morant (Explosive)", "LeBron (All-Around)"]
    )
    st.session_state.archetype = archetype

    st.success("Tip: Select preset or archetype → go to Workout tab")

# =========================================================
# WORKOUT TAB
# =========================================================
with workout:
    st.title("🏀 Build Your D1 Workout")

    focus = st.text_input("🎯 Focus", value=st.session_state.preset)

    energy = st.slider("⚡ Energy Level", 1, 10, 5)
    difficulty = st.slider("🔥 Difficulty", 1, 10, 5)

    time = st.selectbox("⏱ Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("🏀 Court", ["Driveway", "Half Court", "Full Court"])

    partner = st.selectbox("🤝 Partner?", ["No", "Yes"])
    injury = st.text_input("🦵 Body Status (sore, tight, injury?)")

    st.markdown("---")

    generate = st.button("🔥 Generate Workout")

    def generate_workout():
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
Body Status: {injury}

RULES:
- If partner = Yes → add competitive 1v1 / reaction drills
- If injury/sore → reduce jumping, add recovery + mobility
- Must include LIVE READ decision drill
- Must feel like D1 training + TikTok engaging
- Must include pressure situations

FORMAT:
1. Warm-Up
2. Skill Work
3. Pressure Work
4. Game Simulation
5. Challenge
6. Coaching Cues
"""
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite basketball trainer."},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content

    if generate:
        with st.spinner("Building your D1 workout..."):
            workout_text = generate_workout()

            st.session_state.generated_workout = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "archetype": st.session_state.archetype,
                "text": workout_text
            }

            st.session_state.history.append(st.session_state.generated_workout)

            st.session_state.go_to_workout = True

# ----------------------------
# AUTO SWITCH TAB LOGIC
# ----------------------------
if st.session_state.go_to_workout:
    st.session_state.go_to_workout = False
    st.rerun()

# =========================================================
# SHOW CURRENT WORKOUT (CARD STYLE)
# =========================================================
with workout:
    if st.session_state.generated_workout:
        w = st.session_state.generated_workout

        st.success("Workout Created ✅ Go to this tab anytime to review it.")

        st.markdown("### 🧱 Workout Card")

        st.container(border=True)
        st.markdown(f"**Focus:** {w['focus']}")
        st.markdown(f"**Archetype:** {w['archetype']}")
        st.markdown(f"**Time:** {w['time']}")

        st.markdown("---")

        st.text(w["text"])

        st.info(random.choice(quotes))

# =========================================================
# HISTORY TAB
# =========================================================
with history:
    st.title("📊 Workout History")

    if not st.session_state.history:
        st.info("No workouts yet.")
    else:
        for i, w in enumerate(reversed(st.session_state.history)):
            with st.container(border=True):
                st.markdown(f"### 🕒 {w['time']}")
                st.markdown(f"**Focus:** {w['focus']}")
                st.markdown(f"**Archetype:** {w['archetype']}")

                st.text_area(
                    "Workout",
                    w["text"],
                    height=250,
                    key=f"history_{i}"
                )

# =========================================================
# WEEKLY PLAN TAB
# =========================================================
with plans:
    st.title("📅 Weekly Plan")

    goal = st.text_input("What is your goal?")

    if st.button("Generate Plan"):
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a basketball coach."},
                {"role": "user", "content": f"Create 7 day plan for: {goal}"}
            ]
        )

        st.text(res.choices[0].message.content)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(random.choice(quotes))