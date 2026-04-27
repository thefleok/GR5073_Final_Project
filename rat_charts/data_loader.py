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

    rats_311 = pd.read_csv("rat_csv/rats_slim_final.csv")
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

@st.cache_data
def load_rest_by_zip():
    restaurants = pd.read_csv("rat_csv/restaurants_slim.csv")
    rodent_mask = restaurants['VIOLATION_DESCRIPTION'].str.contains(
        'rodent|Rodent|rat |mice|mouse', case=False, na=False)
    rodent_restaurants = restaurants[rodent_mask].copy()
    rest_by_zip = (rodent_restaurants.groupby('ZIPCODE').size()
                   .reset_index(name='rodent_violations'))
    rest_by_zip['ZIPCODE'] = rest_by_zip['ZIPCODE'].astype(int).astype(str)
    return rest_by_zip

@st.cache_data
def load_permits_by_zip():
    disruption_types = ['Foundation', 'Earth Work', 'Support of Excavation',
                        'Full Demolition', 'General Construction']
    permits = pd.read_csv("rat_csv/permits_slim.csv")
    permits_disruptive = permits[permits['work_type'].isin(disruption_types)].copy()
    permits_disruptive['issued_date'] = pd.to_datetime(permits_disruptive['issued_date'])

    # Cap at 2025
    permits_disruptive = permits_disruptive[permits_disruptive['issued_date'] < '2026-01-01']

    # Count per zip
    permits_by_zip = (permits_disruptive.groupby('zip_code').size()
                    .reset_index(name='construction_permits'))
    permits_by_zip['zip_code'] = permits_by_zip['zip_code'].astype(int).astype(str)
    return permits_by_zip