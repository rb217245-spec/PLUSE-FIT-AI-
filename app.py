import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(
    page_title="Pulse Fit Plus AI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: radial-gradient(circle at 15% 0%, #182b3b 0%, #0b1220 38%, #080d17 100%); color: #eef4fb; }
[data-testid="stSidebar"] { background: #0d1725; border-right: 1px solid #203247; }
h1,h2,h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f4f8fc; }
.hero { padding: 28px 30px; border: 1px solid #29445a; border-radius: 22px;
        background: linear-gradient(115deg, rgba(19,44,61,.96), rgba(20,32,53,.92));
        margin-bottom: 22px; }
.hero-kicker { color: #5ce1bd; font-size: 12px; font-weight: 700; letter-spacing: 2px; }
.hero-title { font-family: 'Space Grotesk'; font-size: 34px; font-weight: 700; margin: 7px 0 4px; }
.hero-sub { color: #a9bdcf; font-size: 14px; }
.metric-card { background: linear-gradient(145deg,#142438,#101b2a); border: 1px solid #263d52;
               border-radius: 16px; padding: 18px; min-height: 118px; }
.metric-label { color: #9cb1c5; font-size: 12px; }
.metric-value { color: #f4f8fc; font-family: 'Space Grotesk'; font-size: 28px; font-weight: 700; margin-top: 8px; }
.metric-note { color: #5ce1bd; font-size: 11px; margin-top: 3px; }
.panel { background: #111d2c; border: 1px solid #263b50; border-radius: 16px; padding: 18px; }
.small-muted { color: #9cb1c5; font-size: 13px; }
div.stButton > button { background: linear-gradient(90deg,#20c997,#43d9b5); color: #07131b;
    border: 0; border-radius: 10px; font-weight: 700; min-height: 42px; }
div.stButton > button:hover { background: #62e8c5; color: #07131b; border: 0; }
.stTextInput input, .stTextArea textarea, .stNumberInput input { background: #101d2b !important; color: #eef4fb !important; }
[data-baseweb="select"] > div { background: #101d2b; }
hr { border-color: #263b50; }
</style>
""", unsafe_allow_html=True)


if "user" not in st.session_state:
    st.session_state.user = None
if "workouts" not in st.session_state:
    st.session_state.workouts = [
        {"date": date.today() - timedelta(days=4), "activity": "Brisk walk", "minutes": 25},
        {"date": date.today() - timedelta(days=3), "activity": "Bodyweight basics", "minutes": 20},
        {"date": date.today() - timedelta(days=1), "activity": "Cycling", "minutes": 30},
    ]
if "water" not in st.session_state:
    st.session_state.water = 5
if "chat" not in st.session_state:
    st.session_state.chat = [
        ("assistant", "Hi! I’m Pulse AI. Ask me about workout ideas, recovery, hydration, or balanced nutrition.")
    ]

def hero(title, subtitle, kicker="PULSE FIT PLUS AI"):
    st.markdown(f"""<div class="hero">
      <div class="hero-kicker">{kicker}</div>
      <div class="hero-title">{title}</div>
      <div class="hero-sub">{subtitle}</div>
    </div>""", unsafe_allow_html=True)

def metric(label, value, note=""):
    st.markdown(f"""<div class="metric-card"><div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>""",
      unsafe_allow_html=True)

def ai_workout(level, goal, equipment, minutes):
    plans = {
        "Beginner": [
            ("Warm-up", "5 min easy marching, shoulder rolls and gentle mobility"),
            ("Main set", "2 rounds: 8 chair squats, 8 wall push-ups, 10 glute bridges, 20-sec comfortable plank"),
            ("Cool-down", "5 min relaxed walking and gentle stretching"),
        ],
        "Intermediate": [
            ("Warm-up", "5–7 min brisk walking and dynamic mobility"),
            ("Main set", "3 comfortable rounds: 10 squats, 8 incline push-ups, 10 reverse lunges (each side), 20-sec plank"),
            ("Cool-down", "5 min easy walking and gentle stretching"),
        ],
        "Active": [
            ("Warm-up", "7 min easy cardio and dynamic mobility"),
            ("Main set", "3 rounds at a controlled pace: 12 squats, 10 incline push-ups, 12 hip bridges, 30-sec dead bug hold"),
            ("Cool-down", "5–7 min easy movement and stretching"),
        ],
    }
    result = plans[level]
    if equipment == "Gym access":
        result = [
            ("Warm-up", "5–7 min easy treadmill or cycle"),
            ("Main set", "2–3 controlled rounds: light goblet squat, seated row, chest press and cable-free core exercise. Choose comfortable resistance."),
            ("Cool-down", "5 min easy walking and gentle stretching"),
        ]
    return result

def assistant_reply(prompt):
    q = prompt.lower()
    if any(x in q for x in ["protein", "food", "meal", "nutrition", "eat"]):
        return ("For balanced nutrition, include a mix of protein foods (dal, beans, paneer, eggs, curd or tofu), "
                "whole grains, vegetables or fruit, and enough fluids. Needs vary by person; avoid extreme food rules. "
                "If you have a medical condition or specific dietary needs, ask a qualified health professional.")
    if any(x in q for x in ["workout", "exercise", "gym", "training"]):
        return ("A simple session can include a gentle warm-up, a few comfortable strength movements, and a cool-down. "
                "Start at a manageable level, focus on technique, and take rest days. Stop if you feel pain, dizziness, "
                "or unwell, and ask a trusted adult or qualified professional for help.")
    if any(x in q for x in ["water", "hydration", "drink"]):
        return ("Keep water available and drink regularly, especially around activity and in hot weather. "
                "Thirst, heat, and activity level all affect fluid needs.")
    if any(x in q for x in ["sleep", "rest", "recovery"]):
        return ("Recovery matters. Keep a consistent sleep routine, allow easier days between harder sessions, "
                "and avoid training through pain.")
    return ("I can help with general workout ideas, balanced nutrition, hydration and recovery. "
            "Tell me which area you want to explore. I’m a built-in demo assistant, not a medical professional.")


with st.sidebar:
    st.markdown("## 💚 Pulse Fit")
    st.caption("YOUR WELLNESS COMPANION")
    if st.session_state.user:
        st.success(f"Signed in as {st.session_state.user}")
    page = st.radio("NAVIGATION", [
        "Dashboard", "AI Workout Planner", "Nutrition Assistant",
        "Progress Charts", "Chatbot", "Login / Signup"
    ], label_visibility="visible")
    st.markdown("---")
    st.caption("Built-in AI demo • No API key required")
    if st.button("Reset demo data", use_container_width=True):
        st.session_state.workouts = []
        st.session_state.water = 0
        st.session_state.chat = [("assistant", "Hi! I’m Pulse AI. Ask me about workout ideas, recovery, hydration, or balanced nutrition.")]
        st.rerun()


if page == "Dashboard":
    hero("Move better. Feel stronger.", "A simple space to plan activity, explore balanced habits and track your consistency.")
    total_minutes = sum(x["minutes"] for x in st.session_state.workouts)
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("ACTIVITY SESSIONS", str(len(st.session_state.workouts)), "Logged sessions")
    with c2: metric("ACTIVE MINUTES", str(total_minutes), "Across logged sessions")
    with c3: metric("WATER CHECK-IN", f'{st.session_state.water} glasses', "Editable daily check-in")
    with c4: metric("TODAY", date.today().strftime("%d %b"), "Keep it consistent")
    st.write("")
    left,right = st.columns([1.35,1])
    with left:
        st.markdown("### Recent activity")
        if st.session_state.workouts:
            df = pd.DataFrame(st.session_state.workouts)
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d %b")
            st.dataframe(df.rename(columns={"date":"Date","activity":"Activity","minutes":"Minutes"}),
                         use_container_width=True, hide_index=True)
        else:
            st.info("No activity logged yet. Add a session in Progress Charts.")
    with right:
        st.markdown("### Daily check-in")
        st.write("Water check-in (glasses)")
        st.session_state.water = st.number_input("Water glasses", min_value=0, max_value=30,
                                                 value=int(st.session_state.water), step=1,
                                                 label_visibility="collapsed")
        st.markdown('<div class="panel"><b>Small reminder</b><p class="small-muted">Progress is about consistency, energy and feeling well — not perfection.</p></div>', unsafe_allow_html=True)
    st.markdown("### Quick start")
    q1,q2,q3 = st.columns(3)
    with q1:
        st.markdown('<div class="panel"><h4>🏃 Activity</h4><p class="small-muted">Build a manageable routine.</p></div>', unsafe_allow_html=True)
    with q2:
        st.markdown('<div class="panel"><h4>🥗 Nutrition</h4><p class="small-muted">Explore balanced food choices.</p></div>', unsafe_allow_html=True)
    with q3:
        st.markdown('<div class="panel"><h4>📈 Progress</h4><p class="small-muted">Notice your activity patterns.</p></div>', unsafe_allow_html=True)

elif page == "AI Workout Planner":
    hero("AI Workout Planner", "Create a simple, adjustable activity session based on your experience and available time.")
    a,b = st.columns(2)
    with a:
        level = st.selectbox("Experience level", ["Beginner", "Intermediate", "Active"])
        goal = st.selectbox("Main focus", ["General fitness", "Mobility and flexibility", "Strength basics", "Cardio fitness"])
    with b:
        equipment = st.selectbox("Available setup", ["No equipment", "Gym access"])
        minutes = st.slider("Available time (minutes)", 10, 60, 25, 5)
    if st.button("Generate my plan", use_container_width=True):
        st.session_state.generated_plan = ai_workout(level, goal, equipment, minutes)
        st.session_state.plan_focus = goal
    if "generated_plan" in st.session_state:
        st.markdown("### Your suggested session")
        st.caption(f"Focus: {st.session_state.get('plan_focus', goal)} • Adjust or skip any movement that doesn't feel comfortable.")
        for name, detail in st.session_state.generated_plan:
            st.markdown(f'<div class="panel"><b>{name}</b><p class="small-muted">{detail}</p></div>', unsafe_allow_html=True)
            st.write("")
        st.info("This is a general demo plan, not individualized medical advice. Use comfortable effort, prioritize good form and take breaks.")
    else:
        st.info("Choose your preferences and select Generate my plan.")

elif page == "Nutrition Assistant":
    hero("Nutrition Assistant", "Practical ideas for balanced meals, everyday energy and food variety.")
    st.markdown("### Build a balanced plate")
    cols = st.columns(3)
    cards = [
        ("🥚 Protein foods", "Dal, chickpeas, beans, paneer, curd, eggs, tofu or other suitable options."),
        ("🌾 Energy foods", "Roti, rice, oats, millets, potatoes and other grains or starchy foods."),
        ("🥦 Variety foods", "Vegetables and fruits in different colours, plus nuts or seeds when suitable.")
    ]
    for col,(title,desc) in zip(cols,cards):
        with col:
            st.markdown(f'<div class="panel"><h4>{title}</h4><p class="small-muted">{desc}</p></div>', unsafe_allow_html=True)
    st.write("")
    food = st.selectbox("Choose a food to explore", [
        "Dal", "Paneer", "Eggs", "Curd", "Chickpeas", "Oats", "Banana", "Tofu"
    ])
    food_notes = {
        "Dal":"A useful source of plant protein and fibre. Pair with rice or roti and vegetables.",
        "Paneer":"Provides protein and calcium. Pair with vegetables and a grain for a balanced meal.",
        "Eggs":"Provide protein and several nutrients. Prepare in a way that suits your preferences.",
        "Curd":"Provides protein and calcium; choose plain or lightly sweetened options if preferred.",
        "Chickpeas":"Provide plant protein and fibre. Add to salads, curries or wraps.",
        "Oats":"A whole-grain option that can be paired with milk or curd and fruit.",
        "Banana":"A convenient fruit that provides carbohydrates and potassium.",
        "Tofu":"A plant-based protein option that works in many savoury meals."
    }
    st.markdown(f'<div class="panel"><h4>{food}</h4><p class="small-muted">{food_notes[food]}</p></div>', unsafe_allow_html=True)
    st.caption("Nutrition needs differ from person to person. This tool does not calculate restrictive calorie targets or prescribe diets.")

elif page == "Progress Charts":
    hero("Progress & Activity", "Log movement you enjoy and view your activity history over time.")
    with st.expander("＋ Add an activity session", expanded=True):
        with st.form("activity_form"):
            d = st.date_input("Date", value=date.today())
            activity = st.selectbox("Activity", ["Walking", "Cycling", "Swimming", "Sports", "Bodyweight basics", "Yoga / Mobility", "Other"])
            mins = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=20)
            submitted = st.form_submit_button("Save activity")
            if submitted:
                st.session_state.workouts.append({"date": d, "activity": activity, "minutes": int(mins)})
                st.success("Activity saved.")
                st.rerun()
    if st.session_state.workouts:
        df = pd.DataFrame(st.session_state.workouts)
        df["date"] = pd.to_datetime(df["date"])
        daily = df.groupby("date", as_index=False)["minutes"].sum().sort_values("date")
        chart1,chart2 = st.columns(2)
        with chart1:
            st.markdown("### Active minutes")
            fig = px.line(daily, x="date", y="minutes", markers=True,
                          labels={"date":"Date","minutes":"Minutes"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#dce8f3", margin=dict(l=10,r=10,t=20,b=10))
            st.plotly_chart(fig, use_container_width=True)
        with chart2:
            st.markdown("### Activity mix")
            mix = df.groupby("activity", as_index=False)["minutes"].sum()
            fig2 = px.pie(mix, names="activity", values="minutes", hole=.55)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#dce8f3",
                               margin=dict(l=10,r=10,t=20,b=10), legend_title_text="")
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("### Session history")
        display = df.sort_values("date", ascending=False).copy()
        display["date"] = display["date"].dt.strftime("%d %b %Y")
        st.dataframe(display.rename(columns={"date":"Date","activity":"Activity","minutes":"Minutes"}),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No activity data yet. Add a session above to create your charts.")

elif page == "Chatbot":
    hero("Pulse AI Chat", "Ask general questions about movement, balanced nutrition, hydration or recovery.")
    for role, message in st.session_state.chat:
        with st.chat_message(role):
            st.write(message)
    prompt = st.chat_input("Ask Pulse AI something...")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        answer = assistant_reply(prompt)
        st.session_state.chat.append(("assistant", answer))
        st.rerun()
    st.caption("Pulse AI uses built-in topic-based responses. It does not connect to an external AI model or replace professional advice.")

elif page == "Login / Signup":
    hero("Welcome to Pulse Fit", "Create a local demo profile or sign in for this browser session.")
    st.info("Demo authentication only: account details are stored in Streamlit session memory, not in a secure database. Do not use a real password.")
    mode = st.radio("Choose an option", ["Login", "Signup"], horizontal=True)
    with st.form("auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Demo password", type="password")
        go = st.form_submit_button(mode)
        if go:
            if not username.strip() or not password:
                st.error("Please enter both fields.")
            else:
                st.session_state.user = username.strip()
                st.success(f"{mode} successful for this demo session, {username.strip()}!")
                st.rerun()
    if st.session_state.user and st.button("Logout"):
        st.session_state.user = None
        st.rerun()

st.markdown("---")
st.markdown('<div style="text-align:center;color:#7890a5;font-size:12px;padding:8px">PULSE FIT PLUS AI · Built for a balanced, consistent wellness journey</div>', unsafe_allow_html=True)
