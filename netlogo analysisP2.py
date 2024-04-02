# RP4 - Agent Based Model Analysis Part 2
# Ben Mazin
# 03/26/2024
# School of Interdisciplinary Science, McMaster University

# This script is used to analyze the results of the NetLogo simulation. It reads the results from the csv file and plots the results as histograms. 
$It also calculates the standard deviation of the results and saves the results to a csv file.

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


# save path for the results
save_path = '/Users/benmazin/Code Dev/RP 4/netlogo results/'

def plothist(data, title, xlabel, ylabel, save_path):
    data = data[np.isfinite(data)]
    bins = np.arange(0.5, 101.5, 1)

    hist_data, bin_edges = np.histogram(data, bins=bins, density=True)
    plt.hist(bin_edges[:-1], bins=bins, weights=hist_data, alpha=0.5, color='g', edgecolor='black')

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # List of distributions to test
    distributions = [stats.norm, stats.lognorm, stats.expon, stats.beta, stats.gamma, stats.weibull_min]

    sse = {}
    for distribution in distributions:
        try:
            params = distribution.fit(data)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]

            pdf = distribution.pdf(bin_centers, *arg, loc=loc, scale=scale)
            sse[distribution.name] = np.sum(np.power(hist_data - pdf, 2))
        except Exception as e:
            print(f"Could not fit {distribution.name} due to {e}")

    best_fit = min(sse, key=sse.get)
    best_params = distributions[distributions.index(getattr(stats, best_fit))].fit(data)

    x = np.linspace(min(data), max(data), 100)
    pdf = getattr(stats, best_fit).pdf(x, *best_params[:-2], loc=best_params[-2], scale=best_params[-1])
    plt.plot(x, pdf, 'k', linewidth=2, label=f"{best_fit} fit")

    plt.title(f"{title}\nBest fit: {best_fit}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(save_path, dpi=300)
    plt.close()

#open the csv from the preanalysis
results = pd.read_csv(save_path + 'results.csv')

# Plot an individual distribution for each category and save to a png in the same directory
plothist(results['ChemoTotalDead'], 'Total Dead with Doxorubicin Treatment', 'Total Dead', 'Frequency', save_path + 'ChemoTotalDeadHist.png')
plothist(results['ChemoPercentInfect'], 'Infection with Doxorubicin Treatment', 'Most Infected at One Time', 'Frequency', save_path + 'ChemoMostInfectHist.png')
plothist(results['NoChemoTotalDead'], 'Total Dead WITHOUT Doxorubicin Treatment', 'Total Dead', 'Frequency', save_path + 'NoChemoTotalDeadHist.png')
plothist(results['NoChemoPercentInfect'], 'Infection WITHOUT Doxorubicin Treatment', 'Most Infected at One Time', 'Frequency', save_path + 'NoChemoMostInfectHist.png')

data = results

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