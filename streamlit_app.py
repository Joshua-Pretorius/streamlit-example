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

import pandas as pd
import folium
import streamlit as st

# Load the routes and airports data
url_routes = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'
url_airports = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
routes = pd.read_csv(url_routes, header=None, names=['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 'codeshare', 'stops', 'equipment'])
airports = pd.read_csv(url_airports, header=None, names=['id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'offset', 'dst', 'timezone'])

# Filter out rows with missing values in the source column of the routes DataFrame
routes = routes.dropna(subset=['source'])

# Merge the routes and airports data based on the source and destination airports
routes = pd.merge(routes, airports[['iata', 'latitude', 'longitude']], left_on='source', right_on='iata', how='left', suffixes=('_source', '_dest'))
routes = pd.merge(routes, airports[['iata', 'latitude', 'longitude']], left_on='dest', right_on='iata', how='left', suffixes=('_source', '_dest'))

# Create a map centered at (0, 0)
m = folium.Map(location=[0, 0], zoom_start=2)

# Add all routes as lines on the map
for index, row in routes.iterrows():
    source = (row['latitude_source'], row['longitude_source'])
    dest = (row['latitude_dest'], row['longitude_dest'])
    folium.PolyLine(locations=[source, dest], color='red', weight=1).add_to(m)

# Add zoom controls to the map
m.add_child(folium.plugins.LatLngPopup())
m.add_child(folium.plugins.MousePosition())
folium.plugins.Fullscreen(position='topright', title='Expand me', title_cancel='Exit fullscreen', force_separate_button=True).add_to(m)
folium.plugins.MiniMap(toggle_display=True).add_to(m)
folium.plugins.MeasureControl().add_to(m)
folium.plugins.ScrollZoomToggler().add_to(m)
folium.plugins.Geocoder().add_to(m)

# Display the map on Streamlit
st.write(m)
