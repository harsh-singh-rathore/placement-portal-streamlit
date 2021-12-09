import streamlit as st
from queries.queries import get_name, get_all_companies, get_elligible_companies

def app(username: str, password: str):
    st.write(f"Hello, {get_name(username=username)}")
    option = 'All Companies'
    option = st.selectbox(
        'Filter',
        ('All Companies', 'Elligible'))
    if option == 'All Companies':
        st.write(get_all_companies())
    elif option == 'Elligible':
        st.write(get_elligible_companies(username))
    st.text_input('Apply to job_id')
