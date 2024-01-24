import networkx as nx
import numpy as np

class Population:
    
    '''
    Class structure of a population of agents in a network.
    '''
    
    def __init__(self, n_nodes:int, n_edges:int=None, pr_edge:float=None):
        '''
        Description
        -----------
        Initializes a random network of nodes given a probability 
        of connection or a specified number of edges.

        Parameters
        ----------
        `n_nodes` : int
            Number of nodes in the network.
        `n_edges` : int (optional)
            Number of edges in the network.
        `pr_edge` : float [0, 1] (optional)
            Probability of an edge between two nodes.
        '''
        # Parse arguments
        self.n_nodes = n_nodes
        self.pr_edge = pr_edge
        self.n_edges = n_edges

        # Initialize network
        self.network = nx.Graph()
        self.nodes = np.arange(n_nodes)
        
        if self.n_edges is not None:
            self.generate_edges_with_n_edge()
        elif self.pr_edge is not None:
            # self.generate_edges_with_pr_edge()
            pass
        else:
            raise ValueError('Either `n_edges` or `pr_edge` must be specified.')
        
        # Add generated nodes and edges to network
        self.network.add_nodes_from(self.nodes)
        self.network.add_edges_from(self.edges)
        

    def generate_edges_with_n_edge(self):
        '''Randomly generates `n_edges` edges between random node pairs.'''
        i = np.random.randint(0, self.n_nodes, size=self.n_edges)
        j = np.random.randint(0, self.n_nodes, size=self.n_edges)
        self.edges = np.vstack((i, j)).T
    

pop = Population(10_000, n_edges=50_000)
print('------------------')
print('Graph:', pop.network)
print('Nodes:', pop.nodes)
print('Network nodes:', pop.network.nodes)
print('Network edges:', pop.network.edges)
print('------------------')
