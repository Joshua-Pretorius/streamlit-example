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
import folium

# Replace missing values with NaN
airport_locs = airports[['IATA', 'Latitude', 'Longitude']]
airport_locs['Latitude'] = airport_locs['Latitude'].replace('\\N', np.nan).astype(float)
airport_locs['Longitude'] = airport_locs['Longitude'].replace('\\N', np.nan).astype(float)

# Merge dataframes using pd.concat
routes = pd.concat([routes, airport_locs.rename(columns={'IATA': 'Source airport'})[['Source airport', 'Latitude', 'Longitude']]], axis=1)
selected_routes = routes[(routes['Source airport'] == selected_airport) & (routes['Destination airport'] != selected_airport)]

# Drop rows with NaN values
selected_routes = selected_routes.dropna()

# Display selected routes
st.write(f"## Available routes from {selected_airport}")
st.dataframe(selected_routes[['source', 'dest', 'airline']])










