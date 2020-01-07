import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

# Find city with lowest precipitation
totalCityPrecip = totals.sum(axis=1)
lowestCity = totalCityPrecip.idxmin(axis=1)

print("City with lowest total precipitation:")
print(lowestCity)

# Find Average monthly precipitation
totalMonthlyPrecip = totals.sum(axis=0)
totalMonthlyCount = counts.sum(axis=0)
avgMonthlyPrecip = totalMonthlyPrecip/totalMonthlyCount

print("Average precipitation in each month:")
print(avgMonthlyPrecip)

# Find Average precipitation in city
totalCityCount = counts.sum(axis=1)
avgCityPrecip = totalCityPrecip/totalCityCount

print("Average precipitation in each city:")
print(avgCityPrecip)
