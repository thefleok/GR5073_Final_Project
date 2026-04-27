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

def show():
    st.markdown("# Rodents in NYC")
    st.markdown("### 311 complaints by borough over time")
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


    st.markdown("###")
    chart3 = bar3_chart()
    st.altair_chart(chart3)
    

    st.markdown("### see below")
    chart4 = map_chart4()
    st_folium(chart4)
    st.markdown("see above")

    st.markdown("### see below")
    chart5 = scatter5_chart()
    st.altair_chart(chart5)
    st.markdown("see above")