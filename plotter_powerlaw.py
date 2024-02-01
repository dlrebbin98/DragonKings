import json
import numpy as np
import powerlaw
import matplotlib.pyplot as plt

def plot_distribution_powerlaw(nodes=1000):
    # Initialize the plot
    plt.figure()
    plt.xlabel('Failure Size')
    plt.ylabel('Probability')
    plt.title('Log-Log PDF of Failure Sizes')
    plt.grid(True)

    # Define the settings of m for which you have exported results
    m_values = [2, 5, 10, 15] # range(10, 16, 5)

    # Choose a color map for the gradient
    color_map = plt.get_cmap('viridis')

    # Loop over different settings of m
    for m in m_values:
        all_values = []

        # Loop over five runs
        for run in range(1, 15):
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

                        last_value_int = int(last_value_rounded*1000)

                        print(last_value_int)

                        all_values.append(last_value_int)

                    except json.JSONDecodeError:
                        # Handle JSON decoding errors
                        pass

        # Create a powerlaw Fit object
        fit = powerlaw.Fit(all_values, discrete=True)
        #print(fit.alpha)

        # Get color based on the m value
        color = color_map((m - min(m_values)) / (max(m_values) - min(m_values)))

        xmin = fit.power_law.xmin
        print(xmin)

        #p = fit.distribution_compare('power_law', 'lognormal')
        #print(p)

        # Plot the power-law fit on a log-log scale
        fit.plot_pdf(color=color, linewidth=2, label=f'm={m}', linestyle='-')

        # Fitted idealised power law
        fit.power_law.plot_pdf(color=color, linewidth=1, label=f'm={m}', linestyle='--')

    plt.xscale('log')
    plt.yscale('log')

    plt.legend()
    plt.show()

# Call the function
plot_distribution_powerlaw(nodes=1000)
