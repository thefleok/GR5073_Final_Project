import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import altair as alt


from streamlit_folium import st_folium
from rat_charts.bar3 import bar3_chart
alt.data_transformers.disable_max_rows()
import geopandas as gpd
import json
import folium
from folium.plugins import GroupedLayerControl
import branca.colormap as cm
import requests
import networkx as nx
from pyvis.network import Network
from rat_charts.line1 import behavior_chart
from rat_charts.bar2 import bar2_chart
from rat_charts.bar3 import bar3_chart
from rat_charts.map4 import map_chart4
from rat_charts.scatter5 import scatter5_chart
from rat_charts.heat6 import heat6_chart
from rat_charts.scatter7 import scatter7_chart

def show():
    st.markdown("# Rodents in NYC")
    st.markdown("### Line plot: 311 complaints by borough over time")
    chart1 = behavior_chart()
    st.altair_chart(chart1)
    st.markdown("NYC rodent complaints follow a seasonal cycle, peaking each summer and dipping in winter." \
    " Complaints surged from 2020 through mid-2022, reaching a high ~4,500 in a single month. Following the " \
    "appointment of NYC’s ‘rat czar’ in April 2023 and a series of trash containerization mandates, the summer" \
    " peaks have gradually declined. The 2025 peak came in noticeably lower than those of 2022 and 2023, suggesting t" \
    "he city’s multi-pronged intervention may be having an effect.")

    st.markdown("### Bar Chart: 311 complaints by borough")
    chart2 = bar2_chart()
    st.altair_chart(chart2)
    st.markdown("Brooklyn dominates with over 80,000 rodent complaints since 2020, accounting for nearly 40 percent of" \
    " all reports citywide. Manhattan follows with roughly 58,000, consistent with its high population density and " \
    "concentration of food establishments. Queens and the Bronx report similar complaint volumes despite significant " \
    "differences in population size and urban character. Staten Island, the citys most suburban borough, accounts for " \
    "just 3 percent of complaints.")


    st.markdown("### Faceted Bar Chart: 311 Complaints by Type by Borough")
    chart3 = bar3_chart()
    st.altair_chart(chart3)
    st.markdown("Rat sightings make up the majority of complaints across all five boroughs. However, the proportional " \
    "breakdown varies. Staten Island stands out with a notably higher share of ‘Condition Attracting Rodents’ reports " \
    "relative to actual sightings, suggesting residents there are more likely to flag environmental conditions like loose " \
    "garbage rather than spotting rats directly. Mouse sightings are concentrated in the Bronx and Manhattan, consistent with " \
    "their higher density of apartment buildings where mice are more commonly encountered indoors.")
    

    st.markdown("### Chlorpleth: Rodent complaints by zipcode (per 1000 residents)")
    chart4 = map_chart4()
    st_folium(chart4)
    st.markdown("This map demonstrates rat complaints, restaurant violations, and construction permits per 1,000 residents " \
    "across zip codes in the 5 NYC boroughs. From this map, we can see high-density rat complaint locations include upper Manhattan"
    " and areas in Brooklyn, whereas restaurant violations and construction seem to be happening mainly in mid- and downtown Manhattan.")

    st.markdown("### Scatterplot: 311 complaints by zipcode vs. restaurant/construction factors (per 1000 residents)")
    chart5 = scatter5_chart()
    st.altair_chart(chart5)
    st.markdown("This interactive scatterplot allows you to dive deeper into how construction sites and restaurant violations may be related to 311 rat complaints!")

    st.markdown("### Heatmap:311 complaint density with MTA and NYCHA")
    chart6 = heat6_chart()
    st_folium(chart6)
    st.markdown("This heatmap highlights the density of rat complaints across New York City. The interactive feature allows you to examine rat complaint density along" \
    " subway lines, MTA stations, and near low-income housing. Note the high density in Western Queens.")

    st.markdown("### Scatterplot: 311 complaints by zipcode vs. demographic factors (per 1000 residents)")
    chart7 = scatter7_chart()
    st.altair_chart(chart7)
    st.markdown("What other factors might influence 311 rat complaints, and who is more likely to make 311 rat complaints? Use this interactive scatterplot to " \
    "investigate demographic differences in 311 rat complaints by borough.")