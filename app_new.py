import streamlit as st

from voice_input import listen_for_income
from voice_profile_parser import parse_voice_profile

from rag_engine import retrieve_schemes
from eligibility_engine import find_eligible_schemes, rank_schemes
from ai_engine import explain_schemes

st.set_page_config(
    page_title="Bharat Sahayak AI",
    page_icon="🇮🇳",
    layout="wide"
)

# -----------------------
# DARK STYLE
# -----------------------

st.markdown("""
<style>

.stApp {
background:#0f172a;
}

h1,h2,h3,h4,p,label {
color:white;
}

.scheme-card {
background:#1e293b;
padding:18px;
border-radius:12px;
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATE
# -----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "profile" not in st.session_state:
    st.session_state.profile = {}

# -----------------------
# HEADER
# -----------------------

st.title("🇮🇳 Bharat Sahayak AI")
st.caption("Ask about Government Schemes")

st.divider()

# -----------------------
# CHAT HISTORY
# -----------------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -----------------------
# VOICE BUTTON
# -----------------------

col1,col2 = st.columns([6,1])

with col2:

    if st.button("🎤"):

        speech = listen_for_income()

        st.session_state.messages.append(
            {"role":"user","content":speech}
        )

        st.rerun()

# -----------------------
# CHAT INPUT
# -----------------------

user_input = st.chat_input(
"Ask about schemes or describe your profile..."
)

if user_input:

    st.session_state.messages.append(
        {"role":"user","content":user_input}
    )

    # -----------------------
    # PROFILE PARSING
    # -----------------------

    profile_update = parse_voice_profile(user_input)

    st.session_state.profile.update(profile_update)

    profile = st.session_state.profile

    # -----------------------
    # RAG RETRIEVAL
    # -----------------------

    retrieved = retrieve_schemes(user_input)

    schemes = find_eligible_schemes(profile, retrieved)

    top_schemes = rank_schemes(schemes)

    # -----------------------
    # AI EXPLANATION
    # -----------------------

    response = explain_schemes(profile, user_input)

    st.session_state.messages.append(
        {"role":"assistant","content":response}
    )

    st.rerun()

# -----------------------
# SHOW SCHEMES
# -----------------------

if "profile" in st.session_state and st.session_state.profile:

    st.divider()

    st.subheader("🏆 Recommended Schemes")

    retrieved = retrieve_schemes(str(st.session_state.profile))

    schemes = find_eligible_schemes(
        st.session_state.profile,
        retrieved
    )

    top_schemes = rank_schemes(schemes)

    for s in top_schemes:

        st.markdown(f"""
        <div class="scheme-card">
        <h3>{s['name']}</h3>
        <p>{s['benefit']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(s["score"]/100)

        st.write("Eligibility Score:",s["score"],"%")

        with st.expander("📄 Documents Required"):

            for d in s["documents"]:
                st.write("-",d)