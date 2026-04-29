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
from rat_charts.data_loader import load_rats_2025, load_rest_by_zip, load_permits_by_zip



def behavior_chart():
    # Chart 1: Interactive Monthly Trend with Borough Filter
    rats_2025 = load_rats_2025()
    # Borough colors
    BOROUGH_COLORS = {
        "BROOKLYN": "#52796F",
        "MANHATTAN": "#84A98C",
        "QUEENS": "#CAD2C5",
        "BRONX": "#354F52",
        "STATEN ISLAND": "#A8BCCC"
    }

    PALETTE = {
            'teal': '#52796F',
            'dark': '#2F3E46',
            'light': '#CAD2C5'
        }

    # Policy annotations data
    policy_data = pd.DataFrame([
        {'date': '2023-04-01', 'label': 'Rat Czar appointed'},
        {'date': '2023-07-01', 'label': 'Food biz containerization'},
        {'date': '2024-03-01', 'label': 'All biz containerization'},
        {'date': '2024-11-01', 'label': 'Residential containerization'}
    ])
    policy_data['date'] = pd.to_datetime(policy_data['date'])

    # Prepare monthly data by borough
    monthly_borough = (rats_2025
        .query("borough != 'Unspecified'")
        .groupby([rats_2025['created_date'].dt.to_period('M'), 'borough'])
        .size()
        .reset_index(name='complaints'))
    monthly_borough['date'] = monthly_borough['created_date'].dt.to_timestamp()
    monthly_borough = monthly_borough.drop(columns='created_date')

    # Add "All NYC" combined total
    monthly_all = monthly_borough.groupby('date')['complaints'].sum().reset_index()
    monthly_all['borough'] = 'All NYC'
    monthly_combined = pd.concat([monthly_borough, monthly_all], ignore_index=True)

    # Borough dropdown
    borough_dropdown = alt.binding_select(
        options=[None, 'All NYC', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'BRONX', 'STATEN ISLAND'],
        labels=['All Boroughs (overlaid)', 'All NYC (combined)', 'Brooklyn',
                'Manhattan', 'Queens', 'Bronx', 'Staten Island'],
        name='Borough: '
    )
    borough_select = alt.selection_point(fields=['borough'], bind=borough_dropdown)

    # Nearest point for crosshair
    nearest = alt.selection_point(nearest=True, on='pointerover', fields=['date'], empty=False)

    # Line
    line = alt.Chart(monthly_combined).mark_line(strokeWidth=2).encode(
        x=alt.X('date:T', title=None, axis=alt.Axis(format='%b %Y', labelAngle=-45)),
        y=alt.Y('complaints:Q', title='Number of Complaints'),
        color=alt.Color('borough:N', title='Borough', scale=alt.Scale(scheme='tableau10')),
        opacity=alt.condition(borough_select, alt.value(1), alt.value(0.1))
    ).add_params(borough_select)

    # Invisible hover points
    hover_points = alt.Chart(monthly_combined).mark_point(opacity=0, size=50).encode(
        x='date:T', y='complaints:Q'
    ).add_params(nearest)

    # Highlighted point on hover
    highlight = alt.Chart(monthly_combined).mark_point(size=80, filled=True).encode(
        x='date:T', y='complaints:Q',
        color=alt.Color('borough:N', title='Borough',
                    scale=alt.Scale(
                        domain=list(BOROUGH_COLORS.keys()),
                        range=list(BOROUGH_COLORS.values())
                    ))
    )

    # Vertical crosshair rule
    crosshair = alt.Chart(monthly_combined).mark_rule(
        color='gray', strokeDash=[2, 2]
    ).encode(x='date:T').transform_filter(nearest)

    # Policy annotations
    policy_rules = alt.Chart(policy_data).mark_rule(
        strokeDash=[4, 4], color=PALETTE['teal'], strokeWidth=1.5
    ).encode(x='date:T')

    policy_labels = alt.Chart(policy_data).mark_text(
        align='left', dx=5, fontSize=9, color=PALETTE['teal'], angle=270
    ).encode(x='date:T', y=alt.value(10), text='label:N')

    chart1 = (line + hover_points + highlight + crosshair + policy_rules + policy_labels).properties(
        width=700, height=400,
        title=alt.Title(
            '',
            subtitle=''
        )
    )

    return chart1