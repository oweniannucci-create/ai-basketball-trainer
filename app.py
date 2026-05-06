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

if "latest_workout" not in st.session_state:
    st.session_state.latest_workout = ""

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
home, workout, history, plans = st.tabs(
    ["🏠 Home", "🏀 Workout", "📊 History", "📅 Weekly Plan"]
)

# =========================================================
# HOME TAB
# =========================================================
with home:
    st.title("🏀 D1 AI Trainer")

    st.info(random.choice(bible_verses))

    st.subheader("⚡ Quick Presets (click one)")

    c1, c2, c3 = st.columns(3)

    if c1.button("🔥 Scoring Workout"):
        st.session_state.preset = "Scoring"
        st.rerun()

    if c2.button("🏹 Shooting Workout"):
        st.session_state.preset = "Shooting"
        st.rerun()

    if c3.button("💪 Explosiveness"):
        st.session_state.preset = "Explosiveness"
        st.rerun()

    st.subheader("👤 Player Archetype")

    st.session_state.archetype = st.selectbox(
        "Choose style",
        [
            "Kobe (Mamba Mentality)",
            "Curry (Shooter)",
            "Ja Morant (Explosive)",
            "LeBron (All-Around)"
        ]
    )

    st.markdown("---")

    if st.button("🚀 Go to Workout Tab"):
        st.session_state.go_to_workout = True
        st.rerun()


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

    partner = st.selectbox("🤝 Partner?", ["No", "Yes"])
    struggle = st.text_input("📉 Struggle (optional)")
    body = st.text_input("🦵 Body status (sore / injured / tight / fine)")

    st.markdown("---")

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
Partner: {partner}
Struggle: {struggle}
Body: {body}

RULES:
- If partner = Yes → include live 1v1 / defensive pressure drills
- If sore/injured → reduce intensity + add recovery/mobility
- Must include LIVE READ drill
- Must feel like NBA development workout
- Must be structured and game-realistic

FORMAT:
Warm-Up
Skill Work
Pressure Work
Game Simulation
Challenge
"""

    def generate_workout():
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite basketball trainer."},
                {"role": "user", "content": build_prompt()}
            ]
        )
        return response.choices[0].message.content


    if st.button("🔥 Generate Workout"):

        with st.spinner("Building D1 workout..."):
            output = generate_workout()

            st.session_state.latest_workout = output

            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "focus": focus,
                "workout": output,
                "archetype": st.session_state.archetype
            })

            st.success("Workout Created 💪 Go to Workout Tab to view it")

            st.session_state.go_to_workout = True
            st.rerun()


    # ----------------------------
    # DISPLAY WORKOUT CLEANLY
    # ----------------------------
    if st.session_state.latest_workout:

        st.markdown("## 🧱 Your D1 Training Plan")

        sections = st.session_state.latest_workout.split("\n\n")

        for i, sec in enumerate(sections):
            st.markdown(f"""
            <div style="
                padding:12px;
                border-radius:12px;
                background:#111;
                border:1px solid #333;
                margin-bottom:10px;
            ">
            {sec}
            </div>
            """, unsafe_allow_html=True)

        st.info(random.choice(quotes))


# =========================================================
# HISTORY TAB (FIXED + CLEAN CARDS)
# =========================================================
with history:
    st.title("📊 Workout History")

    if not st.session_state.history:
        st.info("No workouts yet.")
    else:
        for i, w in enumerate(reversed(st.session_state.history)):

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:12px;
                background:#0f0f0f;
                border:1px solid #333;
                margin-bottom:10px;
            ">
            <h4>🕒 {w['time']}</h4>
            <p><b>Focus:</b> {w['focus']}</p>
            <p><b>Archetype:</b> {w['archetype']}</p>
            <pre style="white-space:pre-wrap;">{w['workout']}</pre>
            </div>
            """, unsafe_allow_html=True)


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
                    {"role": "system", "content": "You are a basketball trainer."},
                    {"role": "user", "content": f"Create a 7-day plan: {goal}"}
                ]
            )

            plan = response.choices[0].message.content

            st.markdown("## 📅 Weekly Plan")
            st.write(plan)

            st.download_button("⬇ Download Plan", plan, file_name="weekly_plan.txt")


# =========================================================
# AUTO TAB SWITCH LOGIC
# =========================================================
if st.session_state.go_to_workout:
    st.session_state.go_to_workout = False