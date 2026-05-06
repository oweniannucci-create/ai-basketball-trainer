import streamlit as st
from groq import Groq

# Page setup
st.set_page_config(page_title="AI Hooper Trainer", layout="centered")

# API client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
struggle = st.text_input("📉 Struggle (keep it short)")
body = st.text_input("🦵 Body Status (optional, short)")

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

# --- GENERATE ---
if st.button("🔥 Generate Workout"):

    # Build prompt (kept cleaner + safer)
    prompt = f"""
Create an elite basketball workout for a high school player.

USER INFO:
Focus: {focus}
Time: {time}
Court: {court}
Energy: {energy}
Struggle: {struggle}
Body: {body}
Partner: {partner}
Partner Time: {partner_time}
Partner Role: {partner_role}

RULES:
- Game-speed only
- Must include decision-making (LIVE READ DRILL)
- Include pressure situations
- Include must-make shooting drills
- Keep it simple and structured
- Add coaching cues
- If body is sore, include mobility warm-up

FORMAT:
1. Warm-Up
2. Skill Work
3. Pressure Work
4. Game Simulation
5. Challenge
6. Coaching Cues
"""

    with st.spinner("Building your workout..."):

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an elite basketball skill development trainer who builds simple, high-intensity, game-realistic workouts for serious high school athletes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            output = response.choices[0].message.content

            st.success("Workout Ready 💪")
            st.write(output)

        except Exception as e:
            st.error("Something went wrong with the AI request.")
            st.code(str(e))

st.divider()
st.caption("Built for serious hoopers. Stay consistent.")