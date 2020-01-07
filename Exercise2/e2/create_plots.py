import sys
import pandas as pd
import matplotlib.pyplot as plt

# Get cmd line args as strings with built-in sys module
filename1 = sys.argv[1]
filename2 = sys.argv[2]


data1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
data2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])

# Plot 1: Distribution of Views (data)
# Using only first input file sort the data by the number of pageviews
sorted1 = data1.sort_values('views',ascending=False)

# Plot 2: Daily Views (data)
# Copy a series from one DataFrame to another. Copy views from data1 -> data2

data2['data1views'] = data1['views']

# Plot the two graphs
plt.figure(figsize=(12, 6)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.title('Population Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')
plt.plot(sorted1['views'].values) # build plot 1

plt.subplot(1, 2, 2) # ... and then select the second
plt.title('Daily Correlation')
plt.xlabel('Day 1 Views')
plt.xlabel('Day 2 Views')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0.8,1000)
plt.ylim(0.8,1000)
plt.scatter(data2['data1views'],data2['views']) # build plot 2
#plt.show()
plt.savefig('wikipedia.png')