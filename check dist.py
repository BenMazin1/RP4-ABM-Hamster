import numpy as np
import pandas as pd
from fitter import Fitter, get_common_distributions, get_distributions

data = pd.read_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/results.csv')

# Fit the data to a distribution
f = Fitter(data['ChemoPercentInfect'].dropna().values)

f.fit()
f.summary()


print(f.get_best(method='sumsquare_error'))