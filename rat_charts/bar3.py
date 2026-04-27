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

def bar3_chart():
    rats_2025 = load_rats_2025()

    DESCRIPTOR_COLORS = {
        'Rat Sighting': '#2F3E46',
        'Condition Attracting Rodents': '#52796F',
        'Signs of Rodents': '#527588',
        'Mouse Sighting': '#84A98C'
    }
    BOROUGH_COLORS = {
        'BROOKLYN': '#2F3E46',
        'MANHATTAN': '#52796F',
        'QUEENS': '#84A98C',
        'BRONX': '#527588',
        'STATEN ISLAND': '#CAD2C5',
        'All NYC': '#354F52'
    }

    # Chart 3: Complaint Type by Borough (Faceted)

    descriptor_borough = (rats_2025
        .query("borough != 'Unspecified' and descriptor != 'Rodent Bite - PCS Only'")
        .groupby(['borough', 'descriptor']).size()
        .reset_index(name='complaints'))

    # Consistent color map for descriptors
    descriptor_colors = {
        'Rat Sighting': '#e41a1c',
        'Condition Attracting Rodents': '#ff7f00',
        'Signs of Rodents': '#984ea3',
        'Mouse Sighting': '#377eb8'}

    chart3 = alt.Chart(descriptor_borough).mark_bar().encode(
        x=alt.X('complaints:Q', title='Number of Complaints'),
        y=alt.Y('descriptor:N', title=None, sort='-x'),
        color=alt.Color('descriptor:N', title='Complaint Type',
                    scale=alt.Scale(
                        domain=list(DESCRIPTOR_COLORS.keys()),
                        range=list(DESCRIPTOR_COLORS.values())
                    )),
        tooltip=[alt.Tooltip('borough:N', title='Borough'),
                alt.Tooltip('descriptor:N', title='Type'),
                alt.Tooltip('complaints:Q', title='Complaints', format=',')]
    ).facet(
        facet=alt.Facet('borough:N', title=None),
        columns=3
    ).properties(
        title=alt.Title(
            '',
            subtitle='')
    ).resolve_scale(x='independent')
    return chart3

    #'Rodent Complaint Types by Borough (2020–2025)',
    #        subtitle='Source: NYC Open Data, 311 Service Requests')