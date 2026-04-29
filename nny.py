import streamlit as st
from streamlit_pages import home, project, greenspace, rodents, squirrels

st.set_page_config(page_title = "Nature or New Yorker", layout = "centered")

with st.sidebar:
    st.title("Nature or New Yorker")
    page = st.radio("Select a page", ["Home", "About the Project", "Greenspace", "Rodents", "Squirrels"])

if page == "Home":
    home.show()
elif page == "About the Project":
    project.show()
elif page == "Greenspace":
    greenspace.show()
elif page == "Rodents":
    rodents.show()
elif page == "Squirrels":
    squirrels.show()