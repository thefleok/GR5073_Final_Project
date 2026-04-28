import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely import wkt
from rat_charts.data_loader import load_merged, load_mta, load_nycha, load_neighborhoods, load_boroughs, load_routes


def heat6_chart():

    merged = load_merged()
    MTA = load_mta()
    NYCHA = load_nycha()
    neigh_df = load_neighborhoods()
    borough = load_boroughs()
    routes_gdf = load_routes()



    # Ensure numeric
    merged["Latitude"] = pd.to_numeric(merged["Latitude"], errors="coerce")
    merged["Longitude"] = pd.to_numeric(merged["Longitude"], errors="coerce")

    # Filter to rat/mouse sightings
    rats = merged[
        merged["Problem Detail (formerly Descriptor)"]
        .str.contains("Rat|Mouse", case=False, na=False)
    ].dropna(subset=["Latitude", "Longitude"]).copy()

    # Map
    m = folium.Map(
        location=[40.7128, -74.0060],
        zoom_start=11,
        tiles="CartoDB positron"
    )


    # -----------------------
    # Layer 1: Rat/Mouse Heatmap
    # -----------------------
    heat_layer = folium.FeatureGroup(
        name="Rat/Mouse Complaint Heatmap",
        show=True
    )

    heat_data = rats[["Latitude", "Longitude"]].values.tolist()

    gradient = {
        0.0: "#00000000",

        0.15: "#2596be",
        0.3: "#5385b8",

        0.5: "#f7dda0",
        0.7: "#f0b579",
        0.85: "#e48d62",
        0.95: "#dc7757",

        1.0: "#c13442"
    }

    HeatMap(
        heat_data,
        radius=17,
        blur=10,
        min_opacity=0.1,
        max_zoom=18,
        gradient=gradient
    ).add_to(heat_layer)

    heat_layer.add_to(m)

    # -----------------------
    # Layer: Boroughs
    # -----------------------

  

    borough_layer = folium.FeatureGroup(
        name="Boroughs",
        show=True
    )

    folium.GeoJson(
        borough,
        style_function=lambda x: {
            "fillColor": "none",
            "color": "#52796F",
            "weight": 1,
            "opacity": 0.9
        },
    ).add_to(borough_layer)

    borough_layer.add_to(m)

    # -----------------------
    # Layer: Neighborhoods
    # -----------------------


    neighborhood_layer = folium.FeatureGroup(
        name="Neighborhoods",
        show=True
    )

    folium.GeoJson(
        neigh_df,
        style_function=lambda x: {
            "fillColor": "none",
            "color": "#52796F",
            "weight": 0.5,
            "opacity": 0.4
        }
    ).add_to(neighborhood_layer)

    neighborhood_layer.add_to(m)

    # -----------------------
    # Layer: MTA Stations
    # -----------------------
    mta_layer = folium.FeatureGroup(
        name="MTA Stations",
        show=False
    )

    # Ensure numeric
    MTA["GTFS Latitude"] = pd.to_numeric(MTA["GTFS Latitude"], errors="coerce")
    MTA["GTFS Longitude"] = pd.to_numeric(MTA["GTFS Longitude"], errors="coerce")

    mta_clean = MTA.dropna(subset=["GTFS Latitude", "GTFS Longitude"])

    for _, row in mta_clean.iterrows():
        folium.CircleMarker(
            location=[row["GTFS Latitude"], row["GTFS Longitude"]],
            radius=1.25,
            color="#1d3557",
            fill=True,
            fill_color="#1d3557",
            fill_opacity=0.3,
            opacity=0.3,
            tooltip=f"{row['Stop Name']} ({row['Line']})"
        ).add_to(mta_layer)

    mta_layer.add_to(m)

    # -----------------------
    # Layer: Subway Lines
    # -----------------------
    subway_layer = folium.FeatureGroup(
        name="Subway Lines",
        show=False
    )

    folium.GeoJson(
        routes_gdf,
        style_function=lambda f: {
            "color": "#52796F",   # muted default
            "weight": 2,
            "opacity": 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["route_shor", "route_long"],
            aliases=["Line:", "Route:"]
        )
    ).add_to(subway_layer)

    subway_layer.add_to(m)

    # -----------------------
    # Layer: NYCHA Buildings
    # -----------------------

    

    nycha_layer = folium.FeatureGroup(
        name="NYCHA Buildings",
        show=False
    )

    folium.GeoJson(
        NYCHA,
        style_function=lambda x: {
            "fillColor": "#2F3E46",
            "color": "#2F3E46",
            "weight": 0,
            "fillOpacity": 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["DEVELOPMEN"],
            aliases=["NYCHA Development:"]
        )
    ).add_to(nycha_layer)

    nycha_layer.add_to(m)
    # -----------------------
    # Layer Control
    # -----------------------
    folium.LayerControl(collapsed=False).add_to(m)

    return m