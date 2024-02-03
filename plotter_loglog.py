'''
	Description
	-----------
	Takes the last values from the dictionary and draws a loglog plot with the probability distribution 
    of proportion of nodes affected by cascades following the failure of one randomly selected one.
'''

import matplotlib.pyplot as plt
import json

def plot_last_values_distribution(nodes = 1000, m = 1, run = 1):
    # Initialize the plot
    plt.figure()
    plt.xlabel('Proportion of Nodes Affected')
    plt.ylabel('Probability')
    plt.yscale('log')
    plt.xscale('log')
    plt.title('Distribution of Cascade Sizes')
    plt.grid(True)

    # Initialize a dictionary to store the frequency distribution of last values
    last_values_distribution = {}

    # Variable to store the total number of lines in the file
    total_lines = 0

    # Read the data from the file
    with open(f'exports/results_n{nodes}_m{m}_r{run}.txt', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Get the last value of the dictionary
                last_value = list(data.values())[-1]

                # Round the last value to handle floating-point variations
                last_value_rounded = round(last_value, 3)

                # Update the frequency distribution
                last_values_distribution[last_value_rounded] = last_values_distribution.get(last_value_rounded, 0) + 1

                # Increment total_lines
                total_lines += 1

            except json.JSONDecodeError:
                # Handle JSON decoding errors
                pass

    # Calculate probabilities by dividing frequencies by total_lines
    probabilities = {key: value / total_lines for key, value in last_values_distribution.items()}

    # Plot the probability distribution of last values using triangles
    plt.plot(list(probabilities.keys()), list(probabilities.values()), marker='o', linestyle='None')

    plt.show()

# Call the function
plot_last_values_distribution(nodes = 1000, m = 7, run = 4)
