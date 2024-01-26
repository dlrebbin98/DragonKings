import json

import matplotlib.pyplot as plt
import numpy as np


def plot_results(n_nodes=10_000):
    # Initialize the plot
    plt.figure()
    plt.xlabel('s')
    plt.ylabel('Pr(s)')
    # plt.xscale('log')
    plt.yscale('log')
    plt.title('Cascade Size Distribution')
    plt.grid(True)

    # Read the data from the file
    with open('exports/results.txt', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                # plt.plot(np.array(list(data.values()))* n_nodes, list(data.values()))
                plt.plot(dict(data).keys(), data.values())
                # print(dict(data).keys())
            except:
                # a zero entry is found
                pass
    
    plt.show()
            

plot_results()