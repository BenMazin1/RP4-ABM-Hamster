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
from scipy.stats import norm, lognorm, expon


# save path for the results
save_path = '/Users/benmazin/Code Dev/RP 4/netlogo results/'

'''
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
    plt.savefig(save_path, dpi=300)
    plt.close()
'''

def plothist(data, title, xlabel, ylabel, save_path):
    data = data[np.isfinite(data)]
    bins = np.arange(0.5, 101.5, 1)

    plt.hist(data, bins=bins, density=True, alpha=0.5, color='g', edgecolor='black')

    # Fit different distributions and calculate the sum of squared errors (SSE)
    distributions = [norm, lognorm, expon]
    sse = {}
    for distribution in distributions:
        params = distribution.fit(data)
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        pdf = distribution.pdf(bins, loc=loc, scale=scale, *arg)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        sse[distribution.name] = np.sum(np.power(pdf - np.histogram(data, bins=bins, density=True)[0], 2))

    # Find the best fitting distribution
    best_fit = min(sse, key=sse.get)
    best_params = distributions[distributions.index(getattr(stats, best_fit))].fit(data)

    # Plot the best fitting distribution
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