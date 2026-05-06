import streamlit as st
from openai import OpenAI

# Page setup (mobile friendly)
st.set_page_config(page_title="AI Hooper Trainer", layout="centered")

# API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Header
st.title("🏀 AI Hooper Trainer")
st.caption("Train like a college player. Built for real hoopers.")

st.divider()

# --- INPUT SECTION ---
st.subheader("⚡ Today's Setup")

focus = st.text_input("🎯 What are you working on today?")
time = st.selectbox("⏱ Time Available", ["45–60 minutes", "60–90 minutes"])
court = st.selectbox("🏀 Court Type", ["Driveway", "Half Court", "Full Court"])
energy = st.selectbox("⚡ Energy Level", ["Low", "Medium", "High"])
struggle = st.text_input("📉 What have you been struggling with?")
body = st.text_input("🦵 Body Status (sore, tight, pain?)")

st.divider()

# --- PARTNER SECTION ---
st.subheader("🤝 Partner Mode")

partner = st.radio("Do you have a partner today?", ["No", "Yes"])

partner_time = ""
partner_role = ""

if partner == "Yes":
    partner_time = st.selectbox(
        "⏳ How long?",
        ["Full workout", "Half workout", "Specific time"]
    )
    partner_role = st.selectbox(
        "🎮 Partner Role",
        ["Live defense (1v1)", "Offense only", "Mixed"]
    )

st.divider()

# --- GENERATE BUTTON ---
if st.button("🔥 Generate Workout"):

    with st.spinner("Building your workout..."):

        prompt = f"""
You are an elite basketball skill development trainer building workouts for serious high school players trying to reach the college level.

Your workouts must:
- Be game-speed and realistic
- Include pressure and decision-making
- Include at least ONE LIVE READ DRILL
- Adapt to partner availability
- Include mobility if body soreness is mentioned
- Be mobile-friendly and easy to follow

USER INPUT:
Focus: {focus}
Time: {time}
Court: {court}
Energy: {energy}
Struggle: {struggle}
Body: {body}
Partner: {partner}
Partner Time: {partner_time}
Partner Role: {partner_role}

WORKOUT RULES:
- Warm-up must include dynamic movement + mobility if needed
- Skill work must match goal complexity
- Include:
  • Must-make drills
  • Countdown pressure drills
  • Game-winner scenarios
- Include at least one LIVE READ DRILL (decision-making)
- Include “Search:” for every drill

FORMAT:
Keep everything clean, short, and mobile-friendly.

SECTIONS:
1. Warm-Up
2. Skill Work
3. Pressure Section
4. Game Simulation
5. Challenge
6. Coaching Cues
7. Progress Tracker
"""

        response = client.chat.completions.create(
            model="gpt-5.3",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("Workout Ready 💪")
        st.markdown(response.choices[0].message.content)

st.divider()
st.caption("Built for serious hoopers. Stay consistent.")