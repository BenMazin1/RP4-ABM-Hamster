# RP4 - Agent Based Model Analysis
# Ben Mazin
# 03/26/2024
# School of Interdisciplinary Science, McMaster University

# This script reads in the csv files from the Netlogo model and analyzes the data to determine if the chemo treatment is effective
# It then saves the results to a csv file

import pandas as pd
from scipy import stats

# Set the number of trials and initial hamsters
number_of_trials = 20000
initial_hamsters = 100

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

# Run for number_of_trials
for i in range(1, number_of_trials + 1):

    # Read in the csv file
    file_path = f'/Users/benmazin/Movies/netlogo output/world{i}.csv'
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
    'Category': ['ChemoTotalDeadMean', 'ChemoPercentInfectMean', 'NoChemoTotalDeadMean', 'NoChemoPercentInfectMean', 'TotalDeadTtest', 'PercentInfectTtest'],
    'Value': [chemo_total_dead_mean, chemo_percent_infect_mean, no_chemo_total_dead_mean, no_chemo_percent_infect_mean, totalDeadTtest, percentInfectTtest]
})

# save the summary and results to csv
resultSum.to_csv('/Users/benmazin/Movies/netlogo results/summary.csv', index=False)
results.to_csv('/Users/benmazin/Movies/netlogo results/results.csv', index=False)  