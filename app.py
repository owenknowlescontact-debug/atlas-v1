import os
import base64
import streamlit as st

st.set_page_config(
    page_title="Atlas",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Helpers
# -----------------------------
def image_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = image_to_base64("atlas_logo_transparent.png")

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    html, body, [class*="css"] {
        font-family: "Amazon Ember", "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(180,190,210,0.07), transparent 16%),
            radial-gradient(circle at 50% 14%, rgba(255,255,255,0.02), transparent 12%),
            linear-gradient(180deg, #04070b 0%, #060910 45%, #04070b 100%);
        color: #e9edf5;
        overflow: hidden;
    }

    .block-container {
        max-width: 100%;
        padding: 0.35rem 0.55rem 0.55rem 0.55rem;
    }

    /* Remove a lot of Streamlit default whitespace */
    div[data-testid="stVerticalBlock"] {
        gap: 0.25rem;
    }

    .shell {
        min-height: calc(100vh - 0.7rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.06);
        background:
            radial-gradient(circle at 50% 10%, rgba(255,255,255,0.03), transparent 15%),
            linear-gradient(180deg, rgba(6,9,14,0.97), rgba(4,7,11,0.99));
        box-shadow: 0 24px 90px rgba(0,0,0,0.5);
        overflow: hidden;
        position: relative;
    }

    .shell::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.012) 50%, transparent 100%);
        mix-blend-mode: screen;
    }

    .topbar {
        height: 64px;
        display: flex;
        align-items: center;
        padding: 0 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(4,6,10,0.40);
    }

    .topbar-group {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }

    .top-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 42px;
        padding: 0.42rem 0.85rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        color: #dfe5ef;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }

    .top-pill.atlas {
        font-size: 0.98rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        padding: 0.45rem 1rem;
    }

    .hero-wrap {
        min-height: calc(100vh - 64px - 1.2rem);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.15rem 1rem 0.4rem 1rem;
        position: relative;
    }

    .hero-wrap::before {
        content: "";
        position: absolute;
        top: 3%;
        left: 50%;
        transform: translateX(-50%);
        width: 44%;
        height: 24%;
        background: radial-gradient(circle, rgba(255,255,255,0.045), transparent 70%);
        filter: blur(18px);
        pointer-events: none;
    }

    .hero {
        width: 100%;
        max-width: 920px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        z-index: 1;
        margin: 0 auto;
    }

    .hero-logo {
        width: 86px;
        height: 86px;
        margin: 0 auto 1rem auto;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015));
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow:
            0 16px 50px rgba(0,0,0,0.32),
            0 0 30px rgba(255,255,255,0.025);
    }

    .hero-logo img {
        filter: brightness(0) invert(1) opacity(0.96);
        transform: scale(1.38);
        transform-origin: center;
    }

    .hero-title {
        font-size: 2.45rem;
        line-height: 1.06;
        font-weight: 650;
        letter-spacing: -0.03em;
        color: #edf2f9;
        margin: 0 auto 0.45rem auto;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8c95a2;
        margin: 0 auto 1rem auto;
        text-align: center;
    }

    .response-card {
        width: 100%;
        max-width: 760px;
        margin: 0.9rem auto 0 auto;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
        padding: 1rem;
        text-align: left;
    }

    .response-label {
        font-size: 0.8rem;
        color: #8c95a2;
        margin-bottom: 0.3rem;
    }

    .response-value {
        color: #edf2f9;
        font-size: 1rem;
        line-height: 1.5;
    }

    .subtle-note {
        margin-top: 0.75rem;
        color: #68717d;
        font-size: 0.76rem;
        text-align: center;
    }

    /* Style the real Streamlit form block */
    div[data-testid="stForm"] {
        width: 100%;
        max-width: 760px;
        margin: 0 auto;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stForm"] > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Actual input */
    div[data-testid="stTextInputRootElement"] > div {
        background: transparent !important;
    }

    div[data-testid="stTextInputRootElement"] input {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        color: #edf2f9 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 999px !important;
        padding: 1rem 1.1rem !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        min-height: 58px !important;
    }

    div[data-testid="stTextInputRootElement"] input::placeholder {
        color: #9aa3af !important;
    }

    /* Actual submit button */
    .stFormSubmitButton > button {
        width: 100% !important;
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        color: #edf2f9 !important;
        padding: 0.95rem 1rem !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        min-height: 58px !important;
    }

    .stFormSubmitButton > button:hover {
        border-color: rgba(255,255,255,0.14) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02)) !important;
    }

    /* tighten column spacing around input/button */
    div[data-testid="column"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Shell
# -----------------------------
st.markdown('<div class="shell">', unsafe_allow_html=True)

st.markdown('<div class="topbar"><div class="topbar-group">', unsafe_allow_html=True)
st.markdown('<div class="top-pill atlas">Atlas</div>', unsafe_allow_html=True)
st.markdown('<div class="top-pill">BETA</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hero-wrap"><div class="hero">', unsafe_allow_html=True)

if logo_base64:
    st.markdown(
        f'''
        <div class="hero-logo">
            <img src="data:image/png;base64,{logo_base64}" width="56" />
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.markdown('<div class="hero-title">Good to see you.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">How can I assist you today?</div>', unsafe_allow_html=True)

with st.form("atlas_prompt_form", clear_on_submit=False):
    cols = st.columns([8.6, 1.8], gap="small")
    with cols[0]:
        user_input = st.text_input(
            "",
            placeholder="Ask anything...",
            label_visibility="collapsed",
            key="atlas_prompt",
        )
    with cols[1]:
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.last_prompt = user_input.strip()

if st.session_state.last_prompt:
    st.markdown(
        f"""
        <div class="response-card">
            <div class="response-label">Latest prompt</div>
            <div class="response-value">{st.session_state.last_prompt}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="subtle-note">Atlas beta · cinematic operational AI shell</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)