import altair as alt
import pandas as pd
alt.data_transformers.disable_max_rows()
from rat_charts.data_loader import load_zip_df


def scatter7_chart():

    zip_df = load_zip_df()


    #Colours
    BOROUGH_COLORS = {
        'Brooklyn': '#2F3E46',
        'Manhattan': '#52796F',
        'Queens': '#84A98C',
        'Bronx': '#527588',
        'Staten Island': '#CAD2C5'
    }

    zip_df = zip_df[zip_df["ZCTA5CE20"] != "11430"]

    #Scatterplot
    zip_scatter = zip_df.dropna(
        subset=["rats_per_1000", "poverty_rate", "white_prop", "black_prop", "borough"]
    ).copy()

    # Long format for dropdown
    zip_long = zip_scatter.melt(
        id_vars=["ZCTA5CE20", "borough", "rats_per_1000"],
        value_vars=["poverty_rate", "white_prop", "black_prop"],
        var_name="factor",
        value_name="value"
    )

    zip_long["factor"] = zip_long["factor"].map({
        "poverty_rate": "Poverty Rate",
        "white_prop": "White Population Share",
        "black_prop": "Black Population Share"
    })

    # Dropdown
    factor_dropdown = alt.binding_select(
        options=[
            "Poverty Rate",
            "White Population Share",
            "Black Population Share"
        ],
        name="Compare against: "
    )

    factor_select = alt.selection_point(
        fields=["factor"],
        bind=factor_dropdown,
        value="Poverty Rate"
    )

    # Borough highlight
    borough_select = alt.selection_point(
        fields=["borough"],
        bind="legend"
    )

    scatter = alt.Chart(zip_long).mark_circle(size=70).encode(
        x=alt.X("value:Q", title="Selected Factor"),
        y=alt.Y("rats_per_1000:Q", title="Rat Complaints per 1,000 Residents"),
        color=alt.Color("borough:N", title="Borough", scale=alt.Scale(domain=list(BOROUGH_COLORS.keys()), range=list(BOROUGH_COLORS.values()))),
        opacity=alt.condition(borough_select, alt.value(0.75), alt.value(0.12)),
        tooltip=[
            alt.Tooltip("ZCTA5CE20:N", title="Zip Code"),
            alt.Tooltip("borough:N", title="Borough"),
            alt.Tooltip("rats_per_1000:Q", title="Rat Complaints per 1,000", format=",d"),
            alt.Tooltip("factor:N", title="Factor"),
            alt.Tooltip("value:Q", title="Value", format=".2f")
        ]
    ).transform_filter(
        factor_select
    ).add_params(
        factor_select,
        borough_select
    ).properties(
        width=600,
        height=400,
        title="Rat Complaints per 1,000 vs Zip-Code Characteristics"
    )

    return scatter