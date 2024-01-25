'''
This module contains an implementation of the 'self-organized dragon king' model by Lin et al (2018).

The model consists of two versions:
    1. Inoculation or IN:
        a. Nodes of status 1 (weak) fail if 1 or more neighbors fail.
        b. Nodes of status 2 (strong) cannot fail.
    
    2. TODO Complex contagion or CC:
        a. Nodes of status 1 (weak) fail if 1 or more neighbors fail.
        b. Nodes of status 2 (strong) fail if 2 or more neighbors fail.

Running this module as a script run an example.
'''


import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from network import Network
from network_modifier import degrade, fail, save_state, load_state, reinforce


class Inoculation:
    
    '''
    Class to simulate the inoculation version of the self-organized dragon king model.
    '''

    def __init__(self, n_steps, n_trials, n_nodes, n_edges=None, pr_edge=None, epsilon=0.2, verbose=False, visualize=False, export_results=False):
        '''
        Description
        -----------
        Initializes the model and simulation environment.

        Parameters
        ----------
        `n_steps` : int
            The number of steps in a trial.
        `n_trials` : int
            The number of trials.
        `n_nodes` : int
            The number of nodes in the network.
        `n_edges` : int
            The number of edges in the network.
        `pr_edge` : float
            The probability that two nodes will be connected.
        `epsilon` : float
            The probability that a weak node will be repaired as strong.
        `verbose` : bool
            Whether whether, per step, progression should be broadcasted. Replaces the default progress bar. 
        `visualize` : 
            Whether, per step, progression should be plotted. CAUTION only use with very small `n_nodes`.
        `export_results` : str or False
            Whether the results should be exported to a csv file. If `False` (default), no export will take place. 
            Otherwise, the string should contain the path to the export directory (see example usage).
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
        self.time = 0

        # Initialize flags
        self.verbose = verbose
        self.visualize = visualize
        self.export_results = export_results

    def run(self):
        '''
        Description
        -----------
        Runs the simulation.
        '''
        # Loop through trials
        for trial in np.arange(1, self.n_trials + 1):
            
            # Loop through the number of steps
            for step in np.arange(1, self.n_steps + 1):
                
                # Update the current step
                self.time = step

                if not self.verbose:
                    # If verbose is False (default), display a progress bar
                    print(f"Starting trial {trial} of {self.n_trials}  |  Step {step} of {self.n_steps}               ", end='\r')
                
                # Execute a single step
                self.step()

        print('\nSimulation completed.')
            
            # # Save the results
            # self.results[trial] = self.network.get_all_statuses()
            # self.network.reset()

    
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

        if self.contains_failed_nodes():
            
            # Cascade failures until no more failures occur
            failed_nodes = self.cascade_failures()

            # Repair nodes
            load_state(self.network, before_degrade)

            # Reinforce some of the failed nodes with status 1 given epsilon
            reinforce(self.network, failed_nodes, self.epsilon)

            if self.visualize:
                return self._visualize_network()

        # Otherwise (i.e. no failure), end the step
        else:
            return self._visualize_network() if self.visualize else None
    

    def cascade_failures(self):
        '''
        Description
        -----------
        Cascades failures until no more failures occur.

        Returns
        -------
        An array containing all failed nodes of status 1.
        '''
        # Get current statuses as values
        current_state = np.array(list(self.network.get_all_statuses().values()))

        # Initialize previous state to save
        previous_state = np.zeros_like(current_state)
        
        # Cycle until no more changes in status occur
        # TODO refactor to eliminate additional cycle after all nodes have failed
        while not (previous_state == current_state).all():
            
            # Update previous state
            previous_state = current_state
            
            # Find failed nodes
            failed_nodes = np.where(current_state==0)[0]
            
            # Locate neighbors
            all_neighbors = self.network.get_multiple_neighbors(failed_nodes)
            
            # Cycle through neighbors (multiple neighbors of multiple nodes) and locate weaklings
            for neighbors in all_neighbors:
                
                fail(self.network, list(neighbors))
            
            # Update current_state
            current_state = np.array(list(self.network.get_all_statuses().values()))

            # Visualize network
            self._visualize_network() if self.visualize else None
        
        return failed_nodes


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
        plt.title(f"Time Step: {self.time}")
        plt.show()


    def _export_results(self):
        '''
        Description
        -----------
        Exports the results to a csv file.
        '''
        pass



def complex_contagion():
    pass


if __name__ == "__main__":

    ### EXAMPLE USAGE ###
    simulation = Inoculation(
        n_steps=3, 
        n_trials=1, 
        n_nodes=10_000,  # N^5
        n_edges=30_000, 
        pr_edge=False,
        epsilon=0.2, 
        verbose=False, 
        visualize=False,
        export_results='exports/'
    )

    # # Visualize the network at t = 0
    # simulation._visualize_network()
    
    simulation.run()
