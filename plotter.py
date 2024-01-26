import json

import matplotlib.pyplot as plt


def plot_results():
    # Read the data from the file
    with open('exports/results.txt', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                plt.plot(dict(data).keys(), data.values())
                # print(dict(data).keys())
            except:
                # a zero entry is found
                pass
            

plot_results()