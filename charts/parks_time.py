## LOADING PACKAGES
import geopandas as gpd
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mapclassify as mc
import folium as fol
import folium.plugins
import branca as br
#import geodatasets as gd
import os
import altair as alt
from vega_datasets import data
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from prettytable import PrettyTable
import shapely
from shapely import LineString, Point, Polygon
import pydeck as pdk
from charts.data_loader import load_parks, load_boroughs


def parks_time_chart():

    parks = load_parks()
    boroughs = load_boroughs()

    # 1. Convert acquisitiondate to datetime objects
    # Note: NYC Open Data often has inconsistent string formats; using coerce to handle NaT
    parks['acquisitiondate'] = pd.to_datetime(parks['acquisitiondate'], errors='coerce')

    # 2. Extract Year for the Time-Slider logic
    # Note: We will use this integer column to drive the Streamlit slider interaction
    parks['acq_year'] = parks['acquisitiondate'].dt.year

    # 3. Handle Missing Data (The "NaT" problem)
    # Note: Identifying how much of our historical narrative is "silent"
    missing_dates_count = parks['acquisitiondate'].isna().sum()


    # 4. Filter for relevant classes
    green_parks = parks[parks['class'] == 'PARK'].copy()

    # 1. Cast 'acres' to float to fix the TypeError
    # Note: Errors are coerced to NaN to prevent program termination on corrupted strings
    parks['acres'] = pd.to_numeric(parks['acres'], errors='coerce')

    # 2. Unify 'mapped' values to avoid case-sensitivity issues
    # Note: Ensuring 'true' and 'True' are treated as the same category
    parks['mapped'] = parks['mapped'].astype(str).str.capitalize()

    # 3. Grouping to identify spatial inequality
    # Note: Aggregating mean acreage to test if 'Mapped' status correlates with size
    mapping_summary = parks.groupby('mapped')['acres'].agg(['mean', 'count', 'sum']).sort_values(by='mean', ascending=False)

    # 4. Cleanup 'acq_year' for cleaner visualization
    # Note: Converting float years (e.g., 2002.0) to nullable integers for the Time-Slider
    parks['acq_year'] = parks['acq_year'].astype('Int64')

    # ==========================================
    # 1. Constants & Aesthetic Setup
    # ==========================================
    COLOR_MAP = {
        'Romantic/Social Lungs (<1873)':      {'fill': '#354F52', 'stroke': '#2F3E46'},
        'Consolidation Era (1874-1933)':      {'fill': '#2C6E49', 'stroke': '#1B4332'},
        'Robert Moses Boom (1934-1960)':      {'fill': '#52796F', 'stroke': '#354F52'},
        'Crisis & Conservancies (1961-1990)': {'fill': '#84A98C', 'stroke': '#52796F'},
        'Post-Industrial/Modern (1991-Now)':  {'fill': '#CAD2C5', 'stroke': '#84A98C'}
    }

    BINS = [0, 1873, 1933, 1960, 1990, 2026]
    LABELS = list(COLOR_MAP.keys())

    # ==========================================
    # 2. Data Preparation
    # ==========================================
    parks_viz = parks.to_crs(epsg=4326)
    boroughs_viz = boroughs.to_crs(epsg=4326)

    parks_clean = parks_viz[['signname', 'acq_year', 'acres', 'geometry']].copy()
    parks_clean['acq_year'] = pd.to_numeric(parks_clean['acq_year'], errors='coerce').fillna(0).astype(int)
    parks_clean['acres_int'] = pd.to_numeric(parks_clean['acres'], errors='coerce').fillna(0).round().astype(int)
    parks_clean['era'] = pd.cut(parks_clean['acq_year'], bins=BINS, labels=LABELS)

    # ==========================================
    # 3. Map Initialization
    # ==========================================
    m = folium.Map(
        location=[40.7306, -73.9352],
        zoom_start=15,
        tiles='CartoDB positron'
    )

    folium.GeoJson(
        boroughs_viz[['geometry']],
        style_function=lambda x: {
            'fillColor': '#D3D3D3',
            'color': '#8D99AE',
            'weight': 1.0,
            'fillOpacity': 0
        },
        control=False,
        interactive=False
    ).add_to(m)

    # ==========================================
    # 4. Era-based FeatureGroups
    # ==========================================
    fg_dict = {}
    for era in LABELS:
        fill_color = COLOR_MAP[era]['fill']
        legend_name = f'''
            <i style="background:{fill_color}; width:12px; height:12px;
            float:left; margin-right:8px; margin-top:2px; border-radius:2px;"></i>{era}
        '''
        fg_dict[era] = folium.FeatureGroup(name=legend_name).add_to(m)

    for era in LABELS:
        era_data = parks_clean[parks_clean['era'] == era]
        if era_data.empty:
            continue

        style_colors = COLOR_MAP[era]

        folium.GeoJson(
            era_data,
            style_function=lambda x, colors=style_colors: {
                'fillColor': colors['fill'],
                'color': colors['stroke'],
                'weight': 1.5,
                'fillOpacity': 0.65
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['signname', 'acq_year', 'acres_int'],
                aliases=['Park:', 'Year:', 'Acres:'],
                localize=True
            )
        ).add_to(fg_dict[era])

    # ==========================================
    # 5. UI Customization (NYT Style - Updated)
    # ==========================================
    # Note: CSS updated to remove the title header
    nyt_css = """
    <style>
        .leaflet-control-layers {
            border: 2px solid #555 !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
            font-family: 'Helvetica', sans-serif !important;
            font-size: 12px !important;
            padding: 12px !important;
            box-shadow: none !important;
        }
    </style>
    """
    m.get_root().header.add_child(folium.Element(nyt_css))

    # Position changed to topright as requested
    folium.LayerControl(collapsed=False, position='topright').add_to(m)

    return m