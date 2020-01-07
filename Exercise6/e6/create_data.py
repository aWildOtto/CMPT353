import pandas as pd
import numpy as np
from implementations import all_implementations
import time
import sys

arr_sz = 500
sample_sz = 200
data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'], index=np.arange(sample_sz))

for i in range(sample_sz):
	random_array = np.random.randint(low = -1000, high = 1000, size = arr_sz)
	for sort in all_implementations:
		st = time.time()
		res = sort(random_array)
		en = time.time()
		total_time = en-st
		data.iloc[i][sort.__name__] = total_time


data.to_csv('data.csv', index=False)