import folium
import streamlit as st
from streamlit_folium import st_folium
import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
from folium.plugins import Draw
import io

load_dotenv()

username = os.environ.get('USERNAMEE')
password = os.environ.get('PASSWORD')


def get_geojson(date, hailsize):
    token = requests.get(
        f"https://gis.aes.accuweather.com/arcgis/tokens/generateToken?f=json&username={username}&password={password}").json()['token']
    url = f"https://gis.aes.accuweather.com/arcgis/rest/services/DataServices/Hail_Swaths_Combined/FeatureServer/0/query?where=date >= '{date}' and hailsize={hailsize}&outFields=*&returnGeometry=true&f=geojson&token={token}"
    url = url.replace(" ", "%20")

    r = requests.get(url)
    return r.json()


st.title('Hail Swaths')

date = st.date_input('Pick a Date', format="YYYY-MM-DD")

hailsize = st.selectbox(
    'Pick Hail Size', [0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3])

geojson = None

if not (os.path.exists(f'data/{date} {hailsize}.json')):
    geojson = get_geojson(date, hailsize)
    json_obj = json.dumps(geojson)
    with open(f'data/{date} {hailsize}.json', "w") as outfile:
        outfile.write(json_obj)
else:
    geojson = f'data/{date} {hailsize}.json'

m = folium.Map([43, -100], zoom_start=4)

folium.GeoJson(geojson).add_to(m)

st_folium(m, width=500, returned_objects=[])
