import streamlit as st
from streamlit_pages import home, motivation, greenspace, rodents, squirrels

st.set_page_config(page_title = "Nature or New Yorker", layout = "centered")

with st.sidebar:
    st.title("Nature or New Yorker")
    page = st.radio("Select a page", ["Home", "Project Motivation", "Greenspace", "Rodents", "Squirrels"])

if page == "Home":
    home.show()
elif page == "Project Motivation":
    motivation.show()
elif page == "Greenspace":
    greenspace.show()
elif page == "Rodents":
    rodents.show()
elif page == "Squirrels":
    squirrels.show()