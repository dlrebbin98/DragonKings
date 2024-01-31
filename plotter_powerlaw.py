import json
import numpy as np
import powerlaw
import matplotlib.pyplot as plt

def plot_distribution_powerlaw(nodes=1000):
    # Initialize the plot
    plt.figure()
    plt.xlabel('Last Value')
    plt.ylabel('Probability')
    plt.title('Log-Log Distribution of Last Values for Nodes == 1000')
    plt.grid(True)

    # Define the settings of m for which you have exported results
    m_values = range(1, 11)

    # Choose a color map for the gradient
    color_map = plt.get_cmap('viridis')

    # Loop over different settings of m
    for m in m_values:
        all_values = []

        # Loop over five runs
        for run in range(1, 3):
            filename = f'exports/results_n{nodes}_m{m}_r{run}.txt'

            # Read the data from the file
            with open(filename, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)

                        # Get the last value of the dictionary
                        last_value = list(data.values())[-1]

                        # Round the last value to handle floating-point variations
                        last_value_rounded = round(last_value, 3)

                        all_values.append(last_value_rounded)

                    except json.JSONDecodeError:
                        # Handle JSON decoding errors
                        pass

        # Create a powerlaw Fit object
        fit = powerlaw.Fit(all_values, discrete=True)

        #print(all_values)

        # Get color based on the m value
        color = color_map((m - min(m_values)) / (max(m_values) - min(m_values)))

        # Plot the power-law fit on a log-log scale
        fit.plot_pdf(color=color, linewidth=2, label=f'm={m}', linestyle='-')

    plt.xscale('log')
    plt.yscale('log')

    plt.legend()
    plt.show()

# Call the function
plot_distribution_powerlaw(nodes=1000)
