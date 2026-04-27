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
from rat_charts.data_loader import load_zip_gdf

def map_chart4():
    zip_gdf = load_zip_gdf()
    print(zip_gdf[['population', 'rat_per_1000', 'violations_per_1000', 'permits_per_1000']].describe())
    print(zip_gdf.columns.tolist())



    #  Normalized Folium Choropleth
    m = folium.Map(location=[40.7128, -73.95], zoom_start=11, tiles='CartoDB positron', attr="")
    zip_plot = zip_gdf.to_crs(epsg=4326)

    # Filter to zip codes with population
    zip_plot = zip_plot[zip_plot['population'] > 0]

    ## Layer 1: Rat Complaints per 1,000
    rat_colormap = cm.LinearColormap(
        ['#F6F5F2', '#CAD2C5', '#84A98C', '#52796F', '#2F3E46'],
        vmin=0, vmax=zip_plot['rat_per_1000'].quantile(0.95),
        caption='Rat Complaints per 1,000 Residents (2020–2025)')

    rat_layer = folium.FeatureGroup(name='Rat Complaints per 1,000')
    folium.GeoJson(
        zip_plot[zip_plot['rat_per_1000'] > 0],
        style_function=lambda f: {
            'fillColor': rat_colormap(min(f['properties']['rat_per_1000'],
                                        zip_plot['rat_per_1000'].quantile(0.95))),
            'color': '#354F52', 'weight': 0.5, 'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['zipcode', 'rat_per_1000', 'rat_complaints', 'population'],
            aliases=['Zip Code:', 'Per 1,000:', 'Total Complaints:', 'Population:']
        )
    ).add_to(rat_layer)
    rat_layer.add_to(m)
    rat_colormap.add_to(m)

    ## Layer 2: Restaurant Violations per 1,000
    rest_colormap = cm.LinearColormap(
        ['#F6F5F2', '#84A98C', '#2C6E49'],
        vmin=0, vmax=zip_plot['violations_per_1000'].quantile(0.95),
        caption='Restaurant Rodent Violations per 1,000 Residents')

    rest_layer = folium.FeatureGroup(name='Restaurant Violations per 1,000', show=False)
    folium.GeoJson(
        zip_plot[zip_plot['violations_per_1000'] > 0],
        style_function=lambda f: {
            'fillColor': rest_colormap(min(f['properties']['violations_per_1000'],
                                        zip_plot['violations_per_1000'].quantile(0.95))),
            'color': '#354F52', 'weight': 0.5, 'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['zipcode', 'violations_per_1000', 'rodent_violations', 'population'],
            aliases=['Zip Code:', 'Per 1,000:', 'Total Violations:', 'Population:']
        )
    ).add_to(rest_layer)
    rest_layer.add_to(m)

    ## Layer 3: Construction Permits per 1,000
    perm_colormap = cm.LinearColormap(
        ['#F6F5F2', '#A8BCCC', '#527588', '#354F52'],
        vmin=0, vmax=zip_plot['permits_per_1000'].quantile(0.95),
        caption='Construction Permits per 1,000 Residents')

    perm_layer = folium.FeatureGroup(name='Construction Permits per 1,000', show=False)
    folium.GeoJson(
        zip_plot[zip_plot['permits_per_1000'] > 0],
        style_function=lambda f: {
            'fillColor': perm_colormap(min(f['properties']['permits_per_1000'],
                                        zip_plot['permits_per_1000'].quantile(0.95))),
            'color': '#354F52', 'weight': 0.5, 'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['zipcode', 'permits_per_1000', 'construction_permits', 'population'],
            aliases=['Zip Code:', 'Per 1,000:', 'Total Permits:', 'Population:']
        )
    ).add_to(perm_layer)
    perm_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m