import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

# Find Row with lowest precipitation
totalCityPrecip = np.sum(totals, axis=1)
totalCityCount = np.sum(counts, axis=1)

lowestCity = np.argmin(totalCityPrecip)
print("Row with lowest total precipitation:")
print(lowestCity)

# Find average monthly precipitation
totalMonthlyPrecip = np.sum(totals, axis=0)
totalMonthlyCount = np.sum(counts, axis=0)
avgMonthlyPrecip = totalMonthlyPrecip/totalMonthlyCount

print("Average precipitation in each month:")
print(avgMonthlyPrecip)

# Find average precipitation in each city
avgCityPrecip = totalCityPrecip/totalCityCount

print("Average precipitation in each city:")
print(avgCityPrecip)

# Find quarterly precipitation by reshape, sum, reshape
precipRowNum = totals.shape[0] #find num of rows(cities) in data array totals
quarterCityPrecip = totals.reshape(4*precipRowNum, 3)
quarterSumPrecip = np.sum(quarterCityPrecip, axis=1)
quarterTotalPrecip = quarterSumPrecip.reshape(precipRowNum, 4)

print("Quarterly precipitation totals:")
print(quarterTotalPrecip)
