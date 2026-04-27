import streamlit as st
from streamlit_folium import st_folium
from charts.park_types import park_types_chart
from charts.parks_time import parks_time_chart
from charts.parks_housing import parks_housing_chart
from charts.parks_accessibility import parks_accessibility_chart

def show():
    st.markdown("# NYC Parks and Greenspaces")
    st.markdown("The parks and greenspaces (and rare trees!) around NYC are discussed " \
    "in this mapping. We include interactive map visualizations that capture the evolution " \
    "of parks over time and their benefits for the citizens of NYC (proximity to affordable " \
    "housing, tree density, etc.).")


    # introduction to first graph
    st.markdown("### Graph 1: Overview of parks and greenspaces")

    chart1 = park_types_chart()
    st_folium(chart1, width = 700, height = 500)

    st.markdown("This map shows the different parks and greenspaces (including" \
    " recreation areas, gardens, and waterfront areas) around NYC, as well as " \
    "the top 5 rarest trees (the Virginia pine, black pine, Scots pine, Osage-orange,"
    " and European alder) that were living and healthy according to the 2015 Tree " \
    "Census. Parkways, buildings, and playgrounds were excluded.")




    # introduction to second graph
    st.markdown("### Graph 2: When NYC Parks were Established")
    
    chart2 = parks_time_chart()
    st_folium(chart2, width = 700, height = 500)

    st.markdown("This map shows the dates when all of New York City’s parks were " \
    "established to date, divided into five main periods, illustrating the guiding " \
    "principles behind the city’s development during different historical phases.")

    

    # show third map
    st.markdown("### Graph 3: Affordable housing, distance from green spaces")
    chart3 = parks_housing_chart()
    st_folium(chart3, width = 700, height = 500)



    chart4 = parks_accessibility_chart()
    st_folium(chart4, width = 700, height = 500)