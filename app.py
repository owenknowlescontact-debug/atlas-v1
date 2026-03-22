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

# -----------------------------
# Session state
# -----------------------------
if "prompt_value" not in st.session_state:
    st.session_state.prompt_value = ""

if "submitted_prompt" not in st.session_state:
    st.session_state.submitted_prompt = ""

# -----------------------------
# Page styling
# -----------------------------
st.markdown(
    """
    <style>
    /* Hide Streamlit chrome */
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(255,255,255,0.055), transparent 20%),
            radial-gradient(circle at 22% 12%, rgba(255,255,255,0.02), transparent 16%),
            radial-gradient(circle at 78% 10%, rgba(255,255,255,0.018), transparent 16%),
            linear-gradient(180deg, #05070b 0%, #080b10 30%, #05070b 100%);
        color: #e7ebf1;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.6rem;
        padding-bottom: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* Top shell */
    .atlas-shell {
        min-height: calc(100vh - 1rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.07);
        background:
            linear-gradient(180deg, rgba(16,20,27,0.68), rgba(8,11,16,0.88)),
            radial-gradient(circle at 50% 0%, rgba(255,255,255,0.03), transparent 24%);
        overflow: hidden;
        box-shadow: 0 25px 90px rgba(0,0,0,0.42);
        backdrop-filter: blur(20px);
        position: relative;
    }

    .atlas-shell:before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.02) 50%, transparent 100%);
        mix-blend-mode: screen;
    }

    .atlas-topbar {
        height: 64px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1rem;
        background: rgba(6,8,12,0.52);
    }

    .atlas-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .atlas-brand-mark {
        width: 36px;
        height: 36px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015));
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .atlas-brand-title {
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        color: #edf1f7;
    }

    .atlas-top-pill {
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px;
        padding: 0.55rem 0.85rem;
        background: rgba(255,255,255,0.025);
        color: #dbe1e8;
        font-size: 0.83rem;
    }

    /* Layout */
    .atlas-grid {
        display: grid;
        grid-template-columns: 78px minmax(0, 1fr) 300px;
        min-height: calc(100vh - 64px - 1rem);
    }

    .atlas-rail {
        border-right: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(7,9,13,0.94), rgba(8,11,16,0.84));
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 1rem 0.7rem;
    }

    .atlas-rail-stack {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        align-items: center;
    }

    .atlas-rail-icon {
        width: 44px;
        height: 44px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.07);
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
        display: flex;
        align-items: center;
        justify-content: center;
        color: #d6dbe2;
        font-size: 1rem;
    }

    .atlas-rail-icon.active {
        border-color: rgba(255,255,255,0.16);
        background: linear-gradient(180deg, rgba(255,255,255,0.095), rgba(255,255,255,0.03));
        box-shadow: 0 10px 28px rgba(255,255,255,0.04);
    }

    .atlas-main {
        position: relative;
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        min-width: 0;
    }

    .atlas-main:before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(circle at 50% 10%, rgba(255,255,255,0.045), transparent 22%);
    }

    .atlas-hero-wrap {
        min-height: 68vh;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .atlas-hero-card {
        width: 100%;
        max-width: 720px;
        text-align: center;
        animation: fadeUp 0.45s ease;
        z-index: 1;
    }

    .atlas-hero-logo {
        width: 92px;
        height: 92px;
        margin: 0 auto 1.15rem auto;
        border-radius: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02));
        box-shadow:
            0 20px 60px rgba(0,0,0,0.35),
            0 0 40px rgba(255,255,255,0.03);
    }

    .atlas-hero-title {
        font-size: 3rem;
        line-height: 1.04;
        font-weight: 650;
        letter-spacing: -0.035em;
        color: #f0f3f8;
        margin-bottom: 0.8rem;
    }

    .atlas-hero-subtitle {
        font-size: 1.02rem;
        color: #98a1ad;
        max-width: 620px;
        margin: 0 auto 1.35rem auto;
    }

    .atlas-chip-label {
        color: #7d8591;
        font-size: 0.82rem;
        margin-bottom: 0.6rem;
    }

    .atlas-composer-shell {
        margin: 0 auto;
        width: 100%;
        max-width: 760px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.016));
        padding: 0.95rem 1rem 1rem 1rem;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.02),
            0 12px 40px rgba(0,0,0,0.2);
    }

    .atlas-composer-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #97a0ab;
        font-size: 0.8rem;
        margin-bottom: 0.7rem;
    }

    .atlas-live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #b8d6ff;
        display: inline-block;
        margin-right: 0.45rem;
        box-shadow: 0 0 12px rgba(184,214,255,0.5);
    }

    .atlas-suggestions {
        margin-top: 0.8rem;
    }

    .atlas-right {
        border-left: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(8,10,15,0.9), rgba(9,12,17,0.78));
        padding: 1rem;
    }

    .atlas-panel-title {
        font-size: 1rem;
        font-weight: 600;
        color: #eef2f7;
        margin-bottom: 0.9rem;
    }

    .atlas-insight-card {
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
        padding: 1rem;
        margin-bottom: 0.85rem;
    }

    .atlas-metric-label {
        color: #98a1ad;
        font-size: 0.82rem;
        margin-bottom: 0.35rem;
    }

    .atlas-metric-value {
        color: #eef2f7;
        font-size: 1.55rem;
        font-weight: 650;
        letter-spacing: -0.02em;
    }

    .atlas-mini-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.72rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #dbe1e8;
        font-size: 0.92rem;
    }

    .atlas-mini-row:last-child {
        border-bottom: none;
    }

    .atlas-mini-value {
        color: #eef3f8;
    }

    .atlas-footer-note {
        margin-top: 0.8rem;
        text-align: center;
        color: #737c88;
        font-size: 0.76rem;
    }

    /* Inputs */
    div[data-testid="stTextInputRootElement"] > div {
        background: transparent !important;
    }

    div[data-testid="stTextInputRootElement"] input {
        background: rgba(255,255,255,0.03) !important;
        color: #edf1f7 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 0.95rem 1rem !important;
        font-size: 0.98rem !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInputRootElement"] input::placeholder {
        color: #87909b !important;
    }

    .stButton > button {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.018)) !important;
        color: #edf1f7 !important;
        padding: 0.72rem 1rem !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        border-color: rgba(255,255,255,0.16) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)) !important;
        color: #ffffff !important;
    }

    div.stSelectbox > div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    div.stSelectbox * {
        color: #eef2f7 !important;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(14px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 1100px) {
        .atlas-grid {
            grid-template-columns: 74px minmax(0, 1fr);
        }
        .atlas-right {
            display: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Top shell
# -----------------------------
st.markdown('<div class="atlas-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="atlas-topbar">
        <div class="atlas-brand">
            <div class="atlas-brand-mark">
    """,
    unsafe_allow_html=True,
)

