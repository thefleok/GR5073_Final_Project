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
from rat_charts.data_loader import load_rats_2025, load_rest_by_zip, load_permits_by_zip

def scatter5_chart():
    rats_2025 = load_rats_2025()
    rest_by_zip = load_rest_by_zip()
    permits_by_zip = load_permits_by_zip()

    BOROUGH_COLORS = {
            'BROOKLYN': '#2F3E46',
            'MANHATTAN': '#52796F',
            'QUEENS': '#84A98C',
            'BRONX': '#527588',
            'STATEN ISLAND': '#CAD2C5',
            'All NYC': '#354F52'
        }
    #  Section 2: Interactive Scatterplot

    # Prepare combined zip-level data with borough
    zip_borough = (rats_2025
        .groupby(['incident_zip', 'borough']).size()
        .reset_index(name='rat_complaints'))
    zip_borough['incident_zip'] = zip_borough['incident_zip'].astype(int).astype(str)
    zip_borough = zip_borough.query("borough != 'Unspecified'")

    # Merge in restaurant and permit counts
    zip_scatter = (zip_borough
        .merge(rest_by_zip, left_on='incident_zip', right_on='ZIPCODE', how='left')
        .merge(permits_by_zip, left_on='incident_zip', right_on='zip_code', how='left'))
    zip_scatter['rodent_violations'] = zip_scatter['rodent_violations'].fillna(0)
    zip_scatter['construction_permits'] = zip_scatter['construction_permits'].fillna(0)

    # Melt to long format for the dropdown
    zip_long = zip_scatter.melt(
        id_vars=['incident_zip', 'borough', 'rat_complaints'],
        value_vars=['rodent_violations', 'construction_permits'],
        var_name='factor', value_name='count'
    )
    zip_long['factor'] = zip_long['factor'].map({
        'rodent_violations': 'Restaurant Rodent Violations',
        'construction_permits': 'Construction Permits (Ground-Disrupting)'
    })

    # Factor dropdown
    factor_dropdown = alt.binding_select(
        options=['Restaurant Rodent Violations', 'Construction Permits (Ground-Disrupting)'],
        name='Compare against: '
    )
    factor_select = alt.selection_point(fields=['factor'], bind=factor_dropdown,
                                        value='Restaurant Rodent Violations')

    # Borough highlight via legend
    borough_select = alt.selection_point(fields=['borough'], bind='legend')

    scatter = alt.Chart(zip_long).mark_circle(size=60).encode(
        x=alt.X('count:Q', title='Factor Count'),
        y=alt.Y('rat_complaints:Q', title='311 Rat Complaints'),
        color=alt.Color('borough:N', title='Borough',
                    scale=alt.Scale(
                        domain=list(BOROUGH_COLORS.keys()),
                        range=list(BOROUGH_COLORS.values())
                    )),
        opacity=alt.condition(borough_select, alt.value(0.7), alt.value(0.1)),
        tooltip=[alt.Tooltip('incident_zip:N', title='Zip Code'),
                alt.Tooltip('borough:N', title='Borough'),
                alt.Tooltip('rat_complaints:Q', title='Rat Complaints', format=','),
                alt.Tooltip('count:Q', title='Factor Count', format=',')]
    ).transform_filter(
        factor_select
    ).add_params(
        factor_select,
        borough_select
    ).properties(
        width=600, height=400,
        title=alt.Title(
            '',
            subtitle=''
        )
    )

    #'Rat Complaints vs Contributing Factors by Zip Code',
    #        subtitle='Select a factor from dropdown | Click legend to highlight borough | Source: NYC Open Data'

    return scatter