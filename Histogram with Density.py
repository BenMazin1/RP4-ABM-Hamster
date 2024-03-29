import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram_with_normal_curve(data, data_name, x_label):
    # Calculate the mean and standard deviation
    mu = np.mean(data)
    sigma = np.std(data)
    
    # Create the histogram of the data
    plt.hist(data, bins=50, density=True, alpha=0.5, color='g', edgecolor='black')

    # Generate points on the x axis
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    
    # Calculate the normal distribution values
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    
    # Plot the normal distribution curve
    plt.plot(x, y, linewidth=2, color='r')

    # Adding titles and labels
    plt.title('Histogram of ' + data_name)
    plt.xlabel(x_label)
    plt.ylabel('Probability Density')

    # save the plot
    plt.savefig(f'/Users/benmazin/Code Dev/RP 4/netlogo results/Histogram with Density{data_name}.png', dpi=300)
    plt.close()

# Load the data
data = pd.read_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/results.csv')

# Plot the histogram with normal curve
plot_histogram_with_normal_curve(data['ChemoTotalDead'], 'Total Death with Chemo Use', 'Total Death Count')
plot_histogram_with_normal_curve(data['NoChemoTotalDead'], 'Total Death without Chemo Use', 'Total Death Count')
plot_histogram_with_normal_curve(data['ChemoPercentInfect'], 'Infection Rate with Chemo Use', 'Maximum Infection Rate Over Trials')
plot_histogram_with_normal_curve(data['NoChemoPercentInfect'], 'Infection Rate without Chemo Use', 'Maximum Infection Rate Over Trials')
