import streamlit as st
from queries.queries import get_name

def app(username: str, password: str):
    st.write(f"Admin Portal")