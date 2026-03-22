import streamlit as st
import base64

# Page config
st.set_page_config(page_title="Atlas", layout="wide")

# Load logo
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64("atlas_logo_transparent.png")

# CSS styling (Aether-inspired)
st.markdown(f"""
<style>
body {{
    background: radial-gradient(circle at top, #1a1c22, #0b0c0f);
    color: #e5e7eb;
}}

.main {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}}

.center-box {{
    text-align: center;
    animation: fadeIn 1.5s ease-in-out;
}}

.logo {{
    width: 80px;
    margin-bottom: 20px;
    opacity: 0.9;
}}

.title {{
    font-size: 42px;
    font-weight: 600;
    color: #e5e7eb;
}}

.subtitle {{
    font-size: 18px;
    color: #9ca3af;
    margin-top: 10px;
}}

.input-box {{
    margin-top: 40px;
}}

.stTextInput > div > div > input {{
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    padding: 12px;
    border-radius: 10px;
}}

.stButton button {{
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 10px;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# UI
st.markdown(f"""
<div class="main">
    <div class="center-box">
        <img src="data:image/png;base64,{logo_base64}" class="logo"/>
        <div class="title">Good to see you.</div>
        <div class="subtitle">How can I assist you today?</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input area
user_input = st.text_input("", placeholder="Ask anything...")

if st.button("Send"):
    st.write(f"You said: {user_input}")