'''
This module contains an altered implementation of the 'self-organized dragon king' model by Lin et al (2018).

The model consists of a version where a given number of nodes are randomly selected to fail, setting their status to 0
before all other neighbouring nodes are checked for whether their own status falls to 0 or below so that they fail themselves. 
The cascade continues until no more node is induced to fail.

Running this module as a script run an example.
'''

import json
import random

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from AB_network import Network
from AB_network_modifier import degrade, fail, save_state, load_state, reinforce


class Degree_Cascade:
    
    '''
    Class to simulate the inoculation version of the self-organized dragon king model.
    '''

    def __init__(self, n_steps, n_trials, n_nodes, n_edges=None, n_failures = None, threshold=None, verbose=False, visualize=False, export_dir=None):
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
            The number of edges added per node (=m)
        `n_failures` : int
            The number of failures induced in the network.
        `verbose` : bool
            Whether whether, per step, progression should be broadcasted. Replaces the default progress bar. 
        `visualize` : 
            Whether, per step, progression should be plotted. CAUTION only use with very small `n_nodes`.
        `export_dir` : str
            Whether the resulting failure size distributions should be exported. If `None` (default), no export will take place. 
            Otherwise, the string should contain the path to the export directory (e.g. 'exports/').
        '''

        # Initialize the network
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.network = Network(n_nodes, n_edges) # create AB network with n nodes and m edges
        
        # Initialize the state
        self.network.set_all_statuses() # all nodes initialised with status = degree

        # Initialize the parameters
        self.n_failures = n_failures # number of failures induced
        self.n_steps = n_steps
        self.n_trials = n_trials
        self.threshold = threshold
        
        # Initialize the current step
        self.time = 0

        # Initialize flags
        self.verbose = verbose
        self.visualize = visualize
        self.export_dir = export_dir

        # Initialize the export directory
        if export_dir is not None:
            self._initialize_results()


    def run(self):
        '''
        Description
        -----------
        Runs the simulation.
        '''
        # Loop through trials
        for self._itrial in np.arange(1, self.n_trials + 1):
            
            # Loop through the number of steps
            for self._istep in np.arange(1, self.n_steps + 1):
                
                if not self.verbose:
                    # If verbose is False (default), display a progress bar
                    print(f"Starting trial {self._itrial} of {self.n_trials}  |  Step {self._istep} of {self.n_steps}               ", end='\r')
                
                # Execute a single step
                self.step()

            # Re-initialize the network
            self.network = Network(self.n_nodes, self.n_edges)

        print('\nSimulation completed.')
        
        if self.exporting:
            self._export_results()
            print(f'Exported results to {self.export_dir}results.csv')


    def step(self):
        '''
        Description
        -----------
        Runs a single step of the simulation.
        '''
        # Randomly select given number of nodes to fail
        nodes_to_fail = np.random.choice(self.network.graph.nodes)

        # initiate the recursive cascade
        self.cascade_failures(nodes_to_fail)

        # Repair node statuses to represent their degree
        self.network.set_all_statuses()

        if self.visualize:
            return self._visualize_network()

        # Otherwise (i.e. no failure), end the step
        else:
            return self._visualize_network() if self.visualize else None
    
    def recursive_cascade(self, node):
        
        # Base case: Stop recursion if the node has already failed
        if self.network.get_status(node) < 1:
            return

        # Locate neighbors
        all_neighbors = self.network.get_neighbors(node)

        # retain previous status
        prev_status = self.network.get_status(node)

        # set status of failed node to 0
        self.network.set_status(node, 0)
            
        # Cycle through neighbors (multiple neighbors of multiple nodes) and locate weaklings
        for neighbor in all_neighbors:
            if self.network.get_status(neighbor) < prev_status:
                self.recursive_cascade(neighbor)

        # Store current cascade iteration
        self._store_cascade()  if self.exporting  else None

    def cascade_failures(self, node):
        '''
        Description
        -----------
        Cascades failures until no more failures occur.

        Returns
        -------
        An array containing all failed nodes of status 1.
        '''
        
        # Start tracking cascade
        self._initialize_cascade()  if self.exporting  else None

        # Call recursive failing function
        self.recursive_cascade(node)

        # Store results of step
        self._store_step_results() if self.exporting else None


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
    

    def _initialize_cascade(self):
        '''
        Description
        -----------
        Initialize a failure size array.
        '''
        self.cascade_dict = {}
        self.cascade_counter = -1
        self._store_cascade()


    def _get_cascade(self):
        '''
        Description
        -----------
        Returns the failure size and counter of current cascade.
        '''
        status_values = list(self.network.get_all_statuses().values())
        if len(status_values) != self.n_nodes:
            raise ValueError("Length of all statuses does not match the specified number of nodes.")

        failures = status_values.count(0)

        return self.cascade_counter, failures / len(status_values)


    def _store_cascade(self):
        '''
        Description
        -----------
        Stores a value in the cascade dict.
        '''
        self.cascade_counter += 1
        t, x = self._get_cascade()
        self.cascade_dict[t] = x


    def _visualize_network(self):
        '''
        Description
        -----------
        Visualize the network.
        
        red: failed nodes.
        yellow: weak nodes.  
        green: strong nodes.
        '''
        # Extract node statuses
        node_statuses = nx.get_node_attributes(self.network.graph, 'status')

        # Map colors based on node statuses
        node_colors = ['red' if status == 0 else 'green' for status in node_statuses.values()]

        # Draw the network with node labels
        pos = nx.spring_layout(self.network.graph)  # You can use other layout algorithms
        nx.draw(self.network.graph, pos, node_color=node_colors, with_labels=True, labels=node_statuses)
        
        plt.title(f"Time Step: {self.time}")
        plt.show()


    def _initialize_results(self):
        '''
        Description
        -----------
        Initializes the results array. 

        Used to track failure sizes over time, starting from 1st node failure.

        TODO switch to a pickle/file based approach to secure intermittent results.
        '''
        self.exporting = True
        self.results = [[0]*self.n_steps]*self.n_trials

    def _store_step_results(self):
        '''
        Description
        -----------
        Stores results of a step.
        '''
        self.results[self._itrial - 1][self._istep - 1] = self.cascade_dict
        print(f"Stored result for trial {self._itrial} and step {self._istep}.") if self.verbose else None

    def _export_results(self):
        '''
        Description
        -----------
        Exports stored results to csv file.
        '''
        with open(f'{self.export_dir}results.txt', 'w') as file:
            for trial in np.arange(self.n_trials):
                for step in np.arange(self.n_steps):
                    # print(f"\nExporting result for trial {trial} and step {step}.")
                    json.dump(self.results[trial][step], file)
                    file.write('\n')


if __name__ == "__main__":

    ### EXAMPLE USAGE ###
    simulation = Degree_Cascade(
        n_steps=1000, 
        n_trials=1, 
        n_nodes=100,  
        n_edges=10, 
        n_failures = 1,
        verbose=False, 
        visualize=False,
        export_dir='exports/'
    )

    # # Visualize the network at t = 0
    # simulation._visualize_network()
    
    simulation.run()
