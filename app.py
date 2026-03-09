import streamlit as st

from eligibility_engine import find_eligible_schemes, rank_schemes
from ai_engine import explain_schemes, application_guide
from voice_profile_parser import parse_voice_profile
from rag_engine import retrieve_schemes
from voice_output import speak
import plotly.graph_objects as go


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Bharat Sahayak AI",
    page_icon="🇮🇳",
    layout="wide"
)

# -----------------------------
# CUSTOM DARK UI
# -----------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top, #1e3a8a, #0f172a);
background-attachment: fixed;
}

h1,h2,h3,h4{
color:white;
}

.scheme{
background:#1e293b;
padding:20px;
border-radius:12px;
margin-bottom:20px;
border:1px solid #334155;
}

.scheme:hover{
border:1px solid #3b82f6;
}

.stTextInput>div>div>input{
background:#1e293b;
color:white;
}

.feature-card{
background:#1e293b;
padding:20px;
border-radius:10px;
border:1px solid #334155;
text-align:center;
}

.feature-card:hover{
border:1px solid #3b82f6;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HERO SECTION
# -----------------------------

st.markdown(
"""
<h1 style='text-align:center;font-size:48px;'>🇮🇳 Bharat Sahayak AI</h1>
<p style='text-align:center;font-size:20px;'>Your AI Guide to Government Schemes</p>
<p style='text-align:center;font-size:14px;color:#9ca3af;'>
Helping citizens discover the right government benefits with AI
</p>
""",
unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)

st.divider()


# -----------------------------
# FEATURE CARDS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h3>🎯 Smart Discovery</h3>
    <p>AI analyzes your profile and finds the most relevant government schemes.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h3>🧠 AI Explanation</h3>
    <p>Understand why a scheme matches your profile in simple language.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>📄 Application Help</h3>
    <p>Get step-by-step instructions to apply for schemes easily.</p>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# -----------------------------
# USER INPUT
# -----------------------------

st.subheader("🧾 Tell us about yourself")

st.caption("Try examples:")
st.write("• मैं किसान हूँ मेरी आय 2 लाख है और मैं उत्तर प्रदेश से हूँ")
st.write("• मैं महिला हूँ और छोटा व्यवसाय शुरू करना चाहती हूँ")

user_text = st.text_input(
    "Describe yourself:"
)

# -----------------------------
# MAIN AI ENGINE
# -----------------------------

if user_text:

    with st.spinner("🤖 AI is analyzing your profile..."):

        profile = parse_voice_profile(user_text)

        st.subheader("🧠 AI Detected Profile")

        st.json(profile)

        retrieved_schemes = retrieve_schemes(user_text)

        eligible = find_eligible_schemes(profile, retrieved_schemes)

        top_schemes = rank_schemes(eligible)

    # -----------------------------
    # DISPLAY SCHEMES
    # -----------------------------

    st.subheader("🏆 Recommended Government Schemes")

    if len(top_schemes) == 0:

        st.warning("No schemes found for this profile.")

    else:

        for i, s in enumerate(top_schemes):

            st.markdown(f"""
            <div class="scheme">
            <h3>{s['name']}</h3>
            <p>{s['benefit']}</p>
            </div>
            """, unsafe_allow_html=True)

            score = s["score"]

            colA, colB = st.columns([3,1])

            with colA:
                st.markdown(f"""
                <div class="scheme">
                <h3>{s['name']}</h3>
                <p>{s['benefit']}</p>
                </div>
                """, unsafe_allow_html=True)

            with colB:
                score = s["score"]
            
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={'text': "Score"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#3b82f6"},
                        'steps': [
                            {'range': [0, 40], 'color': "#7f1d1d"},
                            {'range': [40, 70], 'color': "#92400e"},
                            {'range': [70, 100], 'color': "#065f46"}
                        ],
                    }
                ))
            
                fig.update_layout(height=200)
            
                st.plotly_chart(fig, use_container_width=True, key=f"gauge{i}")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(f"📄 Documents for {s['name']}", key=f"doc{i}"):

                    for d in s["documents"]:
                        st.write("•", d)

            with col2:

                if st.button(f"📝 How to Apply for {s['name']}", key=f"apply{i}"):

                    guide = application_guide(s)

                    st.info(guide)

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------

    st.divider()

    st.subheader("🤖 AI Explanation")

    explanation = explain_schemes(profile, user_text)

    st.write(explanation)

    try:
        speak(explanation)
    except:
        pass


# -----------------------------
# CHAT MODE
# -----------------------------

st.divider()

st.subheader("💬 Ask Bharat Sahayak")

question = st.text_input("Ask anything about government schemes")

if question:

    st.chat_message("user").write(question)

    if user_text:

        answer = explain_schemes(profile, question)

    else:

        answer = "Please tell me about yourself first so I can recommend the best schemes."

    st.chat_message("assistant").write(answer)


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption("Built with ❤️ for Digital India")
