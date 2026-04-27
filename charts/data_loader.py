import streamlit as st
import geopandas as gpd
import pandas as pd
import pygris

@st.cache_data
def load_parks():
    return gpd.read_file("csv_data/Parks_Properties_20260414.geojson")

@st.cache_data
def load_housing():
    return pd.read_csv("csv_data/Affordable_Housing_Production_by_Building_20260415.csv")

@st.cache_data
def load_boroughs():
    return gpd.read_file("csv_data/Borough_Boundaries_20260416.geojson")

@st.cache_data
def load_monuments():
    return pd.read_csv("csv_data/NYC_Parks_Monuments_20260416.csv")

@st.cache_data
def load_trees():
    return pd.read_csv("csv_data/trees_sample.csv")

@st.cache_data
def load_popraw():
    # ==========================================
    # 1. Data Retrieval
    # ==========================================
    from pygris.data import get_census

    # Target County FIPS for the 5 boroughs of NYC
    nyc_fips = ["005", "047", "061", "081", "085"]

    # Fetching Total Population data
    nyc_pop_raw = get_census(
        dataset = "acs/acs5",
        variables = "B01003_001E",
        year = 2022,
        params = {
            "for": "tract:*",
            "in": "state:36"
        },
        return_geoid = True
    )

    # ==========================================
    # 2. String Slicing Filter
    # ==========================================
    # Note: GEOID is structured as SSCCCTTTTTT (S=State, C=County, T=Tract)
    # We slice characters from index 2 to 5 to extract the County FIPS code.
    nyc_pop_data = nyc_pop_raw[nyc_pop_raw['GEOID'].str[2:5].isin(nyc_fips)].copy()

    # Note: Renaming for clarity and ensuring the population is numeric
    nyc_pop_data = nyc_pop_data.rename(columns={"B01003_001E": "total_pop"})
    nyc_pop_data['total_pop'] = pd.to_numeric(nyc_pop_data['total_pop'], errors='coerce').fillna(0)

    # ==========================================
    # 3. Geography Retrieval & Merging
    # ==========================================
    # Note: Fetching NYC Tract boundaries specifically for the 5 boroughs
    # This provides the 'geometry' column needed for mapping.
    nyc_geometry = pygris.tracts(state = "NY", county = ["Bronx", "Kings", "New York", "Queens", "Richmond"], year = 2022)

    # Note: Merging the population data with the geometry based on the common GEOID
    # This combined GeoDataFrame is the foundation for your Bivariate Map.
    nyc_final_gdf = nyc_geometry.merge(nyc_pop_data[['GEOID', 'total_pop']], on = "GEOID")

    # Note: Projecting to EPSG:2263 (NY Long Island) for accurate density calculations
    # This is mandatory for QMSS-level spatial analysis.
    nyc_final_gdf = nyc_final_gdf.to_crs(2263)

    # Calculate Population Density (People per Square Mile)
    # Note: 1 sq mile = 27,878,400 sq feet
    nyc_final_gdf['pop_density'] = (nyc_final_gdf['total_pop'] / (nyc_final_gdf.geometry.area / 27878400))

    return nyc_final_gdf