if logo_base64:
    st.markdown(
        f'<img src="data:image/png;base64,{logo_base64}" width="22" />',
        unsafe_allow_html=True,
    )
else:
    st.markdown("A", unsafe_allow_html=True)

st.markdown(
    """
            </div>
            <div class="atlas-brand-title">Atlas</div>
        </div>
        <div class="atlas-top-pill">Operational Intelligence</div>
    </div>
    """,
    unsafe_allow_html=True,
)

rail_col, main_col, right_col = st.columns([1.1, 8.7, 3.2], gap="small")

# -----------------------------
# Left rail
# -----------------------------
with rail_col:
    st.markdown('<div class="atlas-rail">', unsafe_allow_html=True)

    st.markdown('<div class="atlas-rail-stack">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-rail-icon active">✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="atlas-rail-icon">⌂</div>', unsafe_allow_html=True)
    st.markdown('<div class="atlas-rail-icon">⟲</div>', unsafe_allow_html=True)
    st.markdown('<div class="atlas-rail-icon">⌕</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlas-rail-stack">', unsafe_allow_html=True)
    if logo_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" width="34" />',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="atlas-rail-icon">A</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Main center
# -----------------------------
with main_col:
    st.markdown('<div class="atlas-main">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-hero-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-hero-card">', unsafe_allow_html=True)

    st.markdown('<div class="atlas-hero-logo">', unsafe_allow_html=True)
    if logo_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" width="54" />',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("A", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="atlas-hero-title">Good to see you.<br>How can Atlas assist?</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="atlas-hero-subtitle">Your operational intelligence copilot for opportunity sizing, labor signals, VCPU trends, DEA risk, and fast network-level answers.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="atlas-composer-shell">', unsafe_allow_html=True)
    st.markdown(
        '<div class="atlas-composer-meta"><div>◌ Atlas shell is live and ready for data wiring.</div><div><span class="atlas-live-dot"></span>Active intelligence layer</div></div>',
        unsafe_allow_html=True,
    )

    user_input = st.text_input(
        "",
        value=st.session_state.prompt_value,
        placeholder="Ask anything...",
        label_visibility="collapsed",
        key="atlas_input",
    )

    if user_input:
        st.session_state.submitted_prompt = user_input

    chip_cols = st.columns([1, 1, 1, 1])
    with chip_cols[0]:
        if st.button("Top opportunity sites"):
            st.session_state.submitted_prompt = "Top opportunity sites last week"
    with chip_cols[1]:
        if st.button("High missing units"):
            st.session_state.submitted_prompt = "Summary of high missing units"
    with chip_cols[2]:
        if st.button("VCPU trend"):
            st.session_state.submitted_prompt = "Trend of VCPU by site"
    with chip_cols[3]:
        if st.button("DEA risks"):
            st.session_state.submitted_prompt = "Summarize DEA risks by building"

    if st.session_state.submitted_prompt:
        st.markdown(
            f"""
            <div style="
                margin-top: 0.9rem;
                text-align: left;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.018));
                padding: 0.95rem 1rem;">
                <div style="font-size:0.8rem;color:#8d96a2;margin-bottom:0.35rem;">Latest prompt</div>
                <div style="font-size:1rem;color:#eef2f7;">{st.session_state.submitted_prompt}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="atlas-footer-note">Atlas shell v2 · Silver cinematic interface foundation</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Right panel
# -----------------------------
with right_col:
    st.markdown('<div class="atlas-right">', unsafe_allow_html=True)

    st.markdown('<div class="atlas-panel-title">Insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlas-insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-metric-label">Selected Site</div>', unsafe_allow_html=True)
    st.selectbox(
        "Site",
        ["All Sites", "SAZ2", "SVA2", "SDF1", "SFL1", "SA22"],
        label_visibility="collapsed",
        key="site_selector",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlas-insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-metric-label">Labor Hours</div>', unsafe_allow_html=True)
    st.markdown('<div class="atlas-metric-value">16.2K</div>', unsafe_allow_html=True)
    st.caption("Rolling 7-day operational estimate")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlas-insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-metric-label">Top Opportunity Sites</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="atlas-mini-row"><span>SVA2</span><span class="atlas-mini-value">$94.6K</span></div>
        <div class="atlas-mini-row"><span>SDF1</span><span class="atlas-mini-value">$83.3K</span></div>
        <div class="atlas-mini-row"><span>SA22</span><span class="atlas-mini-value">$63.2K</span></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlas-insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="atlas-metric-label">System State</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="atlas-mini-row"><span>Model Layer</span><span class="atlas-mini-value">Online</span></div>
        <div class="atlas-mini-row"><span>Data Source</span><span class="atlas-mini-value">Pending Athena</span></div>
        <div class="atlas-mini-row"><span>Prompt Cache</span><span class="atlas-mini-value">Ready</span></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)