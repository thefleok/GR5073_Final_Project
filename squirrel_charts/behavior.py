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

def behavior_chart():
    squirrel_cleaned = load_df()
    behavior_categories = ["Eating", "Foraging", "Running", "Kuks", "Tail flags"]
    color_counts = squirrel_cleaned["Primary Fur Color"].value_counts()
    behavior_counts = squirrel_cleaned.groupby("Primary Fur Color")[behavior_categories].sum()

    behavior_proportions = (behavior_counts.div(color_counts, axis = 0) * 100).reset_index()
    squirrel_updated = behavior_proportions.melt(id_vars = "Primary Fur Color", var_name = "Behavior", value_name = "Percentage")

    color_scale = alt.Scale(
        domain = ["Gray", "Cinnamon", "Black"],
        range = ["#2F3E46", "#ad5e4e", "#2f1f1c"]
    )

    chart = alt.Chart(squirrel_updated).mark_bar().encode(
        x = alt.X("Primary Fur Color:N", title = None, axis = alt.Axis(labels = False, ticks = False)),
        y = alt.Y("Percentage:Q", title = "Proportion of Color Group Partaking in Activity", axis = alt.Axis(grid = False, labelExpr = "datum.value + '%'")),
        color = alt.Color("Primary Fur Color:N", scale = color_scale, legend = None),
        column = alt.Column("Behavior:N", header = alt.Header(title = None, labelOrient = "bottom")),
        tooltip = [alt.Tooltip("Primary Fur Color:N", title = "Squirrel Color"),
                alt.Tooltip("Behavior:N"),
                alt.Tooltip("Percentage:Q", title = "Percentage of squirrels of this color doing it", format = ".2f")]

    ).properties(
        width = 100,
        height = 400,
        title = "Squirrel Behaviors Normalized by Color Group"
    ).configure_view(stroke = None)

    return chart