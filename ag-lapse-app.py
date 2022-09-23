import streamlit as st
from streamlit_option_menu import option_menu
from apps import trend, status
import numpy as np

st.set_page_config(page_title="AgLapse", layout="wide")

apps = [
    {"func": status.app, "title": "Ag-Status", "icon": "clock"},
    {"func": trend.app, "title": "Ag-Trend", "icon": "graph-up-arrow"}
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

row1_1, row1_2, row1_3 = st.columns((1, 1, 1))

with row1_1:
    st.title("Ag-Lapse")
    st.write(
        """
        A spatiotemporal visualization tool for four major agricultural crops in the United States.
        """
    )
    
with row1_2:
    selected = option_menu(
        None,
        options=['Status', 'Trend'],
        icons=["clock", "graph-up-arrow"],
        menu_icon="cast",
        #default_index=default_index,
        orientation="horizontal"
    )
    
    # Time scale
    if selected == 'Status':
        time = st.slider("Select time",
                         min_value=1910,
                         max_value=2021,
                         value=2018,
                         step=1)
    else:
        time_options = np.arange(1910, 2022)
        start, end = st.select_slider("Select time range",
                                      options=time_options,
                                      value=(1930, 2021))
    
with row1_3:
    # Crop type
    crops_choice = ['CORN', 'SOYBEANS', 'BARLEY', 'OATS']
    crop_sel = st.selectbox("Select crop", crops_choice)

    # Crop type
    traits_choice = ['Yield', 'Planted', 'Harvested']
    trait_sel = st.selectbox("Select trait", traits_choice)


if selected == 'Status':
    status.app(crop_sel, trait_sel, time)
else:
    trend.app(crop_sel, trait_sel, start, end, True)
    
    
row2_1, row2_2 = st.columns((2, 1))

with row2_1:
    st.write(
        """
        #### Disclaimer
        The county and state shapefiles were downloaded from the U.S. Census 
        [TIGER database](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).
        The agricultural dataset was downloaded from the [USDA NASS database](https://quickstats.nass.usda.gov).
        The trend was calculated by simply taking a timeseries and calculating the corresponding slope. 
        All the analysis was performed using open-source packages in Python.   
        **Map Author:**  *Sourav Bhadra* [souravbhadra.github.io](https://souravbhadra.github.io) | [GitHub](https://github.com/souravbhadra) | [LinkedIn](https://www.linkedin.com/in/bhadrasourav/) | [Twitter](https://twitter.com/sbhadra19)
        """
    )
    
with row2_2:
    st.image('assets/images.png')