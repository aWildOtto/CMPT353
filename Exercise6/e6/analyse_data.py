import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

csv_file = sys.argv[1]
data = pd.read_csv(csv_file)
#print(data)

print("Normal Test P Values -----------------------------------------------")
print("qs1 normal p value: " + str(stats.normaltest(data['qs1']).pvalue))
print("qs2 normal p value: " + str(stats.normaltest(data['qs2']).pvalue))
print("qs3 normal p value: " + str(stats.normaltest(data['qs3']).pvalue))
print("qs4 normal p value: " + str(stats.normaltest(data['qs4']).pvalue))
print("qs5 normal p value: " + str(stats.normaltest(data['qs5']).pvalue))
print("merge1 normal p value: " + str(stats.normaltest(data['merge1']).pvalue))
print("partition_sort normal p value: " + str(stats.normaltest(data['partition_sort']).pvalue))
print("--------------------------------------------------------------------")

print("Runtime Means ------------------------------------------------------")
qs1_mean = data['qs1'].mean()
qs2_mean = data['qs2'].mean()
qs3_mean = data['qs3'].mean()
qs4_mean = data['qs4'].mean()
qs5_mean = data['qs5'].mean()
merge1_mean = data['merge1'].mean()
partition_sort_mean = data['partition_sort'].mean()



print("qs1 runtime mean: " + str(qs1_mean))
print("qs2 runtime mean: " + str(qs2_mean))
print("qs3 runtime mean: " + str(qs3_mean))
print("qs4 runtime mean: " + str(qs4_mean))
print("qs5 runtime mean: " + str(qs5_mean))
print("merge1 runtime mean: " + str(merge1_mean))
print("partition_sort runtime mean: " + str(partition_sort_mean))
print("--------------------------------------------------------------------")

# anova to check if there is differende between means of group. If p < 0.05
anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
print("--------------------------------------------------------------------")
print("Anova p value: " + str(anova.pvalue))
print("--------------------------------------------------------------------")

# Because anova p < 0.05, perform Post Hoc Analysis
melt_data = pd.melt(data)
posthoc = pairwise_tukeyhsd(melt_data['value'].astype('float64'), melt_data['variable'], alpha=0.05)
print("Post Hoc Analysis")
print(posthoc)
