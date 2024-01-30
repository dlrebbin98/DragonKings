'''
	Description
	-----------
	Takes the last values from the dictionary and draws a loglog plot with the probability distribution 
    of proportion of nodes affected by cascades following the failure of one randomly selected one.
'''

import json
import numpy as np
import matplotlib.pyplot as plt

def plot_distribution(nodes=1000):
    # Initialize the plot
    plt.figure()
    plt.xlabel('Last Value')
    plt.ylabel('Probability')
    plt.title('Log-Log Distribution of Last Values for Nodes == 1000')
    plt.grid(True)

    # Define the settings of m for which you have exported results
    m_values = range(3, 11, 7)

    # Choose a color map for the gradient
    color_map = plt.get_cmap('viridis')

    # Loop over different settings of m
    for m in m_values:
        all_probabilities = []

        # Loop over five runs
        for run in range(1, 6):
            filename = f'exports/results_n{nodes}_m{m}_r{run}.txt'

            # Initialize a dictionary to store the frequency distribution of last values
            last_values_distribution = {round(value, 3): 0.0 for value in np.arange(0, 1.001, 0.001)}

            # Variable to store the total number of lines in the file
            total_lines = 0

            # Read the data from the file
            with open(filename, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)

                        # Get the last value of the dictionary
                        last_value = list(data.values())[-1]

                        # Round the last value to handle floating-point variations
                        last_value_rounded = round(last_value, 3)

                        # Update the frequency distribution
                        last_values_distribution[last_value_rounded] += 1

                        # Increment total_lines
                        total_lines += 1

                    except json.JSONDecodeError:
                        # Handle JSON decoding errors
                        pass

            # Calculate probabilities by dividing frequencies by total_lines
            probabilities = {key: value / total_lines for key, value in last_values_distribution.items()}
            all_probabilities.append(list(probabilities.values()))

        # Calculate mean and standard deviation for each probability bin
        mean_probabilities = np.mean(all_probabilities, axis=0)
        std_dev_probabilities = np.std(all_probabilities, axis=0)

        # Get color based on the m value
        color = color_map((m - min(m_values)) / (max(m_values) - min(m_values)))

        # Plot the mean probability distribution of last values with error bands on a log-log scale
        plt.plot(list(probabilities.keys()), mean_probabilities, label=f'm={m}', marker='o', linestyle='-', color=color)
        #plt.fill_between(list(probabilities.keys()), mean_probabilities - std_dev_probabilities, mean_probabilities + std_dev_probabilities, alpha=0.3, color=color)

    # Set log scale for both axes
    plt.xscale('log')
    plt.yscale('log')

    plt.legend()
    plt.show()

# Call the function
plot_distribution(nodes=1000)

