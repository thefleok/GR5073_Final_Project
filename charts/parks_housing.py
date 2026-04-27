# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mapclassify as mc
import folium as fol
import folium.plugins
import branca as br
import os
import altair as alt
from vega_datasets import data
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from prettytable import PrettyTable
import shapely
from shapely import LineString, Point, Polygon
import numpy as np
from charts.data_loader import load_parks, load_monuments, load_trees

def parks_housing_chart():
    parks = load_parks()
    monuments = load_monuments()
    trees = load_trees()


    ## CLEANING PARKS DATA ##

    basic_parks = parks[parks['typecategory'].isin(['Community Park', 'Flagship Park', 'Neighborhood Park'])] # filter for the most
    # typical "park" parks
    parks_geo = basic_parks.loc[:,'geometry'] # select geometry column for plotting

    ## INDIVIDUAL PARKS ##
    comms = parks[parks['typecategory'] == 'Community Park']
    comms_geo = comms.loc[:,'geometry'] # select geometry column for plotting

    flag = parks[parks['typecategory'] == 'Flagship Park']
    flag_geo = flag.loc[:,'geometry'] # select geometry column for plotting

    neighborhood = parks[parks['typecategory'] == 'Neighborhood Park']
    neighborhood_geo = neighborhood.loc[:,'geometry'] # select geometry column for plotting

    gardens = parks[parks['typecategory'] == 'Garden']
    gardens_geo = gardens.loc[:,'geometry'] # select geometry column for plotting

    nature_areas = parks[parks['typecategory'] == 'Nature Area']
    nature_areas_geo = nature_areas.loc[:,'geometry'] # select geometry column for plotting

    rec = parks[parks['typecategory'] == 'Recreational Field/Courts']
    rec_geo = rec.loc[:,'geometry'] # select geometry column for plotting

    triplaza = parks[parks['typecategory'] == 'Triangle/Plaza']
    triplaza_geo = triplaza.loc[:,'geometry'] # select geometry column for plotting

    waterfront = parks[parks['typecategory'] == 'Waterfront Facility']
    waterfront_geo = waterfront.loc[:,'geometry'] # select geometry column for plotting

    ## CLEANING MONUMENTS ##
    monuments = monuments.drop_duplicates(subset = 'name') # drop duplicate monuments

    monuments = monuments.dropna(subset=['X', 'Y']) # drop NAs in location

    monuments['geom'] = gpd.points_from_xy(monuments['X'], monuments['Y'],crs = '2263') # make X and Y into coordinates

    monuments = monuments.reset_index() # reset index for merge

    monuments = monuments.rename(columns = {'index': 'id_var'}) # rename index to "id variable"

    monuments_geo = gpd.GeoDataFrame(geometry=gpd.GeoSeries(monuments['geom'])) # set geometry

    monuments_geo = monuments_geo.reset_index() # reset geometry index for merge

    monuments_geo = monuments_geo.rename(columns = {'index': 'id_var'}) # rename index to "id variable"

    monuments_geo = monuments_geo.to_crs('EPSG:4326') # project geometry to 4326 for plotting

    ## REMERGE MONUMENTS ##

    monuments_full = monuments_geo.merge(monuments, left_on = 'id_var', right_on = 'id_var', how = 'inner')

    # set latitude and longitude
    monuments_full['latitude'] = [row.y for row in monuments_full['geometry']]
    monuments_full['longitude'] = [row.x for row in monuments_full['geometry']]

    ## CLEANING TREES ##

    trees = trees[trees['status'] == 'Alive'] # live trees
    #trees = trees[trees['health'] == 'Good'] # healthiest trees since there are so many
    trees['spc_common'] = trees['spc_common'].fillna(' ').astype(str) # set to type string for cleaning
    trees['spc_common'] = [row.replace("'", "") for row in trees['spc_common']] # remove commas for plotting
    trees['instance'] = 1 # set instance to sum counts

    grouped = trees.groupby('spc_common', as_index=False)['instance'].sum() # group by species and sum count
    sorted = grouped.sort_values('instance', ascending=True) # find rarest trees
    sorted[1:6] # top 5 rarest trees

    rare_trees = ['Virginia pine', 'black pine', 'Scots pine', 'Osage-orange', 'European alder'] # rare tree names

    rare_treesdf = trees[trees['spc_common'].isin(rare_trees)] # filter for rare trees

    trees['spc_common'].unique()

    cherry_treesdf = trees[trees['spc_common'].isin(['cherry', 'black cherry', 'Cornelian cherry', 'Schubert chokecherry'])]

    comms = comms.loc[:, ['signname', 'acres', 'geometry']]
    flag = flag.loc[:, ['signname', 'acres', 'geometry']]
    neighborhood = neighborhood.loc[:, ['signname', 'acres', 'geometry']]

    ### PLOT ###

    m = folium.Map(
        location=[40.78, -73.94],
        zoom_start=13, # zoomed out
        tiles='CartoDB positron' # I like positron for these maps
    )


    # community parks
    comm_park_layer = folium.FeatureGroup(name="Community Parks", show=False).add_to(m)

    folium.GeoJson(
        comms,
        style_function = lambda feature:{'fillColor' : '#49725d','color' : '#49725d','weight' : 1,'fillOpacity' : 0.25,
                                        'opacity' :0.5},tooltip=folium.GeoJsonTooltip(fields=['signname', 'acres'],
                                                                                    aliases=['Park:', 'Acres:']),
        popup=folium.GeoJsonPopup(fields=['signname'])).add_to(comm_park_layer)


    ## flagship parks
    flagship_park_layer = folium.FeatureGroup(name="Flagship Parks", show=True).add_to(m)

    folium.GeoJson(
        flag,style_function = lambda feature:{'fillColor' : '#2C6E49','color' : '#2C6E49','weight' : 1,'fillOpacity' : 0.25,
                                                'opacity' :0.5},tooltip=folium.GeoJsonTooltip(fields=['signname', 'acres'],
                                                                                                aliases=['Park:', 'Acres:']),
        popup=folium.GeoJsonPopup(fields=['signname'])).add_to(flagship_park_layer)

    ## neighborhood park layer
    neighborhood_layer = folium.FeatureGroup(name="Neighborhood Parks", show=True).add_to(m)

    folium.GeoJson(neighborhood,
                fill_color = '#2d7452', color = '#2d7452', opacity = .5).add_to(neighborhood_layer)

    ## nature areas
    nature_layer = folium.FeatureGroup(name="Nature Areas", show=True).add_to(m)

    folium.GeoJson(nature_areas_geo,
                fill_color = '#26ae00', color = '#26ae00', opacity = .5).add_to(nature_layer)

    ## gardens
    garden_layer = folium.FeatureGroup(name="Gardens", show=True).add_to(m)

    folium.GeoJson(gardens_geo,
                fill_color = '#7dce66', color = '#7dce66', opacity = .5).add_to(garden_layer)

    ## rec layer
    rec_layer = folium.FeatureGroup(name="Recreation Centers", show=True).add_to(m)

    folium.GeoJson(rec_geo,
                fill_color = '#44ff32', color = '#44ff32', opacity = .5).add_to(rec_layer)

    ## triplaza
    triplaza_layer = folium.FeatureGroup(name="Triangles/Plazas", show=True).add_to(m)

    folium.GeoJson(triplaza_geo,
                fill_color = '#13ab65', color = '#13ab65', opacity = .5).add_to(triplaza_layer)

    ## waterfront
    water_layer = folium.FeatureGroup(name="Waterfront Areas", show=True).add_to(m)

    folium.GeoJson(waterfront_geo,
                fill_color = '#527588', color = '#527588', opacity = .5).add_to(water_layer)


    # add layer for trees
    rare_trees_layer = folium.FeatureGroup(name="Rare Trees", show=False).add_to(m)

    rare_trees_features = pd.DataFrame({
        'species' : rare_treesdf['spc_common'],
        'lat' : rare_treesdf['latitude'],
        'long' : rare_treesdf['longitude']
    })

    for idx, row in rare_trees_features.iterrows():
        popup_content = f"""
        <h4>{row['species']}</h4>
        """

        folium.Marker(
            location = [row['lat'], row['long']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip = f"{row['species']}",
            icon=folium.Icon(
            icon = 'tree',
            prefix = 'fa',
            color = 'green')).add_to(rare_trees_layer)

    folium.LayerControl(collapsed=False).add_to(m)

    return m


