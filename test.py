import streamlit as st
from streamlit_pages import greenspace

st.set_page_config(page_title = "Nature or New Yorker", layout = "centered")

with st.sidebar:
    st.title("Nature or New Yorker")
    page = st.radio("Select a page", ["Greenspace"])

if page == "Greenspace":
    greenspace.show()