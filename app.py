import streamlit as st
import pandas as pd
import boto3

st.title("Atlas V1 - SSD Ops Assistant")

st.write("Ask a question about your site performance:")

query = st.text_input("Enter your question")

if query:
    st.write(f"You asked: {query}")

    # Placeholder response (we will connect Athena next)
    st.success("Atlas is working 🚀")