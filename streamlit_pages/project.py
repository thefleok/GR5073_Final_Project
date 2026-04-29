import streamlit as st

def show():
    st.markdown("# Project Motivation")
    st.markdown("""
    Enthusiastic New Yorkers embrace what is colloquially referred to as the "concrete jungle". 
    Constantly facing buildings, street noise, and apartment buildings, their natural or humanistic 
    life is often sacrificed at the expense of a vibrant and cultural city. 

    In this analysis, we set out to try and tell a data-driven story about whether New Yorkers 
    are truly inhabitants of a "concrete jungle" or if there are ample opportunities to still 
    engage with wildlife. In our consideration of parks, we try to understand (from a mapping 
    perspective) the prevalence of parks in New York. In our consideration of rodents and squirrels, 
    we try to understand how much these city environments are corrupted by rodents and less 
    pleasurable living acquaintances.
    """)

    st.markdown("# Methodology")
    st.markdown("""
    We utilized geospatial and text analysis to answer these questions: 
    1) The location and establishment of parks, greenspaces, and trees around the city, and their accessibility for residents;  
    2) Rodent complaints by borough, zip code, and transportation lines and their relationship to demographic factors; 
    3) Central Park squirrel sightings, including text analysis of the Squirrel Census.
    """)

    st.markdown("# Data Sources")
    st.markdown("- Department of Parks and Recreation (DPR) Parks Properties (NYC OpenData)\n"
                "- Department of Housing Preservation and Development (HPD) Affordable Housing Production by Building (NYC OpenData)\n"
                "- Department of Parks and Recreation (DPR) 2015 Street Tree Census - Tree Data (NYC OpenData)\n"
                "- New York City Housing Authority (NYCHA) NYCHA Public Housing Developments (NYC OpenData)\n"
                "- Department of Parks and Recreation (DPR) Parks Zones (NYC OpenData)\n"
                "- Department of City Planning (DCP) Borough Boundaries Dataset (NYC OpenData)\n"
                "- United States Census Bureau 2025 TIGER/Line® Shapefiles\n"
                "- United States Census Bureau American Community Survey 5-Year Data\n"
                "- NYU Spatial Data Repository 2016 NYC Subway Routes\n"
                "- Department of City Planning (DCP) 2020 Neighborhood Tabulation Areas (NTAs)\n"
                "- Metropolitan Transportation Authority MTA Subway Stations\n"
                "- The Squirrel Census 2018 Central Park Squirrel Census\n"
                "- 311 Service Requests from 2020 to Present\n"
                "- Department of Buildings (DOB) DOB NOW: Build – Approved Permits\n"
                "- Department of Health and Mental Hygiene (DOHMH) Restaurant Inspection Results"
                )