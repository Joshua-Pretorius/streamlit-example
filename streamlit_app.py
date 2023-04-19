import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from folium.plugins import MarkerCluster

# Load datasets
airports_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',
                          header=None, names=['airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst', 'tz'])
routes_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat',
                        header=None, names=['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 'codeshare', 'stops', 'equipment'])

# Create the app
st.title("Airport Dashboard")

# Create figure 1: Number of airports in each country
airports_per_country = airports_df.groupby('country').size().reset_index(name='count')
fig1 = px.bar(airports_per_country, x='country', y='count', title='Number of airports in each country')

# Create figure 2: Number of routes per airline
routes_per_airline = routes_df.groupby('airline').size().reset_index(name='count')
fig2 = px.bar(routes_per_airline, x='airline', y='count', title='Number of routes per airline')

# Create figure 3: Number of routes per source airport
routes_per_source_airport = routes_df.groupby('source').size().reset_index(name='count')
fig3 = px.bar(routes_per_source_airport, x='source', y='count', title='Number of routes per source airport')

# Create the map
st.subheader("Airports around the world")
marker_cluster = MarkerCluster().add_to(folium.Map(location=[0, 0], zoom_start=2))
for _, row in airports_df.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(marker_cluster)

# Render the figures and map in the app
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st_folium_map(marker_cluster)


