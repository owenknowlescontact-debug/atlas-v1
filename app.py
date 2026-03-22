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
            radial-gradient(circle at 50% 0%, rgba(180,190,210,0.06), transparent 16%),
            radial-gradient(circle at 50% 16%, rgba(255,255,255,0.025), transparent 12%),
            linear-gradient(180deg, #04070b 0%, #060910 45%, #04070b 100%);
        color: #e9edf5;
        overflow: hidden;
    }

    .block-container {
        padding-top: 0.45rem;
        padding-bottom: 0.45rem;
        padding-left: 0.55rem;
        padding-right: 0.55rem;
        max-width: 100%;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(9,12,18,0.98), rgba(6,8,12,0.98)) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        min-width: 290px !important;
        max-width: 290px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* Sidebar collapse / expand arrow */
    button[title="Close sidebar"],
    button[title="Open sidebar"] {
        color: #eef2f9 !important;
    }

    button[title="Close sidebar"] svg,
    button[title="Open sidebar"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: #eef2f9 !important;
        stroke: #eef2f9 !important;
        color: #eef2f9 !important;
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
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        color: #dfe5ef;
        font-size: 0.86rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }

    .sidebar-label {
        color: #8f98a5;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .placeholder-row {
        color: #8f98a5;
        font-size: 0.95rem;
        padding: 0.55rem 0.2rem 0.2rem 0.2rem;
    }

    /* Main area */
    .main-shell {
        min-height: calc(100vh - 0.9rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.06);
        background:
            radial-gradient(circle at 50% 12%, rgba(255,255,255,0.03), transparent 16%),
            linear-gradient(180deg, rgba(6,9,14,0.97), rgba(4,7,11,0.99));
        box-shadow: 0 24px 90px rgba(0,0,0,0.5);
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

    .center-stage {
        min-height: calc(100vh - 2rem);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.4rem 1rem 0.8rem 1rem;
        position: relative;
    }

    .center-stage::before {
        content: "";
        position: absolute;
        top: 10%;
        left: 50%;
        transform: translateX(-50%);
        width: 42%;
        height: 22%;
        background: radial-gradient(circle, rgba(255,255,255,0.045), transparent 70%);
        filter: blur(16px);
        pointer-events: none;
    }

    .landing-wrap {
        width: 100%;
        max-width: 880px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 1;
    }

    .hero-logo {
        width: 88px;
        height: 88px;
        margin: 0 auto 0.85rem auto;
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
        filter: brightness(0) invert(1) opacity(0.97);
        transform: scale(1.72);
        transform-origin: center;
    }

    .hero-title {
        font-size: 2.35rem;
        line-height: 1.05;
        font-weight: 650;
        letter-spacing: -0.03em;
        color: #edf2f9;
        margin: 0 0 0.35rem 0;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8c95a2;
        margin: 0 0 1.05rem 0;
        text-align: center;
    }

    .chat-card {
        width: 100%;
        max-width: 880px;
        margin: 0 auto;
    }

    /* REAL input styling */
    div[data-testid="stForm"] {
        width: 100%;
        max-width: 880px;
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

    div[data-testid="stTextInputRootElement"] {
        width: 100%;
    }

    div[data-testid="stTextInputRootElement"] [data-baseweb="input"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 999px !important;
        box-shadow: none !important;
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

    .stFormSubmitButton > button {
        width: 100% !important;
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        color: #edf2f9 !important;
        padding: 0.9rem 1rem !important;
        box-shadow: none !important;
        font-weight: 700 !important;
        min-height: 58px !important;
        font-size: 1.1rem !important;
    }

    .stFormSubmitButton > button:hover {
        border-color: rgba(255,255,255,0.14) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02)) !important;
    }

    div[data-testid="column"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    div[data-testid="stChatMessage"] {
        background: transparent !important;
    }

    div[data-testid="stChatMessageContent"] {
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015)) !important;
        color: #edf2f9 !important;
    }

    .subtle-note {
        margin-top: 0.65rem;
        color: #68717d;
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
st.markdown('<div class="main-shell"><div class="center-stage"><div class="landing-wrap">', unsafe_allow_html=True)

if active_chat["messages"]:
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    for msg in active_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)
else:
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

with st.form("atlas_prompt_form", clear_on_submit=True):
    cols = st.columns([8.8, 1.4], gap="small")
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
        active_chat["messages"].append(
            {
                "role": "assistant",
                "content": f"Received: {text}\n\nThis is the placeholder response area for Atlas. Next we can wire this to your actual AI backend."
            }
        )
        st.rerun()

st.markdown('<div class="subtle-note">Atlas beta · cinematic operational AI shell</div>', unsafe_allow_html=True)
st.markdown('</div></div></div>', unsafe_allow_html=True)