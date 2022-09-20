import streamlit as st
from streamlit_option_menu import option_menu
from apps import trend, status

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

st.title("AgLapse")

with st.sidebar:
    selected = option_menu(
        None,
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
        orientation="horizontal"
    )


for app in apps:
    if app["title"] == selected:
        app["func"]()
        break