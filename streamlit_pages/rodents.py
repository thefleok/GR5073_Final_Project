import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import altair as alt
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

def show():
    chart1 = behavior_chart()
    st.pyplot(chart1)