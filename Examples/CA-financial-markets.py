'''
NOTE: This code is a work in progess.

Outline of basic cellular automata methods that
incorporate advanced stochastic techniques for 
a financial market model.

This is a work in progress and is not intended
to be used for any purpose other than to
demonstrate the basic structure of the model.

This code is part of a project for the course
"Complex Systems Simulation" at the University
of Amsterdam, Computational Science MSc, 2024.

Assignment group 11

This module was authored by David Klein Leunk.
'''

# import libraries
import numpy as np
import random

# set parameters
num_traders = 100                                       # = active traders
traders = np.ones(num_traders)                         # trader states = {0: hold, 1: buy, -1: sell}
networks = np.random.rand(num_traders, num_traders)     # Network influence matrix
market_trend = 0                                        # market trends = {1: positive, -1: negative, 0: neutral}

class Market:

    def __init__(self, num_traders=100):
        '''
        Initializes the market with a set of traders
        and a network influence matrix.

        Parameters
        ----------
        num_traders : int, optional
            Number of traders in the market (default=100).
        '''
        self.num_traders = num_traders
        self.traders = np.random.random_integers(-1, 1, self.num_traders)
        self.networks = np.random.rand(self.num_traders, self.num_traders)
        self.market_trend = 0

    def run(self, timesteps=100):
        '''
        Runs the simulation for a given number of time steps.

        Parameters
        ----------
        timesteps : int, optional
            Number of time steps to run the simulation for (default=100).
        '''
        for t in range(timesteps):
            self.update_traders()
            self.update_market_trend()
            print(f"Time step {t}: Market Trend: {self.market_trend}, Trader States: {self.traders}")


    def update_traders(self):
        '''
        Updates trader states based on network influence and market trend.
        '''
        for i in range(self.num_traders):
            network_influence = np.dot(self.networks[i], self.traders)

            # Given that the trader is not holding, 
            # the probability of buying or selling 
            # is proportional to the network 
            # influence and market trend. 

            # Hence, the probability of buying is
            # abs(network_influence + market_trend)
            
            print(network_influence)
            print(self.market_trend)

            if random.random() < abs(network_influence) or random.random() < abs(market_trend):
                self.traders[i] = np.sign(network_influence + market_trend)
            
            else:
                self.traders[i] = 0


    def update_market_trend(self):
        '''
        Updates market trend based on trader actions.
        '''
        self.market_trend = np.sign(np.sum(self.traders))


    def sentiment_analysis():
        # TODO: implement sentiment analysis logic here, currently returns random value.
        return random.uniform(-1, 1)


if __name__ == "__main__":

    # initialize market
    market = Market(num_traders=100)

    # run simulation
    market.run(timesteps=1)

    # # output results
    # print(f"Final market trend: {market.market_trend}")
    # print(f"Final trader states: {market.traders}")
