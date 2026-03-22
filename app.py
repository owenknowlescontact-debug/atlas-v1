import os
import uuid
import base64
import streamlit as st

st.set_page_config(
    page_title="Atlas",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def image_to_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def create_chat(title: str = "New Chat") -> dict:
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "messages": [],
    }


def get_chat_index(chat_id: str) -> int:
    for i, chat in enumerate(st.session_state.chats):
        if chat["id"] == chat_id:
            return i
    return 0


logo_base64 = image_to_base64("atlas_logo_transparent.png")

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = [create_chat("New Chat")]
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = st.session_state.chats[0]["id"]
if "projects_placeholder" not in st.session_state:
    st.session_state.projects_placeholder = ["Project 1", "Project 2", "Project 3"]

active_index = get_chat_index(st.session_state.active_chat_id)
active_chat = st.session_state.chats[active_index]

# -------------------------------------------------
# Styling
# -------------------------------------------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    html, body, [class*="css"] {
        font-family: "Amazon Ember", "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }

    html, body, .stApp {
        height: 100%;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(205,215,230,0.08), transparent 18%),
            radial-gradient(circle at 50% 16%, rgba(255,255,255,0.03), transparent 14%),
            linear-gradient(180deg, #07101a 0%, #09131f 48%, #060d16 100%);
        color: #edf2f9;
        overflow: hidden;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.55rem !important;
        padding-right: 0.55rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(11,15,22,0.98), rgba(8,11,17,0.98)) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        min-width: 290px !important;
        max-width: 290px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.8rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }

    /* Sidebar arrow */
    button[title="Close sidebar"],
    button[title="Open sidebar"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        color: #f1f5fb !important;
    }

    button[title="Close sidebar"] svg,
    button[title="Open sidebar"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: #f1f5fb !important;
        stroke: #f1f5fb !important;
        color: #f1f5fb !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.95rem;
    }

    .brand-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 38px;
        padding: 0.38rem 0.86rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018));
        color: #e7edf7;
        font-size: 0.86rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }

    .sidebar-label {
        color: #98a2b0;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .placeholder-row {
        color: #98a2b0;
        font-size: 0.95rem;
        padding: 0.55rem 0.2rem 0.2rem 0.2rem;
    }

    /* Main */
    .main-shell {
        min-height: calc(100vh - 1rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.06);
        background:
            radial-gradient(circle at 50% 14%, rgba(255,255,255,0.035), transparent 18%),
            linear-gradient(180deg, rgba(10,15,24,0.97), rgba(7,11,18,0.99));
        box-shadow: 0 24px 90px rgba(0,0,0,0.42);
        position: relative;
        overflow: hidden;
    }

    .main-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.012) 50%, transparent 100%);
        mix-blend-mode: screen;
    }

    .main-stage {
        min-height: calc(100vh - 1rem);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 1rem 0.7rem 1rem;
        position: relative;
    }

    .main-stage::before {
        content: "";
        position: absolute;
        top: 10%;
        left: 50%;
        transform: translateX(-50%);
        width: 42%;
        height: 22%;
        background: radial-gradient(circle, rgba(255,255,255,0.05), transparent 72%);
        filter: blur(16px);
        pointer-events: none;
    }

    .landing-wrap {
        width: 100%;
        max-width: 900px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 1;
    }

    .hero-logo {
        width: 92px;
        height: 92px;
        margin: 0 auto 0.9rem auto;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.018));
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow:
            0 16px 50px rgba(0,0,0,0.28),
            0 0 30px rgba(255,255,255,0.02);
    }

    .hero-logo img {
        filter: brightness(0) invert(1) opacity(0.98);
        transform: scale(1.82);
        transform-origin: center;
    }

    .hero-title {
        font-size: 2.35rem;
        line-height: 1.06;
        font-weight: 650;
        letter-spacing: -0.03em;
        color: #f0f5fb;
        margin: 0 0 0.35rem 0;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #9aa5b3;
        margin: 0 0 1.05rem 0;
        text-align: center;
    }

    .prompt-wrap {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
    }

    /* Real form */
    div[data-testid="stForm"] {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    div[data-testid="stForm"] > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Input wrapper */
    div[data-testid="stTextInputRootElement"] {
        width: 100%;
    }

    div[data-testid="stTextInputRootElement"] [data-baseweb="input"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.018)) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 999px !important;
        box-shadow: none !important;
        min-height: 58px !important;
    }

    div[data-testid="stTextInputRootElement"] input {
        background: transparent !important;
        color: #edf2f9 !important;
        -webkit-text-fill-color: #edf2f9 !important;
        border: none !important;
        box-shadow: none !important;
        min-height: 58px !important;
        font-size: 1rem !important;
        padding: 0.95rem 1.15rem !important;
        opacity: 1 !important;
        caret-color: #edf2f9 !important;
    }

    div[data-testid="stTextInputRootElement"] input::placeholder {
        color: #9aa3af !important;
        -webkit-text-fill-color: #9aa3af !important;
        opacity: 1 !important;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover,
    textarea:-webkit-autofill:focus {
        -webkit-text-fill-color: #edf2f9 !important;
        box-shadow: 0 0 0px 1000px rgba(10,14,20,1) inset !important;
        -webkit-box-shadow: 0 0 0px 1000px rgba(10,14,20,1) inset !important;
        transition: background-color 9999s ease-in-out 0s;
    }

    /* Arrow button */
    .stFormSubmitButton > button {
        width: 100% !important;
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.018)) !important;
        color: #edf2f9 !important;
        padding: 0.95rem 1rem !important;
        box-shadow: none !important;
        font-weight: 700 !important;
        min-height: 58px !important;
        font-size: 1.1rem !important;
    }

    .stFormSubmitButton > button:hover {
        border-color: rgba(255,255,255,0.14) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.024)) !important;
    }

    div[data-testid="column"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .response-card {
        width: 100%;
        max-width: 900px;
        margin: 0.85rem auto 0 auto;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(255,255,255,0.038), rgba(255,255,255,0.016));
        padding: 1rem;
        text-align: left;
    }

    .response-label {
        font-size: 0.8rem;
        color: #9aa5b3;
        margin-bottom: 0.3rem;
    }

    .response-value {
        color: #edf2f9;
        font-size: 1rem;
        line-height: 1.5;
    }

    .subtle-note {
        margin-top: 0.65rem;
        color: #758091;
        font-size: 0.76rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-pill">Atlas</div>
            <div class="brand-pill">BETA</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("New Chat", use_container_width=True):
        new_chat = create_chat(f"New Chat {len(st.session_state.chats) + 1}")
        st.session_state.chats.insert(0, new_chat)
        st.session_state.active_chat_id = new_chat["id"]
        st.rerun()

    st.markdown('<div class="sidebar-label">Search Chats</div>', unsafe_allow_html=True)
    st.markdown('<div class="placeholder-row">Coming soon</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Projects</div>', unsafe_allow_html=True)
    for project in st.session_state.projects_placeholder[:3]:
        st.button(project, use_container_width=True, disabled=True)

    st.markdown('<div class="sidebar-label">Your Chats</div>', unsafe_allow_html=True)
    for chat in st.session_state.chats[:10]:
        is_active = chat["id"] == st.session_state.active_chat_id
        label = f"● {chat['title']}" if is_active else chat["title"]
        if st.button(label, use_container_width=True, key=f"chat_{chat['id']}"):
            st.session_state.active_chat_id = chat["id"]
            st.rerun()

# refresh active chat
active_index = get_chat_index(st.session_state.active_chat_id)
active_chat = st.session_state.chats[active_index]

# -------------------------------------------------
# Main
# -------------------------------------------------
st.markdown('<div class="main-shell"><div class="main-stage"><div class="landing-wrap">', unsafe_allow_html=True)

if logo_base64:
    st.markdown(
        f'''
        <div class="hero-logo">
            <img src="data:image/png;base64,{logo_base64}" width="62" />
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.markdown('<div class="hero-title">Good to see you.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">How can I assist you today?</div>', unsafe_allow_html=True)

st.markdown('<div class="prompt-wrap">', unsafe_allow_html=True)
with st.form("atlas_prompt_form", clear_on_submit=True):
    cols = st.columns([8.9, 1.1], gap="small")
    with cols[0]:
        user_input = st.text_input(
            "",
            placeholder="Ask anything...",
            label_visibility="collapsed",
        )
    with cols[1]:
        submitted = st.form_submit_button("➜")

    if submitted and user_input.strip():
        text = user_input.strip()
        if active_chat["title"].startswith("New Chat") and len(active_chat["messages"]) == 0:
            active_chat["title"] = text[:32]
        active_chat["messages"].append({"role": "user", "content": text})
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if active_chat["messages"]:
    last_text = active_chat["messages"][-1]["content"]
    st.markdown(
        f"""
        <div class="response-card">
            <div class="response-label">Latest prompt</div>
            <div class="response-value">{last_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="subtle-note">Atlas beta · cinematic operational AI shell</div>', unsafe_allow_html=True)
st.markdown('</div></div></div>', unsafe_allow_html=True)