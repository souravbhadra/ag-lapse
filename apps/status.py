import streamlit as st
import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from streamlit_folium import folium_static

#st.set_page_config(page_title="AgLapse", layout="wide")

def app(crop_sel, trait_sel, time):
    
    # initialize the map and store it in a m object
    m = folium.Map(location=[38, -97], zoom_start=4)

    ag_data = pd.read_csv('data/ag-data.csv',
                          index_col=0,
                          parse_dates=['Year'])

    ag_data = ag_data[ag_data['Year']==pd.to_datetime(str(time))]
    ag_data = ag_data[ag_data['Commodity'] == crop_sel]

    custom_scale = (ag_data[trait_sel].quantile(np.linspace(0, 1, 10))).tolist()
    
    # Figure out the trait unit
    if trait_sel == 'Yield':
        trait_unit = 'Bu/Acre'
    else:
        trait_unit = 'Acre'
        
    states = gpd.read_file('data/states.geojson')
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#808080', 
                                'fillOpacity': 0.1, 
                                'weight': 1}
    stt = folium.GeoJson(states['geometry'], 
                         style_function=style_function).add_to(m)

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
    
    #gdf = gpd.read_file('data/counties.geojson')
    
    """for i in range(gdf.shape[0]):
        b = folium.GeoJson(gdf.iloc[i, -1])
        county = gdf.loc[i, 'County']
        state = gdf.loc[i, 'State']
        popup_text = f'{county}, {state}'
        b.add_child(folium.Popup(popup_text))
        m.add_child(b)"""

    folium_static(m, width=1250, height=550) 
