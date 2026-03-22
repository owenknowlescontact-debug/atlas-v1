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
if "search_placeholder" not in st.session_state:
    st.session_state.search_placeholder = ""
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

    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(180,190,210,0.06), transparent 16%),
            radial-gradient(circle at 50% 16%, rgba(255,255,255,0.025), transparent 12%),
            linear-gradient(180deg, #04070b 0%, #060910 45%, #04070b 100%);
        color: #e9edf5;
    }

    .block-container {
        padding-top: 0.6rem;
        padding-bottom: 0.7rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        max-width: 100%;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(9,12,18,0.98), rgba(6,8,12,0.98)) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        min-width: 280px !important;
        max-width: 280px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.75rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.9rem;
    }

    .brand-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 36px;
        padding: 0.34rem 0.8rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        color: #dfe5ef;
        font-size: 0.84rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }

    .brand-pill.beta {
        font-size: 0.8rem;
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

    .main-shell {
        min-height: calc(100vh - 1.3rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.06);
        background:
            radial-gradient(circle at 50% 12%, rgba(255,255,255,0.03), transparent 16%),
            linear-gradient(180deg, rgba(6,9,14,0.97), rgba(4,7,11,0.99));
        box-shadow: 0 24px 90px rgba(0,0,0,0.5);
        overflow: hidden;
        position: relative;
    }

    .main-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.012) 50%, transparent 100%);
        mix-blend-mode: screen;
    }

    .main-top {
        height: 58px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex;
        align-items: center;
        padding: 0 1rem;
        color: #e9edf5;
        font-weight: 600;
        background: rgba(4,6,10,0.35);
    }

    .landing-wrap {
        width: 100%;
        max-width: 920px;
        margin: 0 auto;
        padding-top: 6vh;
        padding-bottom: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .hero-logo {
        width: 88px;
        height: 88px;
        margin: 0 auto 0.9rem auto;
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
        transform: scale(1.6);
        transform-origin: center;
    }

    .hero-title {
        font-size: 2.35rem;
        line-height: 1.06;
        font-weight: 650;
        letter-spacing: -0.03em;
        color: #edf2f9;
        margin: 0 0 0.35rem 0;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8c95a2;
        margin: 0 0 1rem 0;
        text-align: center;
    }

    div[data-testid="stTextInputRootElement"] > div {
        background: transparent !important;
    }

    div[data-testid="stTextInputRootElement"] input {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        -webkit-text-fill-color: #edf2f9 !important;
        color: #edf2f9 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 999px !important;
        padding: 1rem 1.15rem !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        min-height: 58px !important;
        opacity: 1 !important;
    }

    div[data-testid="stTextInputRootElement"] input::placeholder {
        color: #9aa3af !important;
        -webkit-text-fill-color: #9aa3af !important;
        opacity: 1 !important;
    }

    .stButton > button,
    .stFormSubmitButton > button,
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border-radius: 999px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)) !important;
        color: #edf2f9 !important;
        padding: 0.9rem 1rem !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        min-height: 50px !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        border-color: rgba(255,255,255,0.14) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02)) !important;
    }

    .chat-card {
        width: 100%;
        max-width: 880px;
        margin: 0 auto;
        padding-bottom: 0.6rem;
    }

    .subtle-note {
        margin-top: 0.7rem;
        color: #68717d;
        font-size: 0.76rem;
        text-align: center;
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

    div[data-testid="column"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .placeholder-row {
        color: #8f98a5;
        font-size: 0.95rem;
        padding: 0.65rem 0.2rem 0.2rem 0.2rem;
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
            <div class="brand-pill beta">BETA</div>
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

# Refresh active chat after potential rerun operations
active_index = get_chat_index(st.session_state.active_chat_id)
active_chat = st.session_state.chats[active_index]

# -------------------------------------------------
# Main
# -------------------------------------------------
st.markdown('<div class="main-shell">', unsafe_allow_html=True)
st.markdown('<div class="main-top">Atlas</div>', unsafe_allow_html=True)

# Show messages if chat has content
if active_chat["messages"]:
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    for msg in active_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)

    if logo_base64:
        st.markdown(
            f'''
            <div class="hero-logo">
                <img src="data:image/png;base64,{logo_base64}" width="60" />
            </div>
            ''',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="hero-title">Good to see you.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">How can I assist you today?</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.form("atlas_prompt_form", clear_on_submit=True):
    cols = st.columns([8.7, 1.6], gap="small")
    with cols[0]:
        user_input = st.text_input(
            "",
            placeholder="Ask anything...",
            label_visibility="collapsed",
        )
    with cols[1]:
        submitted = st.form_submit_button("Send")

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
st.markdown('</div>', unsafe_allow_html=True)