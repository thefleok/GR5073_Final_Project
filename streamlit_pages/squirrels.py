import streamlit as st
from streamlit_folium import st_folium
from squirrel_charts.maps import maps_chart
from squirrel_charts.words import words_chart
from squirrel_charts.behavior import behavior_chart

def show():
    st.markdown("# NYC Parks and Greenspaces")
    st.markdown("The parks and greenspaces (and rare trees!) around NYC are discussed " \
    "in this mapping. We include interactive map visualizations that capture the evolution " \
    "of parks over time and their benefits for the citizens of NYC (proximity to affordable " \
    "housing, tree density, etc.).")



    chart1 = words_chart()
    st.pyplot(chart1)

    # introduction to first graph
    st.markdown("### Graph 2: Squirrel Map")

    chart2 = maps_chart()
    st_folium(chart2, width = 700, height = 500)

    chart3 = behavior_chart()
    st.altair_chart(chart3)