'''
This module contains an implementation of the 'self-organized dragon king' model by Lin et al (2018).

The model consists of two versions:
    1. Inoculation or IN:
        a. Nodes of status 1 (weak) fail if 1 or more neighbors fail.
        b. Nodes of status 2 (strong) cannot fail.

    2. Complex contagion or CC:
        a. Nodes of status 1 (weak) fail if 1 or more neighbors fail.
        b. Nodes of status 2 (strong) fail if 2 or more neighbors fail.

Running this module as a script run an example.
'''


import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from network import Network
from network_modifier import degrade, fail, save_state, load_state


class Inoculation:
    
    '''
    Class to simulate the inoculation version of the self-organized dragon king model.
    '''

    def __init__(self, n_nodes, n_edges=None, pr_edge=None, epsilon=0.2, n_steps=1000, n_trials=100, verbose=False):
        '''
        Description
        -----------
        Initializes the model and simulation environment.

        Parameters
        ----------
        `n_nodes` : int
            The number of nodes in the network.
        `n_edges` : int
            The number of edges in the network.
        `pr_edge` : float
            The probability that two nodes will be connected.
        `epsilon` : float
            The probability that a weak node will be repaired as strong.
        `n_steps` : int
            The number of steps in a trial.
        `n_trials` : int
            The number of trials.
        '''

        # Initialize the network
        self.n_nodes = n_nodes
        self.network = Network(n_nodes, n_edges, pr_edge)
        
        # Initialize the state
        self.network.set_all_statuses(1)

        # Initialize the results
        results = np.zeros((n_trials, n_steps))
        self.results = results.astype(int)

        # Initialize the parameters
        self.epsilon = epsilon
        self.n_steps = n_steps
        self.n_trials = n_trials
        
        # Initialize the current step
        self.current_step = 0

        # Initialize the verbose flag
        self.verbose = verbose

    def run(self):
        '''
        Description
        -----------
        Runs the simulation.
        '''
        self._visualize_network()
        # Loop through trials
        for trial in np.arange(self.n_trials):
            
            # Loop through the number of steps
            for step in np.arange(1, self.n_steps + 1):
                
                # Update the current step
                self.current_step = step
                print(f"Starting trial {trial} of {self.n_trials}  |  Step {step} of {self.n_steps}") if self.verbose else None
                
                # Execute a single step
                self.step()
            
            # # Save the results
            # self.results[trial] = self.network.get_all_statuses()
            # self.network.reset()

        self._visualize_network()

    
    def step(self):
        '''
        Description
        -----------
        Runs a single step of the simulation.
        '''
        
        # Save the current state (only used in cases of failure during degradation)
        before_degrade = save_state(self.network)

        # Degrade a node at random
        degrade(self.network, random=True)

        # Check for failed nodes
        if self.contains_failed_nodes():
            
            # Cascade failures until no more failures occur
            self.cascade_failures()

            return
        
        # If no failed nodes, move on to next step
        else:
            return
    

    def cascade_failures(self):
        '''
        Description
        -----------
        Cascades failures until no more failures occur.
        '''
        # Initialize previous state
        previous_state = None
        while previous_state != self.network.get_all_statuses():
            # Find failed nodes
            print(np.array(self.network.get_all_statuses()) == 0) if self.verbose else None
            failed_nodes = np.argwhere(np.array(self.network.get_all_statuses()) == 0)
            print(f"Found the following failured nodes: {failed_nodes}") if self.verbose else None
            break
            # previous_state = save_state(self.network)
            # self.process_neighbors()


    def contains_failed_nodes(self):
        '''
        Description
        -----------
        Checks if the network contains failed nodes.

        Returns
        -------
        `True` if the network contains failed nodes, `False` otherwise.
        '''
        print(f'Result of contains_failed_nodes method: {0 in self.network.get_all_statuses().values()}') if self.verbose else None
        print(f'Found the following failured nodes: {np.argwhere(np.array(self.network.get_all_statuses().values()) == 0)}') if self.verbose else None
        return 0 in self.network.get_all_statuses().values()
    

    def _get_failure_size(self):
        '''
        Description
        -----------
        Returns the proportion of nodes with status = 0.
        '''
        status_values = self.network.get_all_statuses().values()
        if len(status_values) != self.n_nodes:
            raise ValueError("Length of all statuses does not match the specified number of nodes.")
        
        failures = status_values.count(0)

        return failures / len(status_values)
    

    def _visualize_network(self):
        '''
        Description
        -----------
        Visualize the network.
        
        red: failed nodes.
        yellow: weak nodes.  
        green: strong nodes.
        '''
        nx.draw(
                self.network.graph, 
                node_color=['red' if self.network.graph.nodes[node]['status'] == 0 else ('yellow' if self.network.graph.nodes[node]['status'] == 1 else 'green') for node in self.network.graph.nodes]
                )
        plt.title(f"Time Step: {self.current_step}")
        plt.show()



def complex_contagion():
    pass


if __name__ == "__main__":

    ### EXAMPLE USAGE ###
    simulation = Inoculation(n_nodes=100, n_edges=300_000, epsilon=0.2, n_steps=1, n_trials=1, verbose=True)
    simulation.run()
