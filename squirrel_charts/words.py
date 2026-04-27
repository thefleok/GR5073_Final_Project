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
from squirrel_charts.data_loader import load_stories
import random

def words_chart():
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('punkt')

    stories = load_stories()

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    def string_cleaner(text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        # use character matching to clean punctuation/numbers
        text = "".join(character for character in text if character.isalpha() or character.isspace())
        individual_words = text.split()
        cleaned = [lemmatizer.lemmatize(word) for word in individual_words if word not in stop_words]
        return " ".join(cleaned)

    squirrel_story = stories[["Note Squirrel & Park Stories"]].copy()
    squirrel_story["Cleaned Text"] = squirrel_story["Note Squirrel & Park Stories"].apply(string_cleaner)

    text_input = " ".join(squirrel_story["Cleaned Text"])
    project_colors = ["#2F3E46", "#52796F", "#84A98C", "#44A29A"]
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(project_colors)
    wordcloud = WordCloud(width = 950, height = 550, min_font_size = 8, background_color = "white").generate(text_input)
    wordcloud.recolor(color_func=custom_color_func)
    
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.tight_layout()

    return fig