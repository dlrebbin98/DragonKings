import matplotlib.pyplot as plt
import json

def plot_results(n_nodes=10_000):
    # Initialize the plot
    plt.figure()
    plt.xlabel('Failure Size')
    plt.ylabel('Pr(Failure Size)')
    plt.xscale('log')
    plt.yscale('log')  # Use log scale for both axes
    plt.title('Failure Size Distribution')
    plt.grid(True)

    # Initialize a dictionary to store the failure size distribution
    failure_distribution = {}

    # Read the data from the file
    with open('exports/results.txt', 'r') as f:
        total_nodes = 0  # Variable to store the total number of nodes in the network

        for line in f:
            try:
                data = json.loads(line)
                total_nodes = sum(data.values())  # Update total nodes for each time step

                for key, value in data.items():
                    key = int(key)  # Convert key to integer
                    probability = value / total_nodes
                    failure_distribution[key] = failure_distribution.get(key, 0) + probability

            except json.JSONDecodeError:
                # Handle JSON decoding errors
                pass

    # Plot the failure size distribution
    plt.plot(list(failure_distribution.keys()), list(failure_distribution.values()), marker='o')

    plt.show()

# Call the function
plot_results()
