import streamlit as st

from eligibility_engine import find_eligible_schemes, rank_schemes
from ai_engine import explain_schemes, application_guide
from voice_profile_parser import parse_voice_profile
from rag_engine import retrieve_schemes
from voice_output import speak


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
background:#0f172a;
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

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
"""
<h1 style='text-align:center;'>🇮🇳 Bharat Sahayak AI</h1>
<p style='text-align:center;'>Your AI Guide to Government Schemes</p>
""",
unsafe_allow_html=True
)

st.divider()

# -----------------------------
# USER INPUT
# -----------------------------

st.subheader("🧾 Tell us about yourself")

user_text = st.text_input(
    "Example: मैं किसान हूँ मेरी आय 2 लाख है और मैं उत्तर प्रदेश से हूँ"
)

# -----------------------------
# MAIN AI ENGINE
# -----------------------------

if user_text:

    # Parse user profile
    profile = parse_voice_profile(user_text)

    st.subheader("🧠 AI Detected Profile")

    st.json(profile)

    # Retrieve schemes via RAG
    retrieved_schemes = retrieve_schemes(user_text)

    # Eligibility engine
    eligible = find_eligible_schemes(profile, retrieved_schemes)

    # Ranking
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

            st.progress(s["score"]/100)

            st.write("Eligibility Score:", s["score"], "%")

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

    # Optional voice output
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
