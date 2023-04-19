from collections import namedtuple
import altair as alt
import math
import pandas as pd
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
