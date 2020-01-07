import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

stations_data = sys.argv[1]
cities_data = sys.argv[2]
output = sys.argv[3]

stations_df = pd.read_json(stations_data, lines=True)
cities_df = pd.read_csv(cities_data)

# divide avg_tmax col elements by 10
stations_df['avg_tmax'] = stations_df['avg_tmax']/10

# select cities with finite(!NaN) population and area values
cities_df = cities_df[np.isfinite(cities_df['population'])]
cities_df = cities_df[np.isfinite(cities_df['area'])]
cities_df = cities_df.reset_index(drop=True)

# convert area values from m**2 to km**2
cities_df['area'] = cities_df['area']*0.000001

# create density column
cities_df['density'] = cities_df['population']/cities_df['area']

# select cities with area < 10000 km**2
cities_df = cities_df[cities_df['area'] < 10000].reset_index(drop=True)

# haversine formula
def distance(city, stations):
    lat1 = city['latitude']
    lon1 = city['longitude']
    lat2 = stations['latitude']
    lon2 = stations['longitude']
    a = np.sin((np.deg2rad(lat2-lat1))/2)*np.sin((np.deg2rad(lat2-lat1))/2)
    b = np.cos(np.deg2rad(lat1))*np.cos(np.deg2rad(lat2))
    c = np.sin((np.deg2rad(lon2-lon1))/2)*np.sin((np.deg2rad(lon2-lon1))/2)
    return 12742*np.arcsin(np.sqrt(a+b*c))

# function to be used in .apply() to find min distance of city to every station
# and return the avg_tmax of that station
def best_tmax(city, stations):
    stations['temp distance'] = distance(city, stations)
    loc_tmax = stations['temp distance'].idxmin(axis=1)
    
    return stations.loc[loc_tmax, 'avg_tmax']

# final dataframe
cities_df['avg_tmax'] = cities_df.apply(best_tmax,axis=1, stations = stations_df)

plt.scatter(cities_df['avg_tmax'], cities_df['density'])
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.savefig(output)