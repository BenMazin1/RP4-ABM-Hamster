import numpy as np
import pandas as pd

data = pd.read_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/results.csv')

# calculate the standard deviation
std_dev1 = np.std(data['ChemoTotalDead'].dropna())
std_dev2 = np.std(data['NoChemoTotalDead'].dropna())
std_dev3 = np.std(data['ChemoPercentInfect'].dropna())
std_dev4 = np.std(data['NoChemoPercentInfect'].dropna())

# create a DataFrame to store the results
result = pd.DataFrame({'ChemoTotalDead_std_dev': [std_dev1],
                       'NoChemoTotalDead_std_dev': [std_dev2],
                       'ChemoPercentInfect_std_dev': [std_dev3],
                       'NoChemoPercentInfect_std_dev': [std_dev4]})

# save the DataFrame as a CSV file
result.to_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/std_dev_results.csv', index=False)
