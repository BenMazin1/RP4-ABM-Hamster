import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram_with_normal_curve(data):
    
    # Calculate the mean and standard deviation
    mu = np.mean(data)
    sigma = np.std(data)
    
    # Create the histogram of the data
    count, bins, ignored = plt.hist(data, bins=30, density=True, alpha=0.5, color='g', edgecolor='black')

    # Generate points on the x axis
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    
    # Calculate the normal distribution values
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    
    # Plot the normal distribution curve
    plt.plot(x, y, linewidth=2, color='r')

    # Adding titles and labels
    plt.title('Histogram with Normal Distribution Curve')
    plt.xlabel('Data Points')
    plt.ylabel('Probability Density')

    # Show the plot
    plt.show()

# Load the data
data = pd.read_csv('/Users/benmazin/Code Dev/RP 4/netlogo results/results.csv')

# Plot the histogram with normal curve
plot_histogram_with_normal_curve(data['ChemoTotalDead'])
plot_histogram_with_normal_curve(data['ChemoPercentInfect'])
plot_histogram_with_normal_curve(data['NoChemoTotalDead'])
plot_histogram_with_normal_curve(data['NoChemoPercentInfect'])
