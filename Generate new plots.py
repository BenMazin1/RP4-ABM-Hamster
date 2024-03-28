import pandas as pd
import matplotlib.pyplot as plt


results = pd.read_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/results.csv')

# Plot an individual distribution for each category and save to a png in the same directory
save_path = '/Users/benmazin/Code Dev/RP 4/netlogo results/'

results['ChemoTotalDead'].plot.kde()
plt.xlabel('Chemo Total Dead')
plt.savefig(save_path + 'ChemoTotalDeadDist.png', dpi=300)
plt.close()

results['ChemoPercentInfect'].plot.kde()
plt.xlabel('Chemo Percent Infect')
plt.savefig(save_path + 'ChemoPercentInfectDist.png', dpi=300)
plt.close()

results['NoChemoTotalDead'].plot.kde()
plt.xlabel('No Chemo Total Dead')
plt.savefig(save_path + 'NoChemoTotalDeadDist.png', dpi=300)
plt.close()

results['NoChemoPercentInfect'].plot.kde()
plt.xlabel('No Chemo Percent Infect')
plt.savefig(save_path + 'NoChemoPercentInfectDist.png', dpi=300)
plt.close()
