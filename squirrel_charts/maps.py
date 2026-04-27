import pandas as pd
import folium
from folium.plugins import MarkerCluster
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from squirrel_charts.data_loader import load_df

def maps_chart():
    squirrel_cleaned = load_df()
    squirrel_map = folium.Map(location = [40.78291, -73.96539], # central park start
               zoom_start = 14.2, # customized starting zoom to capture whole park
               min_zoom = 13.3, # avoid over zooming for users
               max_zoom = 18.5, # avoid extraneous exits for users
               tiles = "CartoDB Positron" # light mapping used to have less contrast
               )

    # for mapping primary colors to our data points in the below for loop
    fur_mapping = {"Gray": "gray",
                "Cinnamon": "brown",
                "Black": "black"}

    # we establish feature groups that will be used in our customizable legend
    gray_s = folium.FeatureGroup(name = "Gray Squirrels").add_to(squirrel_map)
    cinnamon_s = folium.FeatureGroup(name = "Cinnamon Squirrels").add_to(squirrel_map)
    black_s = folium.FeatureGroup(name = "Black Squirrels").add_to(squirrel_map)

    # we create clusters for every feature group
    gray_cluster = MarkerCluster(disableClusteringAtZoom=16).add_to(gray_s)
    cinnamon_cluster = MarkerCluster(disableClusteringAtZoom=16).add_to(cinnamon_s)
    black_cluster = MarkerCluster(disableClusteringAtZoom=16).add_to(black_s)

    for index, row in squirrel_cleaned.iterrows():
        # create popup text in HTML to share basic attributes about each pigeon
        popup_text = f"""
        <b>Age:</b> {row["Age"]} <br>
        <b>Color:</b> {row["Primary Fur Color"]} <br>
        <b>Activity:</b> {"Eating" if row["Eating"] else "Foraging" if row["Foraging"] else "Chilling"}
        """

        # map our primary colors using teh esatblished fur mapping above
        color = row["Primary Fur Color"]
        primary_color = fur_mapping.get(row["Primary Fur Color"])

        # building circle markers for each point based on provided coordinates
        marker = folium.CircleMarker(
            location=[row["Y"], row["X"]],
            radius=4,
            popup=folium.Popup(popup_text),
            color=primary_color,
            fill=True,
        )

        if color == "Gray":
            marker.add_to(gray_cluster)
        elif color == "Cinnamon":
            marker.add_to(cinnamon_cluster)
        else:
            marker.add_to(black_cluster)


    folium.LayerControl(collapsed=False).add_to(squirrel_map)

    return squirrel_map