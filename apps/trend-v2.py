import streamlit as st
import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from scipy.stats import linregress
from streamlit_folium import folium_static
import io
import base64
import matplotlib.pyplot as plt
from folium import IFrame

#st.set_page_config(page_title="AgLapse", layout="wide")

# Helper function to calculate trend
def get_slope(series):
    series = series.sort_index()
    x = np.arange(1, series.shape[0]+1)
    return linregress(x, series.values)[0]

def get_trend_values(df, start, end, crop, trait):
    start = pd.to_datetime(str(start))
    end = pd.to_datetime(str(end))
    df = df[df['Commodity']==crop]
    df = df[(df['Year']>=start) & (df['Year']<=end)]
    df = df.set_index('Year')
    
    trait_vals = pd.pivot_table(
        df,
        values=trait,
        index=['Id'],
        aggfunc=get_slope
    )
    trait_vals = trait_vals.reset_index()
    
    return df, trait_vals

def get_plot_values(df, trait, idx):
    
    values = df[df['Id']==idx]
    values = values.sort_index()
    county = values['County'].values[0]
    state = values['State'].values[0]
    values = values[trait]
    
    return values, county, state
    


def app():
    
    # initialize the map and store it in a m object
    m = folium.Map(location=[42, -97], zoom_start=4)

    ag_data = pd.read_csv('data/ag-data.csv',
                          index_col=0,
                          parse_dates=['Year'])

    with st.sidebar:
        st.title("Agricultural Trends")
        # Crop type
        crops_choice = ['CORN', 'SOYBEANS', 'BARLEY', 'OATS']
        crop_sel = st.selectbox("Select crop", crops_choice)
        # Trait type
        traits_choice = ['Yield', 'Harvested', 'Planted']
        trait_sel = st.selectbox("Select trait", traits_choice)
        # Time scale
        time_options = np.arange(1910, 2022)
        start, end = st.select_slider("Select time range",
                                    options=time_options,
                                    value=(1930, 2021))
        # Button 
        button_help = "Draw individual trend plots."
        button = st.button('Draw Trend Plots', help=button_help)
        
        st.title("Contact")
        st.info(
            """
            [Sourav Bhadra](https://souravbhadra.github.io)
            [GitHub](https://github.com/souravbhadra) | [LinkedIn](https://www.linkedin.com/in/bhadrasourav/) | [Twitter](https://twitter.com/sbhadra19)
            """
        )

    df, trait_vals = get_trend_values(ag_data,
                                      start,
                                      end,
                                      crop_sel, 
                                      trait_sel)

    custom_scale = (trait_vals[trait_sel].quantile(np.linspace(0, 1, 10))).tolist()

    ch = folium.Choropleth(
        geo_data='data/counties.geojson',
        data=trait_vals,
        columns=['Id', trait_sel], 
        key_on='feature.properties.Id',
        bins=custom_scale,
        fill_color='YlOrRd',
        nan_fill_color="White",
        nan_fill_opacity=0.0,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Trend (Slope)',
        highlight=True,
        line_color='black'
    ).add_to(m)
    
    
    
    if button:
    
        gdf = gpd.read_file('data/counties.geojson')
        
        for idx in np.unique(df['Id']):
            try:
                png = f'data/figures/{crop_sel}-{trait_sel}-{idx}.png'
                encoded = base64.b64encode(open(png, 'rb').read())
                html = '<img src="data:image/png;base64,{}">'.format
                width, height = 4, 2
                resolution = 75
                iframe = IFrame(html(encoded.decode('UTF-8')),
                                width=(width*resolution)+20,
                                height=(height*resolution)+30)
                popup = folium.Popup(iframe, max_width=2650)
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                b = folium.GeoJson(gdf.iloc[gdf[gdf['Id']==idx].index[0], -1], 
                                style_function=style_function)
                b.add_child(popup)
                ch.add_child(b)
            except:
                pass

    folium_static(m, width=800, height=475)
