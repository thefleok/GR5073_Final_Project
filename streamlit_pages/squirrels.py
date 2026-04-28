import streamlit as st
from streamlit_folium import st_folium
from squirrel_charts.maps import maps_chart
from squirrel_charts.words import words_chart
from squirrel_charts.behavior import behavior_chart

def show():
    st.markdown("# Central Park Squirrel Census")
    st.markdown("In 2018, citizen practictioners spent two weeks in Central Park documenting observations of squirrels. " \
    "Capturing a number of squirrel-related variables and sentiment-driven descriptions of squirrel sightings, these citizens" \
    " counted the total squirrel sightings they observed and shared their findings on the NYC OpenData website. There are 3,023" \
    " total sightings in the dataset that include information about physical appearance, emitted behavior, and a narrative story" \
    " about what the squirrel actually did.")


    st.markdown("### Word Cloud: Squirrel Sighting Descriptions")
    chart1 = words_chart()
    st.pyplot(chart1)
    st.markdown("The above word cloud visualizes the most common words used by citizen practitioners when describing their interactions" \
    " with the squirrels observed in the dataset. Unsurprisingly, squirrel is the largest word in this word cloud after removing stopwords." \
    " It likely appears in close to all documented sightings to describe the animal in question. \n\n The more interesting findings occur " \
    "at second and third tier sizes of words. Adjective words paint a picture of the personality of the squirrel (quiet, busy, little) as" \
    " small, nimble, and impressive creatures. It is also interesting to view the nouns that correspond to common stories potentially available"
    " in the dataset. \"Dog\" and \"bird\" are frequently available, implying that the flexible, nimble nature of squirrels allows them to" \
    " often interact with their surroundings.")

    # introduction to first graph
    st.markdown("### Graph 2: Squirrel Map")
    chart2 = maps_chart()
    st_folium(chart2, width = 700, height = 500)
    st.markdown("Our second chart provides a graph of the entirety of central park and sightings of all available squirrels. It demonstrates " \
    "immediately that our sample is heavily weighted in favor of Cinammon and gray squirrels (over black squirrels). Given that this was a live " \
    "data collection task, it is possible that this was due to the visible clarity of lighter-colored squirrels over their darker counterparts. " \
    "As an alternative, it is also possible that different colors of squirrels are more and less common in the dataset. It is also valuable to " \
    "note that the distribution of squirrels appears to be universal throughout the park. There are no extreme \"squirrel parks\" per say.")

    st.markdown("### Bar plot: Value-adjusted percentage of squirrels emitting particular behaviors")
    chart3 = behavior_chart()
    st.altair_chart(chart3)
    st.markdown("The above chart is scaled by the quantity of squirrels of a particular color. Namely, the percentage displayed represents the " \
    "number of squirrels displaying a particular behavior divided by the number of squirrels with that particular color. This levels the playing " \
    "field between different groups of squirrels (allowing us to understand the percentage of squirrels of a particular color emitting a behavior)"
    ". Otherwise, the chart would be heavily skewed against black squirrels. \n\n The chart provides a valuable insight into the level of \"activity\" "
    "for each of the squirrel color groups. Across the board, cinnamon squirrels appear to be more active per capita than black or grey squirrels in " \
    "4 out of 5 categories. It is also interesting that across colors the rough visual average of activity load remains consistent throughout the dataset;" \
    " all three squirrels display 40-50 percent likelihood of foraging, while all three squirrels are very unlikely to emit Kuks. Across the 5 categories, " \
    "squirrels roughly operate in the same ballpark ranges, with a slight edge for the brown squirrels over their peers (with the exception of Kuks where" \
    " the relationship is relatively inconclusive between the three colors)")