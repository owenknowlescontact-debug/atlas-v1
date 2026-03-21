import streamlit as st

st.set_page_config(page_title="Atlas V1", page_icon="📊", layout="wide")

st.title("Atlas V1 - SSD Ops Assistant")
st.write("Ask a question about your site performance.")

query = st.text_input("Enter your question")

if query:
    st.write(f"You asked: {query}")
    st.success("Atlas is working 🚀")
else:
    st.info("Try asking: What's my worst site this week?")