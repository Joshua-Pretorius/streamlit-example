from collections import namedtuple
import altair as alt
import math
import pandas as pd
import plotly.express as px
import streamlit as st

airlines = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat",
                       header=None, names=["Airline ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"])
airports = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat",
                       header=None, names=["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone"])
routes = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat",
                     header=None, names=["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"])

# create the web application using streamlit
st.set_page_config(page_title="OpenFlights Dashboard", page_icon="✈️", layout="wide")
st.title("OpenFlights Dashboard")

st.header("Airline Data")
st.write(airlines)
st.subheader("Airline Count by Country")
airline_counts = airlines.groupby("Country").size().reset_index(name="Count")
fig1 = px.bar(airline_counts, x="Country", y="Count", color="Country", title="Airline Count by Country")
st.plotly_chart(fig1, theme = 'streamlit')

import streamlit as st
import pandas as pd
import numpy as np
import folium

# Load airports and routes data
airports = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',
                       header=None,
                       names=['airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude',
                              'timezone', 'dst', 'tz'],
                       na_values='\\N')

routes = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat',
                     header=None,
                     names=['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 'codeshare', 'stops',
                            'equipment'])

# Replace missing values with NaN and convert to float
airports['latitude'] = pd.to_numeric(airports['latitude'], errors='coerce')
airports['longitude'] = pd.to_numeric(airports['longitude'], errors='coerce')

# Concatenate the airport latitude and longitude columns into a new dataframe
airport_coords = pd.concat([airports['iata'], airports[['latitude', 'longitude']].astype(float)], axis=1)

# Merge airport data to get latitude and longitude for each airport
routes = pd.merge(routes, airport_coords, left_on='source', right_on='iata', how='left', suffixes=('_source', '_dest'))
routes = pd.merge(routes, airport_coords, left_on='dest', right_on='iata', how='left', suffixes=('_source', '_dest'))

# Create a list of unique airline names for dropdown menu
airline_names = sorted(routes['airline'].unique())

# Create a map centered at 0, 0 coordinates
m = folium.Map(location=[0, 0], zoom_start=2)

# Add markers for each airport
for _, row in airports.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Add flight routes for the selected airline
selected_airline = st.sidebar.selectbox('Select airline', airline_names)
selected_routes = routes[routes['airline'] == selected_airline]

for _, row in selected_routes.iterrows():
    folium.PolyLine(locations=[[row['latitude_source'], row['longitude_source']],
                               [row['latitude_dest'], row['longitude_dest']]], color='blue').add_to(m)

# Display the map
st.markdown(folium.Map().get_root().render(), unsafe_allow_html=True)




