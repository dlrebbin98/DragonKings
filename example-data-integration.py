# import packages
import pandas as pd
import numpy as np
import random


# loading data
df = pd.read_csv('')

# normalizing prizes
df['Normalized_Price'] = (df['Price'] - df['Price'].mean()) / df['Price'].std()

# initializing simulation parameters
num_traders = 100
traders = np.zeros(num_traders)
time_steps = 50

# setting initial trader conditions based on normalized data
for i in range(num_traders):
    if i < len(df):
        traders[i] = 1 if df['Normalized_Price'].iloc[i] > 0 else -1


# defining Cellular Automata update function
def update_traders():
    for i in range(num_traders):
        if random.random() < 0.5:  # TODO: extend random decision to incorporate network influence and market trend
            traders[i] = -traders[i]  # flip trader state buy/sell


if __name__ == '__main__':
    for t in range(time_steps):
        
        # update simulation
        update_traders()

        # TODO: add spaghetti logic for processing trader states and market trend

        # print results
        print(f"Time step {t}, Trader states: {traders}")


# TODO: maybe add feedback loops & real-time data
