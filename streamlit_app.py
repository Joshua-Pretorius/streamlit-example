from collections import namedtuple
import altair as alt
import math
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd

###Cleaning data

airlines = pd.read_csv('airlines.dat', header=None)
airline_col = ['Airline ID', 'Name', 'Alias', 'IATA', 'ICAO', 'Callsign', 'Country', 'Active']
airlines.columns = airline_col
## r Clean data - Airlines
#drop coloumns
airlines = airlines.drop(['Alias', 'IATA', 'ICAO', 'Callsign'], axis = 1)

#Drop all non active airlines
mask = airlines['Active'] == 'Y'
airlines = airlines[mask]

# remove first row
airlines.drop(0)

airports = pd.read_csv('airports.dat', header=None)
airport_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source']
airports.columns = airport_col
#J-Drop uneccesary columns in the airports table
airports = airports.drop(['DST','Tz database time zone','Type','Source','Timezone'], axis=1)
#J-Replace missing values with NaN and convert to float
import numpy as np
airports['Latitude'] = airports['Latitude'].replace('\\N', np.nan).astype(float)
airports['Longitude'] = airports['Longitude'].replace('\\N', np.nan).astype(float)

countries = pd.read_csv('countries.dat', header=None)
country_col = ['Name', 'ISO Code', 'DAFIF Code']
countries.columns = country_col
## r Clean Data Countries
#drop columns
countries = countries.drop(['DAFIF Code'], axis = 1)

planes = pd.read_csv('planes.dat', header=None)
plane_col = ['Name', 'IATA code', 'ICAO code']
planes.columns = plane_col

routes = pd.read_csv('routes.dat', header=None)
route_col = ['Airline', 'Airline ID', 'Source airport', 'Source airport ID', 'Destination airport', 'Destination airport ID', 'Codeshare', 'Stops', 'Equipment']
routes.columns = route_col
#J-Drop uneccesary columns in the routes table
routes = routes.drop(['Airline','Codeshare','Stops','Equipment'], axis=1)


# create the web application using streamlit
st.set_page_config(page_title="OpenFlights Dashboard", page_icon="✈️", layout="wide", initial_sidebar_state = 'expanded')

##style - Custom styles from styles.css
with open ('style.css') as f:
  st.markdown(f'<style>{f.read()}</styles', unsafe_allow_html = True)
#Set titles and subheadings
st.title("OpenFlights Dashboard")
#Sidebar
st.sidebar.hearder('Testing..1,2')

st.header("Airline Data")
st.write(airlines)
st.subheader("Airline Count by Country")
airline_counts = airlines.groupby("Country").size().reset_index(name="Count")
fig1 = px.bar(airline_counts, x="Country", y="Count", color="Country", title="Airline Count by Country")
st.plotly_chart(fig1, theme = 'streamlit')

import streamlit as st
import pandas as pd
import folium
import numpy as np


###MAP
## Joining tables
# Convert the Airport ID's to string for the join
airports['Airport ID'] = airports['Airport ID'].astype(str)
routes['Source airport ID'] = routes['Source airport ID'].astype(str)
routes['Destination airport ID'] = routes['Destination airport ID'].astype(str)


# Join the airports table twice to the routes table- The resu
source_airport_info = airports[['Airport ID', 'Latitude', 'Longitude']]
source_airport_info.columns = ['Source airport ID', 'Source Latitude', 'Source Longitude']

destination_airport_info = airports[['Airport ID', 'Latitude', 'Longitude']]
destination_airport_info.columns = ['Destination airport ID', 'Destination Latitude', 'Destination Longitude']

joined_table = pd.merge(routes, source_airport_info, on='Source airport ID', how='left')
join = pd.merge(joined_table, destination_airport_info, on='Destination airport ID', how='left')

##inintialize map
import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import folium_static

# Clean the lattitude data
join['Source Latitude'] = join['Source Latitude'].dropna().astype(float)
join['Source Longitude'] = join['Source Longitude'].dropna().astype(float)
join['Destination Latitude'] = join['Destination Latitude'].dropna().astype(float)
join['Destination Longitude'] = join['Destination Longitude'].dropna().astype(float)
# Load the joined table
routes = join.dropna()

# Create a map centered on the first route's source airport
m = folium.Map(location=[routes.iloc[0]['Source Latitude'], routes.iloc[0]['Source Longitude']], zoom_start=3)

# Define a function to plot the routes on the map
def plot_routes(routes, airline_filter=None):
    # Filter the routes by airline if an airline filter is provided
    if airline_filter:
        routes = routes[routes['Airline'] == airline_filter]
    
    # Create a feature group for the routes
    route_fg = folium.FeatureGroup(name='Routes')

    # Loop through the routes and plot them on the map
    for index, row in routes.iterrows():
        # Get the source and destination coordinates
        source_coords = [row['Source Latitude'], row['Source Longitude']]
        dest_coords = [row['Destination Latitude'], row['Destination Longitude']]

        # Create a polyline connecting the source and destination airports
        route_line = folium.PolyLine(locations=[source_coords, dest_coords], color='blue', weight=2, opacity=0.7, smooth_factor=1)
        route_line.add_to(route_fg)

    # Add the route feature group to the map
    route_fg.add_to(m)

    # Add a layer control to the map
    folium.LayerControl().add_to(m)

# Add a dropdown menu to filter routes by airline
airline_list = routes['Airline ID'].unique().tolist()
airline_filter = st.sidebar.selectbox('Filter by airline:', ['All'] + airline_list)
if airline_filter == 'All':
    airline_filter = None

# Plot the routes on the map
plot_routes(routes, airline_filter)

# Display the map in Streamlit
folium_static(m)





### CHART _ 






