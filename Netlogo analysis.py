# RP4 - Agent Based Model Analysis
# Ben Mazin
# 03/26/2024
# School of Interdisciplinary Science, McMaster University

# This script reads in the csv files from the Netlogo model and analyzes the data to determine if the chemo treatment is effective
# It then saves the results to a csv file

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Set the number of trials and initial hamsters
number_of_trials = 2000
initial_hamsters = 100

# save path for the results
save_path = '/Users/benmazin/Code Dev/RP 4/'

# Create an empty DataFrame with 4 columns
all_data = []

# Function to read CSV with inconsistent rows
def read_inconsistent_csv(file_path, delimiter=','):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Determine the maximum number of columns by checking all rows
    max_columns = max(len(line.split(delimiter)) for line in lines)

    # Split each line into columns and pad with None if they are too short
    data = [line.strip().split(delimiter) + [None] * (max_columns - len(line.split(delimiter))) for line in lines]

    # Convert the list of lists into a DataFrame
    df = pd.DataFrame(data, columns=range(max_columns))  # Set index to match column numbers
    return df

def plothist(data, title, xlabel, ylabel, save_path):
    
    data = data[np.isfinite(data)]
    bins = np.arange(0.5, 101.5, 1)

    count, bins, ignored = plt.hist(data, bins=bins, density=False, alpha=0.5, color='g', edgecolor='black')

    mu, std = norm.fit(data)

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    bin_width = np.diff(bins)[0]
    p = norm.pdf(x, mu, std) * len(data) * bin_width   
    plt.plot(x, p, 'k', linewidth=2)

    plt.title(title) 
    plt.xlim(0, 101)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(save_path)
    plt.close()

# Run for number_of_trials
for i in range(1, number_of_trials + 1):

    # Read in the csv file
    file_path = f'{save_path}output ABM/world{i}.csv'
    data = read_inconsistent_csv(file_path, delimiter=',')

    # Get the value of ChemoWork
    chemowork = data.iat[6, 5]
    if chemowork != '"true"' and chemowork != '"false"':
        chemowork = data.iat[6, 3]

    # Clean up the data
    data = data.iloc[18:]
    data = data.reset_index(drop=True)

    # Get the total dead and max percent infected
    total_dead = initial_hamsters - int(data.iloc[-1, 9].replace('"', ''))
    max_percent_infect = int(data.iloc[2:, 1].str.replace('"', '').astype(int).max())

    # Append the data to the proper list
    if chemowork == '"true"':
        all_data.append({
            'Trial': i,
            'ChemoTotalDead': total_dead,
            'ChemoPercentInfect': max_percent_infect,
            'NoChemoTotalDead': None,
            'NoChemoPercentInfect': None
        })
    
    elif chemowork == '"false"':
        all_data.append({
            'Trial': i,
            'ChemoTotalDead': None,
            'ChemoPercentInfect': None,
            'NoChemoTotalDead': total_dead,
            'NoChemoPercentInfect': max_percent_infect
        })

    else:
        print("Error: ChemoWork is not true or false")
        print(i)
    
    # Print the progress
    if i % 1000 == 0:
        print(f'{i} trials completed')

#save dataframe to csv
results = pd.DataFrame(all_data)

# get the mean for each data column
chemo_total_dead_mean = results['ChemoTotalDead'].mean()
chemo_percent_infect_mean = results['ChemoPercentInfect'].mean()
no_chemo_total_dead_mean = results['NoChemoTotalDead'].mean()
no_chemo_percent_infect_mean = results['NoChemoPercentInfect'].mean()

# run a t-test to determine if the means are significantly different for total dead and percent infect
totalDeadTtest = stats.ttest_ind(results['ChemoTotalDead'], results['NoChemoTotalDead'] , nan_policy='omit')
percentInfectTtest = stats.ttest_ind(results['ChemoPercentInfect'], results['NoChemoPercentInfect'], nan_policy='omit')

# create a new dataframe with the means and t-test results
resultSum = pd.DataFrame({
    'Category': ['ChemoTotalDeadMean', 'ChemoMostInfectMean', 'NoChemoTotalDeadMean', 'NoChemoMostInfectMean', 'TotalDeadTtest', 'MostInfectTtest'],
    'Value': [chemo_total_dead_mean, chemo_percent_infect_mean, no_chemo_total_dead_mean, no_chemo_percent_infect_mean, totalDeadTtest, percentInfectTtest]
})

# Plot an individual distribution for each category and save to a png in the same directory
save_path = save_path + 'netlogo results/'

plothist(results['ChemoTotalDead'], 'Chemo Total Dead', 'Total Dead', 'Frequency', save_path + 'ChemoTotalDeadHist.png')
plothist(results['ChemoPercentInfect'], 'Chemo most Infect', 'Most Infected at Once', 'Frequency', save_path + 'ChemoPercentInfectHist.png')
plothist(results['NoChemoTotalDead'], 'No Chemo Total Dead', 'Total Dead', 'Frequency', save_path + 'NoChemoTotalDeadHist.png')
plothist(results['NoChemoPercentInfect'], 'No Chemo Most Infect', 'Most Infected at Once', 'Frequency', save_path + 'NoChemoPercentInfectHist.png')


# save the summary and results to csv
resultSum.to_csv(save_path + 'summary.csv', index=False)
results.to_csv(save_path + 'results.csv', index=False)  