import streamlit as st
import geopandas as gpd
import pandas as pd
import pygris

@st.cache_data
def load_line1():
    base_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"

    # Pulling rodent complaints in batches (API returns max 50K per call)
    limit = 50000
    offset = 0
    frames = []

    rats_311 = pd.read_csv("rat_csv/rats_slim.csv")
    rats_311['created_date'] = pd.to_datetime(rats_311['created_date'])
    rats_311['year_month'] = rats_311['created_date'].dt.to_period('M')

    # Monthly trend
    rats_2025 = rats_311[rats_311['created_date'] < '2026-01-01']
    monthly = rats_2025.set_index('created_date').resample('ME').size()
    zip_borough = (rats_2025
        .groupby(['incident_zip', 'borough']).size()
        .reset_index(name='rat_complaints'))
    zip_borough['incident_zip'] = zip_borough['incident_zip'].astype(int).astype(str)
    zip_borough = zip_borough.query("borough != 'Unspecified'")
    return zip_borough