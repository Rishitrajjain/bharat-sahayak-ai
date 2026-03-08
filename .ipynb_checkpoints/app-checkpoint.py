import streamlit as st

from eligibility_engine import find_eligible_schemes, rank_schemes
from ai_engine import explain_schemes, application_guide
from voice_input import listen_for_income
from voice_output import speak
from voice_profile_parser import parse_voice_profile


st.set_page_config(
    page_title="Bharat Sahayak AI",
    page_icon="🇮🇳",
    layout="wide"
)

# ---------------------
# DARK UI
# ---------------------

st.markdown("""
<style>

.stApp{
background:#0f172a;
}

h1,h2,h3,h4{
color:white;
}

.scheme{
background:#1e293b;
padding:20px;
border-radius:10px;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------
# HEADER
# ---------------------

st.title("🇮🇳 Bharat Sahayak AI")
st.caption("Talk to AI to discover government schemes")

st.divider()

# ---------------------
# USER INPUT
# ---------------------

st.subheader("🎤 Talk to Bharat Sahayak")

user_text = st.text_input(
"Example: मैं किसान हूँ मेरी आय 2 लाख है और मैं उत्तर प्रदेश से हूँ"
)

voice_button = st.button("🎙 Speak")

if voice_button:

    speech = listen_for_income()

    user_text = speech

    st.write("You said:", speech)

# ---------------------
# PROCESS PROFILE
# ---------------------

if user_text:

    profile = parse_voice_profile(user_text)

    st.subheader("🧠 AI Detected Profile")

    st.json(profile)

    # ---------------------
    # FIND SCHEMES
    # ---------------------

    schemes = find_eligible_schemes(profile)

    top_schemes = rank_schemes(schemes)

    st.subheader("🏆 Recommended Schemes")

    for s in top_schemes:

        st.markdown(f"""
        <div class="scheme">
        <h3>{s['name']}</h3>
        <p>{s['benefit']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(s["score"]/100)

        st.write("Eligibility Score:", s["score"], "%")

        col1,col2 = st.columns(2)

        with col1:

            if st.button(f"📄 Documents {s['name']}"):

                for d in s["documents"]:
                    st.write("-", d)

        with col2:

            if st.button(f"📝 Apply {s['name']}"):

                guide = application_guide(s)

                st.info(guide)

    # ---------------------
    # AI EXPLANATION
    # ---------------------

    st.subheader("🤖 AI Explanation")

    explanation = explain_schemes(profile, top_schemes)

    st.write(explanation)

    speak(explanation)

# ---------------------
# CHAT MODE
# ---------------------

st.divider()

st.subheader("💬 Ask AI")

question = st.text_input("Ask about schemes")

if question:

    st.chat_message("user").write(question)

    answer = explain_schemes(profile, top_schemes)

    st.chat_message("assistant").write(answer)