import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster

# Load datasets
airports_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',
                          header=None, names=['airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst', 'tz'])
routes_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat',
                        header=None, names=['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 'codeshare', 'stops', 'equipment'])

# Set up the layout
st.set_page_config(page_title="Airports", page_icon=":airplane:", layout="wide")
st.title("Airports")

# Create the sidebar
st.sidebar.title("Select an option:")
option = st.sidebar.selectbox("", ["Number of airports in each country", "Number of routes per airline", "Number of routes per source airport"])

# Define the main panel
st.write("## " + option)

# Create the figures
if option == "Number of airports in each country":
    airports_per_country = airports_df.groupby('country').size().reset_index(name='count')
    fig = px.bar(airports_per_country, x='country', y='count', title='Number of airports in each country')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Number of routes per airline":
    routes_per_airline = routes_df.groupby('airline').size().reset_index(name='count')
    fig = px.bar(routes_per_airline, x='airline', y='count', title='Number of routes per airline')
    st.plotly_chart(fig, use_container_width=True)

else:
    routes_per_source_airport = routes_df.groupby('source').size().reset_index(name='count')
    fig = px.bar(routes_per_source_airport, x='source', y='count', title='Number of routes per source airport')
    st.plotly_chart(fig, use_container_width=True)

# Create the map
st.write("## Map of Airports")
m = folium.Map(location=[30, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(m)
for _, row in airports_df.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(marker_cluster)
st.markdown(folium_static(m))


