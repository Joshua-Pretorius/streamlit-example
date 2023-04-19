import pandas as pd
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

#####################################################
airports = pd.read_csv('airports.dat', header=None)
airport_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source']
airports.columns = airport_col
#J-Drop uneccesary columns in the airports table
airports = airports.drop(['DST','Tz database time zone','Type','Source','Timezone'], axis=1)
#J-Replace missing values with NaN and convert to float
import numpy as np
airports['Latitude'] = airports['Latitude'].replace('\\N', np.nan).astype(float)
airports['Longitude'] = airports['Longitude'].replace('\\N', np.nan).astype(float)

#################################################
countries = pd.read_csv('countries.dat', header=None)
country_col = ['Name', 'ISO Code', 'DAFIF Code']
countries.columns = country_col
## r Clean Data Countries
#drop columns
countries = countries.drop(['DAFIF Code'], axis = 1)

########################################################
planes = pd.read_csv('planes.dat', header=None)
plane_col = ['Name', 'IATA code', 'ICAO code']
planes.columns = plane_col

#####################################################
routes = pd.read_csv('routes.dat', header=None)
route_col = ['Airline', 'Airline ID', 'Source airport', 'Source airport ID', 'Destination airport', 'Destination airport ID', 'Codeshare', 'Stops', 'Equipment']
routes.columns = route_col
#J-Drop uneccesary columns in the routes table
routes = routes.drop(['Airline','Codeshare','Stops','Equipment'], axis=1)


