# RP4 - Agent Based Model Analysis Part 2
# Ben Mazin
# 03/26/2024
# School of Interdisciplinary Science, McMaster University

# This script is used to analyze the results of the NetLogo simulation. It reads the results from the csv file and plots the results as histograms. 
# It also calculates the standard deviation of the results and saves the results to a csv file.

# Import the necessary libraries
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


# save path for the results
save_path = '/Users/benmazin/Code Dev/RP 4/netlogo results/'

def plothist(data, figureTitle, xlabel, ylabel, ax, label):

    # Remove NaN values and create bins
    data = data[np.isfinite(data)]
    bins = np.arange(0.5, 101.5, 2)

    # Plot the histogram
    hist_data, bin_edges = np.histogram(data, bins=bins, density=True)
    ax.hist(bin_edges[:-1], bins=bins, weights=hist_data, alpha=0.7, color='skyblue', edgecolor='black', linewidth=1.5)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # List of distributions to test
    distributions = [stats.norm, stats.lognorm, stats.expon, stats.beta, stats.gamma, stats.weibull_min]

    # Fit the distributions to the data
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

    # Get the best fit
    best_fit = min(sse, key=sse.get)
    best_params = distributions[distributions.index(getattr(stats, best_fit))].fit(data)

    # Plot the best fit
    x = np.linspace(min(data), max(data), 100)
    pdf = getattr(stats, best_fit).pdf(x, *best_params[:-2], loc=best_params[-2], scale=best_params[-1])
    ax.plot(x, pdf, 'k', linewidth=3, label=f"{best_fit} fit")

    # Add the title and labels
    ax.set_title(figureTitle, fontsize=20)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.legend(fontsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=10)
    ax.text(0.05, 0.95, label, transform=ax.transAxes, fontsize=50, fontweight='bold', verticalalignment='top')

#open the csv from the preanalysis
results = pd.read_csv(save_path + 'results.csv')

# Plot an individual distribution for each category and save to a png in the same directory
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
plothist(results['ChemoTotalDead'], 'Total Dead with Doxorubicin Treatment', 'Total Dead', 'Frequency', axs[0, 0], 'A')
plothist(results['NoChemoTotalDead'], 'Total Dead WITHOUT Doxorubicin Treatment', 'Total Dead', 'Frequency', axs[0, 1], 'B')
plothist(results['ChemoPercentInfect'], 'Infection with Doxorubicin Treatment', 'Most Infected at One Time', 'Frequency', axs[1, 0], 'C')
plothist(results['NoChemoPercentInfect'], 'Infection WITHOUT Doxorubicin Treatment', 'Most Infected at One Time', 'Frequency', axs[1, 1], 'D')

# Save the figure
plt.tight_layout(pad=1.0, h_pad=3.0, w_pad=2.0)
plt.savefig(save_path + 'combined_histograms.png', dpi=300)
plt.close()

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