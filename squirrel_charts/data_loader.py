import streamlit as st
import pandas as pd

@st.cache_data
def load_stories():
    return pd.read_csv("squirrel_csv/squirrel_stories.csv")

@st.cache_data
def load_df():
    df = pd.read_csv("squirrel_csv/2018_Central_Park_Squirrel_Census.csv")
    heavynan_columns = df.columns[df.isna().sum() > 200]
    df = df.drop(columns=heavynan_columns)
    return df.dropna()