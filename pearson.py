from scipy.stats.stats import pearsonr
import scipy
import random 

a = scipy.array([2.,2.,2.])
b = scipy.array([2.,2.,0.])

print a
pearson = pearsonr(a, b)
print pearson