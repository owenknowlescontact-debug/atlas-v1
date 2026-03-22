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

if "submitted_prompt" not in st.session_state:
    st.session_state.submitted_prompt = ""

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(140,150,170,0.08), transparent 16%),
            radial-gradient(circle at 20% 10%, rgba(255,255,255,0.025), transparent 12%),
            radial-gradient(circle at 80% 10%, rgba(255,255,255,0.02), transparent 12%),
            linear-gradient(180deg, #06080c 0%, #090d14 35%, #06080c 100%);
        color: #e8edf5;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.6rem;
        padding-bottom: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .shell {
        min-height: calc(100vh - 1rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.06);
        background:
            linear-gradient(180deg, rgba(10,13,19,0.92), rgba(7,9,14,0.96)),
            radial-gradient(circle at 50% 0%, rgba(255,255,255,0.02), transparent 22%);
        overflow: hidden;
        box-shadow: 0 24px 90px rgba(0,0,0,0.45);
        position: relative;
    }

    .shell::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 50% 14%, rgba(255,255,255,0.05), transparent 18%),
            linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.012) 50%, transparent 100%);
        mix-blend-mode: screen;
    }

    .topbar {
        height: 62px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1rem;
        background: rgba(4,6,10,0.45);
    }

    .left-top {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }

    .beta-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.38rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        color: #d9e0ea;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .brand-title {
        color: #eef2f8;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }

    .layout {
        display: grid;
        grid-template-columns: 74px minmax(0, 1fr) 290px;
        min-height: calc(100vh - 62px - 1rem);
    }

    .rail {
        border-right: 1px solid rgba(255,255,255,0.05);
        background: linear-gradient(180deg, rgba(7,9,14,0.95), rgba(8,11,17,0.88));
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 1rem 0.65rem;
    }

    .rail-stack {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        align-items: center;
    }

    .rail-icon {
        width: 42px;
        height: 42px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
        color: #d7dde5;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .rail-icon.active {
        border-color: rgba(255,255,255,0.14);
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.025));
        box-shadow: 0 10px 30px rgba(255,255,255,0.035);
    }

    .main {
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        position: relative;
        min-width: 0;
    }

    .main::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 50% 14%, rgba(255,255,255,0.04), transparent 18%);
    }

    .hero-wrap {
        min-height: 70vh;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .hero {
        width: 100%;
        max-width: 760px;
        text-align: center;
        z-index: 1;
    }

    .hero-logo {
        width: 86px;
        height: 86px;
        margin: 0 auto 1.1rem auto;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow:
            0 18px 50px rgba(0,0,0,0.32),
            0 0 30px rgba(255,255,255,0.02);
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.05;
        font-weight: 650;
        letter-spacing: -0.035em;
        color: #eef2f8;
        margin-bottom: 0.75rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8f98a4;
        margin-bottom: 1.25rem;
    }

    .composer {
        width: 100%;
        max-width: 760px;
        margin: 0 auto;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
        padding: 0.85rem 1rem 1rem 1rem;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.02),
            0 12px 36px rgba(0,0,0,0.2);
    }

    .composer-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #8f98a4;
        font-size: 0.79rem;
        margin-bottom: 0.7rem;
    }

    .live {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #72d36f;
        box-shadow: 0 0 10px rgba(114,211,111,0.45);
    }

    .chips-note {
        color: #707987;
        font-size: 0.74rem;
        text-align: center;
        margin-top: 0.75rem;
    }

    .right {
        border-left: 1px solid rgba(255,255,255,0.05);
        background: linear-gradient(180deg, rgba(7,9,14,0.92), rgba(8,11,17,0.84));
        padding: 1rem;
    }

    .panel-title {
        color: #eef2f8;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.9rem;
    }

    .card {
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
        padding: 1rem;
        margin-bottom: 0.85rem;
    }

    .metric-label {
        color: #96a0ac;
        font-size: 0.82rem;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #eef2f8;
        font-size: 1.5rem;
        font-weight: 650;
        letter-spacing: -0.02em;
    }

    .mini-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.72rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #dbe1e9;
        font-size: 0.92rem;
    }

    .mini-row:last-child {
        border-bottom: none;
    }

    .mini-value {
        color: #f0f4f9;
    }

    .footer-note {
        text-align: center;
        margin-top: 0.8rem;
        color: #68707c;
        font-size: 0.76rem;
    }

    div[data-testid="stTextInputRootElement"] > div {
        background: transparent !important;
    }

    div[data-testid="stTextInputRootElement"] input {
        background: rgba(255,255,255,0.035) !important;
        color: #eef2f8 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 0.95rem 1rem !important;
        font-size: 0.98rem !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInputRootElement"] input::placeholder {
        color: #8b94a0 !important;
    }

    .stButton > button {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015)) !important;
        color: #eaf0f8 !important;
        padding: 0.68rem 0.95rem !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        border-color: rgba(255,255,255,0.14) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02)) !important;
    }

    div.stSelectbox > div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    div.stSelectbox * {
        color: #eef2f8 !important;
    }

    @media (max-width: 1100px) {
        .layout {
            grid-template-columns: 74px minmax(0, 1fr);
        }
        .right {
            display: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Shell start
# -----------------------------
st.markdown('<div class="shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="topbar">
        <div class="left-top">
            <div class="beta-pill">BETA</div>
            <div class="brand">
                <div class="brand-mark">
    """,
    unsafe_allow_html=True,
)

if logo_base64:
    st.markdown(
        f'<img src="data:image/png;base64,{logo_base64}" width="20" />',
        unsafe_allow_html=True,
    )
else:
    st.markdown("A", unsafe_allow_html=True)

st.markdown(
    """
                </div>
                <div class="brand-title">Atlas</div>
            </div>
        </div>
        <div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

rail_col, main_col, right_col = st.columns([1.05, 8.8, 3.0], gap="small")

with rail_col:
    st.markdown('<div class="rail">', unsafe_allow_html=True)
    st.markdown('<div class="rail-stack">', unsafe_allow_html=True)
    st.markdown('<div class="rail-icon active">✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="rail-icon">⌂</div>', unsafe_allow_html=True)
    st.markdown('<div class="rail-icon">⟲</div>', unsafe_allow_html=True)
    st.markdown('<div class="rail-icon">⌕</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rail-stack">', unsafe_allow_html=True)
    if logo_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" width="32" />',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main_col:
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="hero-wrap"><div class="hero">', unsafe_allow_html=True)

    st.markdown('<div class="hero-logo">', unsafe_allow_html=True)
    if logo_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" width="48" />',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-title">Good to see you.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">How can I assist you today?</div>', unsafe_allow_html=True)

    st.markdown('<div class="composer">', unsafe_allow_html=True)
    st.markdown(
        '<div class="composer-top"><div>Unlock more Atlas capabilities as the intelligence layer expands.</div><div class="live"><span class="live-dot"></span><span>Active extensions</span></div></div>',
        unsafe_allow_html=True,
    )

    user_input = st.text_input(
        "",
        placeholder="Ask anything...",
        label_visibility="collapsed",
        key="atlas_prompt",
    )

    chip_cols = st.columns([1, 1, 1, 0.45])
    with chip_cols[0]:
        st.button("Any advice for me?")
    with chip_cols[1]:
        st.button("Some Youtube video idea")
    with chip_cols[2]:
        st.button("Life lessons from kratos")
    with chip_cols[3]:
        st.button("⋯")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer-note">Atlas beta · operational intelligence shell</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="right">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Selected Site</div>', unsafe_allow_html=True)
    st.selectbox(
        "Site",
        ["All Sites", "SAZ2", "SVA2", "SDF1", "SFL1", "SA22"],
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Labor Hours</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">16.2K</div>', unsafe_allow_html=True)
    st.caption("Rolling 7-day operational estimate")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Top Opportunity Sites</div>', unsafe_allow_html=True)
    st.markdown(
        '''
        <div class="mini-row"><span>SVA2</span><span class="mini-value">$94.6K</span></div>
        <div class="mini-row"><span>SDF1</span><span class="mini-value">$83.3K</span></div>
        <div class="mini-row"><span>SA22</span><span class="mini-value">$63.2K</span></div>
        ''',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)