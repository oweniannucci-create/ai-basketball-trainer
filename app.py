import streamlit as st
from groq import Groq
from datetime import datetime
import random
import time

# =========================
# PAGE CONFIG (MOBILE FEEL)
# =========================
st.set_page_config(
    page_title="D1 Trainer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================
# STYLE (APP LOOK)
# =========================
st.markdown("""
<style>
/* background */
.main {
    background-color: #0f0f0f;
}

/* title */
h1, h2, h3 {
    color: white;
}

/* cards */
div.stContainer {
    border-radius: 12px;
}

/* buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #ff4b1f, #ff9068);
    color: white;
}

/* input fields */
input, textarea {
    border-radius: 10px;
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
# DATA
# =========================
verse = "Philippians 4:13 — I can do all things through Christ who strengthens me."

quotes = [
    "Greatness is built when no one is watching.",
    "Discipline beats motivation every time.",
    "You don’t rise to talent, you fall to effort."
]

# =========================
# LOGIN
# =========================
if st.session_state.user is None:
    st.title("🏀 D1 TRAINER")

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
# HOME
# =========================
with home:
    st.markdown("## 🏀 D1 TRAINER")

    st.markdown("### 📖 Daily Verse")
    st.info(verse)

    st.markdown("## 🏀 Build Workout")

    focus = st.text_input("What are you working on?")
    struggle = st.text_input("What are you struggling with?")
    body = st.text_input("Body status")
    time_available = st.selectbox("Time", ["45 min", "60 min", "90 min"])
    court = st.selectbox("Court", ["Driveway", "Half Court", "Full Court"])
    energy = st.slider("Energy", 1, 10, 5)

    partner = st.selectbox(
        "Partner",
        ["No partner", "Rebounding partner", "Live defender partner"]
    )

    # =========================
    # WORKOUT GENERATION
    # =========================
    def generate():
        bar = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)

        prompt = f"""
You are an elite basketball trainer.

Make a D1-level workout.

PLAYER:
Focus: {focus}
Struggle: {struggle}
Body: {body}
Time: {time_available}
Court: {court}
Energy: {energy}
Partner: {partner}

RULES:
- Adapt EVERYTHING to focus + struggle
- If sore/injury → reduce intensity
- Partner changes drill structure
- Include reps, sets, and seconds
- Explain each drill clearly

FORMAT:

🔥 WARM-UP (mobility + activation)

🏀 SKILL WORK (detailed drills)

🤝 PARTNER WORK (based on partner type)

⚡ PRESSURE WORK (timed/scored)

🏆 GAME SIMULATION

🔥 FINISHER
"""

        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Elite NBA skills trainer."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    if st.button("🔥 GENERATE WORKOUT"):
        with st.spinner("Building D1 workout..."):
            st.session_state.workout = generate()

            st.session_state.history[user].append({
                "time": datetime.now().strftime("%H:%M"),
                "workout": st.session_state.workout
            })

            st.success("Workout ready → Go to Workout tab 🏀")

# =========================
# WORKOUT TAB (CLEAN CARDS)
# =========================
with workout:
    st.markdown("## 🏀 YOUR WORKOUT")

    if not st.session_state.workout:
        st.info("No workout yet")
    else:
        sections = st.session_state.workout.split("\n")

        box = []
        title = "Workout"

        def card(title, content):
            st.markdown(f"""
            <div style="
                background:#1c1c1c;
                padding:15px;
                border-radius:12px;
                margin-bottom:15px;
                border:1px solid #333;
                color:white;
            ">
            <h3>{title}</h3>
            <p>{content}</p>
            </div>
            """, unsafe_allow_html=True)

        for line in sections:
            if any(x in line.lower() for x in ["warm", "skill", "partner", "pressure", "game", "finish"]):
                if box:
                    card(title, "\n".join(box))
                    box = []
                title = line

            box.append(line)

        if box:
            card(title, "\n".join(box))

        st.markdown(f"### 💬 {random.choice(quotes)}")

# =========================
# HISTORY
# =========================
with history:
    st.markdown("## 📊 HISTORY")

    data = st.session_state.history.get(user, [])

    if not data:
        st.info("No workouts yet")
    else:
        for w in reversed(data):
            st.markdown(f"""
            <div style="
                background:#111;
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
                color:white;
            ">
            <b>{w['time']}</b>
            <pre style="white-space:pre-wrap">{w['workout']}</pre>
            </div>
            """, unsafe_allow_html=True)