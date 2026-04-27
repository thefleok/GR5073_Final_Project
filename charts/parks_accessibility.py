## LOADING PACKAGES
import geopandas as gpd
import streamlit as st
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mapclassify as mc
import folium
import folium.plugins
import branca as br
#import geodatasets as gd
import os
import altair as alt
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from prettytable import PrettyTable
import shapely
from shapely import LineString, Point, Polygon
from pygris.data import get_census
from charts.data_loader import load_parks, load_boroughs, load_popraw, load_monuments, load_trees


def parks_accessibility_chart():
    boroughs = load_boroughs()
    boroughs_viz = boroughs.to_crs(epsg=4326)

    parks_clean = load_parks()
    parks_clean = parks_clean.to_crs(epsg=4326)

    nyc_final_gdf = load_popraw()

    # ==========================================
    # 1. Constants & Bivariate Color Setup
    # ==========================================
    # Note: Using a professional 3x3 bivariate matrix adapted to the project palette
    # X-Axis (Housing Density) | Y-Axis (Green Coverage %)
    # Class naming convention: 'XY' (1=Low, 3=High)
    BIVARIATE_PALETTE = {
        # Y-Low: Low Green Coverage
        '11': '#F6F5F2',  # Low Density / Low Green (Parchment Base)
        '21': '#CAD2C5',  # Med Density / Low Green 
        '31': '#CAD2C5',  # High Density / Low Green (Focus: Park Deserts)

        # Y-Med: Medium Green Coverage
        '12': '#B0B7B2',  # Low Density / Med Green
        '22': '#9FA8A3',  # Med Density / Med Green (Average)
        '32': '#9FA8A3',  # High Density / Med Green

        # Y-High: High Green Coverage
        '13': '#84A98C',  # Low Density / High Green (Suburban Feel)
        '23': '#52796F',  # Med Density / High Green
        '33': '#2C6E49'   # High Density / High Green (Focus: Integrated Greenery)
    }

    # Labels for the descriptive tooltips
    CLASS_LABELS = {
        '11': 'Isolated: Low Density, Minimal Green',
        '31': 'Steel Jungle: High Density, Minimal Green (Park Desert)',
        '13': 'Green Suburb: Low Density, High Greenery',
        '33': 'Integrated: High Density, High Greenery (Ideal Mix)',
        'Default': 'Balanced: Mid-range density and coverage'
    }

    # ==========================================
    # 2. Advanced Spatial Analysis
    # ==========================================
    # Assuming 'nyc_pop_geometry' (EPSG:4326) and 'parks_clean' (EPSG:4326) are already loaded.

    # Step A: Standardize to EPSG:2263 for Accurate Area Calculations
    parks_2263 = parks_clean.to_crs(epsg=2263)
    tracts_2263 = nyc_final_gdf.to_crs(epsg=2263)

    # Note: Calculating Land Area for each Tract (in Square Miles)
    tracts_2263['tract_area_sqmi'] = tracts_2263.geometry.area / 27878400

    # Step B: Spatial Join - Calculating Park Area per Tract
    # Creating intersection of parks and tracts to handle parks crossing boundaries
    parks_intersection = gpd.overlay(parks_2263, tracts_2263, how='intersection')
    parks_intersection['park_area_sqmi'] = parks_intersection.geometry.area / 27878400

    # Aggregating park areas back to the Tract Level
    park_area_by_tract = parks_intersection.groupby('GEOID')['park_area_sqmi'].sum().reset_index()

    # Step C: Merge Analysis results back to main geometry
    final_gdf = tracts_2263.merge(park_area_by_tract, on='GEOID', how='left')
    final_gdf['park_area_sqmi'] = final_gdf['park_area_sqmi'].fillna(0) # Handle tracts with no parks

    # Step D: Calculate Metrics & Classification (Quantiles)
    # Density 1: pop_density
    final_gdf['pop_density'] = pd.to_numeric(final_gdf['pop_density'], errors='coerce').fillna(0)

    # Density 2: Park Coverage %
    final_gdf['green_coverage_pct'] = (final_gdf['park_area_sqmi'] / final_gdf['tract_area_sqmi']) * 100

    # Use qcut to ensure equal-sized bins (Tertiles)
    # Note: Assigning 1=Low, 2=Medium, 3=High
    try:
        # X-Axis: Population Density
        final_gdf['x_label'] = pd.qcut(
            final_gdf['pop_density'].rank(method='first'), 
            3, 
            labels=[1, 2, 3]
        )
        
        # Y-Axis: Green Coverage %
        # This is usually where the duplicates (0.0 values) occur.
        final_gdf['y_label'] = pd.qcut(
            final_gdf['green_coverage_pct'].rank(method='first'), 
            3, 
            labels=[1, 2, 3]
        )
        
        # Create the bivariate index (e.g., '11', '12'...'33')
        final_gdf['bi_class'] = final_gdf['x_label'].astype(str) + final_gdf['y_label'].astype(str)
        
    except Exception as e:
        # Fallback logic to ensure the app doesn't crash
        st.error(f"Classification failed: {e}")
        final_gdf['bi_class'] = '22'

    # Step E: Project back to WGS84 for Mapping
    final_gdf_viz = final_gdf.to_crs(epsg=4326)

    # ==========================================
    # 3. Folium Rendering
    # ==========================================

    # Note: Before converting to JSON, rounding values to 1 or 2 decimal places 
    # to meet the "meaningful detail" requirement in the project checklist.
    final_gdf_viz['pop_density'] = final_gdf_viz['pop_density'].round(1)
    final_gdf_viz['green_coverage_pct'] = final_gdf_viz['green_coverage_pct'].round(2)

    # Initializing map
    m = folium.Map(location=[40.7306, -73.9352], zoom_start=11, tiles='CartoDB positron')

    # Convert GeoDataFrame to JSON
    tracts_json = json.loads(final_gdf_viz.to_json())

    # Layer 1: The Bivariate Choropleth
    folium.GeoJson(
        tracts_json,
        style_function=lambda feature: {
            'fillColor': BIVARIATE_PALETTE.get(feature['properties']['bi_class'], '#F6F5F2'),
            'color': '#8D99AE', 
            'weight': 0.5,
            'fillOpacity': 0.7
        },
        # Note: Replaced 'census_tract_name' with 'NAMELSAD' which exists in the pygris dataset.
        tooltip=folium.GeoJsonTooltip(
            fields=['NAMELSAD', 'pop_density', 'green_coverage_pct', 'bi_class'],
            aliases=['Census Tract:', 'Pop Density (sq mi):', 'Green Coverage %:', 'Archetype Code:'],
            localize=True,
            sticky=False
        )
    ).add_to(m)

    # Layer 2: Basemap Outline
    folium.GeoJson(
        boroughs_viz[['geometry']],
        style_function=lambda x: {
            'fillColor': 'none',
            'color': '#555',
            'weight': 1.2,
            'opacity': 0.6
        },
        interactive=False
    ).add_to(m)

    # Adding Descriptive Title (Checklist requirement)
    title_html = '''
        <div style="position: fixed; 
        top: 10px; left: 50px; width: 450px; height: 35px; 
        background-color: white; border: 2px solid grey; z-index: 9999; 
        font-size: 16px; font-family: sans-serif; font-weight: bold;
        text-align: center; padding-top: 5px; opacity: 0.9;">
        Socio-Spatial Justice: NYC Population Density vs. Green Access
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # ==========================================
    # 4. Custom Bivariate Legend (HTML/CSS)
    # ==========================================
    # Note: Creating a 3x3 matrix legend to explain the intersection of Density and Greenery.
    # This meets the "Legends are present and clear" requirement in the project checklist.

    legend_html = f'''
    <div style="
        position: fixed; 
        bottom: 50px; right: 50px; width: 180px; height: 200px; 
        background-color: white; border: 2px solid grey; z-index: 9999; 
        font-size: 11px; font-family: 'Helvetica', sans-serif;
        padding: 15px; opacity: 0.95; border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    ">
        <div style="text-align: center; font-weight: bold; margin-bottom: 12px; font-size: 12px;">
            Relationship Matrix
        </div>
        
        <div style="display: flex; align-items: center;">
            <div style="writing-mode: vertical-rl; transform: rotate(180deg); 
                        text-align: center; margin-right: 8px; font-weight: bold; color: #2C6E49;">
                Green Access &rarr;
            </div>
            
            <table style="border-collapse: collapse; border: none;">
                <tr>
                    <td style="background-color: {BIVARIATE_PALETTE['13']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['23']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['33']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                </tr>
                <tr>
                    <td style="background-color: {BIVARIATE_PALETTE['12']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['22']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['32']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                </tr>
                <tr>
                    <td style="background-color: {BIVARIATE_PALETTE['11']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['21']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE['31']}; width: 35px; height: 35px; border: 1px solid white;"></td>
                </tr>
            </table>
        </div>
        
        <div style="text-align: center; margin-left: 20px; margin-top: 8px; font-weight: bold; color: #354F52;">
            Pop Density &rarr;
        </div>

        <div style="margin-top: 12px; font-size: 9px; color: #555; line-height: 1.2;">
            <span style="color: #2C6E49;">&#9632;</span> <b>Top-Right:</b> Integrated (Ideal)<br>
            <span style="color: #CAD2C5;">&#9632;</span> <b>Bottom-Right:</b> Steel Jungle (Desert)
        </div>
    </div>
    '''

    # Note: Injecting the legend into the map root
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display map
    return m
