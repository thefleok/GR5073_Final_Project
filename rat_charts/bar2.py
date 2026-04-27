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
from rat_charts.data_loader import load_rats_2025

def bar2_chart():
    rats_2025 = load_rats_2025()

    BOROUGH_COLORS = {
        'BROOKLYN': '#2F3E46',
        'MANHATTAN': '#52796F',
        'QUEENS': '#84A98C',
        'BRONX': '#527588',
        'STATEN ISLAND': '#CAD2C5',
        'All NYC': '#354F52'
    }

    borough_counts = (rats_2025
        .groupby('borough').size()
        .reset_index(name='complaints')
        .query("borough != 'Unspecified'")
        .sort_values('complaints', ascending=False))

    chart2 = alt.Chart(borough_counts).mark_bar(
        cornerRadiusTopRight=3, cornerRadiusTopLeft=3
    ).encode(
        x=alt.X('borough:N', title=None, sort='-y',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('complaints:Q', title='Total Complaints (2020–2025)'),
        color=alt.Color('borough:N', legend=None,
                    scale=alt.Scale(
                        domain=list(BOROUGH_COLORS.keys()),
                        range=list(BOROUGH_COLORS.values())
                    )),
        tooltip=[alt.Tooltip('borough:N', title='Borough'),
                alt.Tooltip('complaints:Q', title='Complaints', format=',')]
    ).properties(
        width=500, height=350,
        title=alt.Title(
            '',
            subtitle=''))
    return chart2

    #title=alt.Title(
    #        'Total 311 Rodent Complaints by Borough (2020-2025)',
    #        subtitle='Source: NYC Open Data, 311 Service Requests'))