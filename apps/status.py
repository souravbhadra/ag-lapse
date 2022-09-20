import streamlit as st
import folium
import pandas as pd
import numpy as np
from streamlit_folium import folium_static

#st.set_page_config(page_title="AgLapse", layout="wide")

def app():
    
    # initialize the map and store it in a m object
    m = folium.Map(location=[42, -97], zoom_start=4)

    ag_data = pd.read_csv('data/ag-data.csv',
                          index_col=0,
                          parse_dates=['Year'])

    with st.sidebar:
        st.title("Agricultural Status")
        # Crop type
        crops_choice = ['CORN', 'SOYBEANS', 'BARLEY', 'OATS']
        crop_sel = st.selectbox("Select crop", crops_choice)
        # Trait type
        traits_choice = ['Yield', 'Harvested', 'Planted']
        trait_sel = st.selectbox("Select trait", traits_choice)
        # Time scale
        time = st.slider("Select time",
                         min_value=2002,
                         max_value=2020,
                         step=1)

    ag_data = ag_data[ag_data['Year']==pd.to_datetime(str(time))]
    ag_data = ag_data[ag_data['Commodity'] == crop_sel]

    custom_scale = (ag_data[trait_sel].quantile(np.linspace(0, 1, 10))).tolist()
    
    # Figure out the trait unit
    if trait_sel == 'Yield':
        trait_unit = 'Bu/Acre'
    else:
        trait_unit = 'Acre'

    folium.Choropleth(
        geo_data='data/counties.geojson',
        data=ag_data,
        columns=['Id', trait_sel], 
        key_on='feature.properties.Id',
        bins=custom_scale,
        fill_color='YlOrRd',
        nan_fill_color="White",
        nan_fill_opacity=0.0,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'{trait_sel} ({trait_unit})',
        highlight=True,
        line_color='black'
    ).add_to(m)

    folium_static(m, width=800, height=475)
