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
    # 1. 2x2 Bivariate Color Setup
    # ==========================================
    # Note: Simplified to 2x2 to increase intuitive contrast.
    # X-Axis (Pop Density) | Y-Axis (Green Coverage %)
    BIVARIATE_PALETTE_2X2 = {
        '11': '#F6F5F2',  # Low Pop / Low Green (Underutilized)
        '21': '#CAD2C5',  # High Pop / Low Green (The "Park Desert" - Critical Focus)
        '12': '#84A98C',  # Low Pop / High Green (Green Suburb/Residential)
        '22': '#2C6E49'   # High Pop / High Green (Integrated Excellence)
    }

    # ==========================================
    # 2. Data Cleaning & Land Clipping
    # ==========================================
    tracts_2263 = nyc_final_gdf.to_crs(epsg=2263)
    boroughs_2263 = boroughs.to_crs(epsg=2263)

    # Note: Clipping to fix the "Sea Fill" issue
    tracts_land_only = gpd.clip(tracts_2263, boroughs_2263)

    # Step B: Recalculate Metrics
    parks_2263 = parks_clean.to_crs(epsg=2263)
    parks_int = gpd.overlay(parks_2263, tracts_land_only, how='intersection')

    # Note: Summing area and renaming to avoid 'geometry' collision
    park_area_val = parks_int.groupby('GEOID')['geometry'].apply(lambda x: x.area.sum() / 27878400).reset_index()
    park_area_val = park_area_val.rename(columns={'geometry': 'park_area_sqmi'})

    # Step C: Merge & Fix Active Geometry
    final_gdf = tracts_land_only.merge(park_area_val, on='GEOID', how='left').fillna(0)

    # Note: Explicitly setting the geometry column after merge
    # This ensures GeoPandas knows which column to use for to_crs()
    final_gdf = final_gdf.set_geometry('geometry')

    # Step D: Recalculate Metrics on Land-Only Geometry
    final_gdf['tract_area_sqmi'] = final_gdf.geometry.area / 27878400
    final_gdf['green_coverage_pct'] = (final_gdf['park_area_sqmi'] / final_gdf['tract_area_sqmi']) * 100

    # Step E: 2x2 Binning (Median Split)
    final_gdf['pop_density'] = final_gdf['total_pop'] / final_gdf['tract_area_sqmi']
    for col in ['x_label', 'y_label', 'bi_class']:
    if col in final_gdf.columns:
        final_gdf.drop(columns=[col], inplace=True)
    final_gdf['x_label'] = pd.qcut(final_gdf['pop_density'].rank(method='first'), 2, labels=['1', '2'])
    final_gdf['y_label'] = pd.qcut(final_gdf['green_coverage_pct'].rank(method='first'), 2, labels=['1', '2'])
    final_gdf['bi_class'] = final_gdf['x_label'].astype(str) + final_gdf['y_label'].astype(str)

    # Now to_crs() will work perfectly
    final_gdf_viz = final_gdf.to_crs(epsg=4326)

    # ==========================================
    # 3. Folium Rendering
    # ==========================================
    m = folium.Map(location=[40.7306, -73.9352], zoom_start=11, tiles='CartoDB positron')

    # Layer 1: The Bivariate 2x2 Layer
    folium.GeoJson(
        json.loads(final_gdf_viz.to_json()),
        style_function=lambda feature: {
            'fillColor': BIVARIATE_PALETTE_2X2.get(feature['properties']['bi_class'], '#F6F5F2'),
            'color': '#8D99AE', 'weight': 0.4, 'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['NAMELSAD', 'pop_density', 'green_coverage_pct'],
            aliases=['Tract:', 'Population Density:', 'Green %:'],
            localize=True
        )
    ).add_to(m)

    # ==========================================
    # 4. Custom 2x2 Legend
    # ==========================================
    legend_html = f'''
    <div style="
        position: fixed;
        top: 20px; right: 20px; width: 150px; height: 160px;
        background-color: white; border: 2px solid #555; z-index: 9999;
        font-size: 10px; font-family: 'Helvetica', sans-serif;
        padding: 10px; opacity: 0.9; border-radius: 4px;
    ">
        <div style="text-align: center; font-weight: bold; margin-bottom: 8px;">Justice Matrix (2x2)</div>
        <div style="display: flex; align-items: center;">
            <div style="writing-mode: vertical-rl; transform: rotate(180deg); font-weight: bold; color: #2C6E49; margin-right: 5px;">
                Green &rarr;
            </div>
            <table style="border-collapse: collapse;">
                <tr>
                    <td style="background-color: {BIVARIATE_PALETTE_2X2['12']}; width: 40px; height: 40px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE_2X2['22']}; width: 40px; height: 40px; border: 1px solid white;"></td>
                </tr>
                <tr>
                    <td style="background-color: {BIVARIATE_PALETTE_2X2['11']}; width: 40px; height: 40px; border: 1px solid white;"></td>
                    <td style="background-color: {BIVARIATE_PALETTE_2X2['21']}; width: 40px; height: 40px; border: 1px solid white;"></td>
                </tr>
            </table>
        </div>
        <div style="text-align: center; margin-top: 5px; font-weight: bold; color: #354F52;">
            Density &rarr;
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display map
    return m