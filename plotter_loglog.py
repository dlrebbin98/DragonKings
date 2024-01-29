import matplotlib.pyplot as plt
import json

def plot_last_values_distribution():
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
    with open('exports/results.txt', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Get the last value of the dictionary
                last_value = list(data.values())[-1]

                # Round the last value to handle floating-point variations
                last_value_rounded = round(last_value, 2)

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
    plt.plot(list(probabilities.keys()), list(probabilities.values()), marker='^', linestyle='None')

    plt.show()

# Call the function
plot_last_values_distribution()
