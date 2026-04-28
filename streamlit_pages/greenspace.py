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
    st.markdown("### High Level Map: Overview of Parks and Greenspaces")

    chart3 = parks_housing_chart()
    st_folium(chart3, width = 700, height = 500)

    st.markdown("This map shows the different parks and greenspaces (including" \
    " recreation areas, gardens, and waterfront areas) around NYC, as well as " \
    "the top 5 rarest trees (the Virginia pine, black pine, Scots pine, Osage-orange,"
    " and European alder) that were living and healthy according to the 2015 Tree " \
    "Census. Parkways, buildings, and playgrounds were excluded.")




    # introduction to second graph
    st.markdown("### Interactive Map: When NYC Parks were Established")
    
    chart2 = parks_time_chart()
    st_folium(chart2, width = 700, height = 500)

    st.markdown("This map shows the dates when certain parks and green spaces were established "
    "in New York City. Prior to 1873, there was a push for more green spaces in New York City to" \
    " help mitigate the effects of communicable diseases. For example, the development of Central" \
    " Park began in around 1858 to offset poor industrial living standards. The City Beautiful" \
    " movement followed, which attempted to further enhance the natural design of New York " \
    "City. Robert Moses’ later influence cannot be understated: swimming pools, parkways, "
    "and new parks and infrastructure popped up all over the city. Then the 1975 fiscal crisis" \
    " created conditions where greenspaces were not prioritized. More recently, the focus has " \
    "been on the climate, as well as green living areas pricing out previous residents (the" \
    "green gentrification).")

    

    # show third map
    st.markdown("### Graph 3: Affordable housing, distance from green spaces")
    chart1 = park_types_chart()
    st_folium(chart1, width = 700, height = 500)
    st.markdown("This map shows the typical “park” parks (including flagship parks, like Central " \
    "Park, community parks, and neighborhood parks) and housing projects which contained at least 20 percent " \
    "low- to extremely-low-income units completed in the second half of 2025. This map also demonstrates the " \
    "distance from each low-income housing unit to its nearest park. The average distance from low-income housing" \
    " to a park is about a **quarter mile**.")

    


    st.markdown("### Park Accessibility Map")
    chart4 = parks_accessibility_chart()
    st_folium(chart4, width = 700, height = 500)
    st.markdown("This map utilizes a 2x2 bivariate matrix to analyze the intersection of population density and green " \
    "space coverage (the percentage of parkland within a census tract). By splitting both variables at their city-wide" \
    " medians, we categorize NYC neighborhoods into four distinct archetypes. The most critical areas are the 'Park " \
    "Deserts', where high residential density meets minimal green infrastructure, signaling potential environmental " \
    "injustice. Conversely, the 'Integrated Excellence' zones represent successful urban planning where high density is " \
    "balanced with significant park access. All data has been clipped to land boundaries to ensure spatial accuracy and " \
    "exclude non-residential water areas.")