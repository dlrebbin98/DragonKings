'''
Module for network related classes and functions.
'''
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx


class NetworkModifier(ABC):
    @abstractmethod
    def increase_strength(self, population:nx.Graph, by):
        pass

class NetworkModifierTime(NetworkModifier):
    @abstractmethod
    def increase_time(self, by):
        pass


class Degrade(NetworkModifier):
    def increase_strength(self, population:nx.Graph, by):
        '''
        Randomly select a node and increase its strength by `by`.
        '''
        node = np.random.choice(population.nodes)
        population.nodes[node]['strength'] += by
        

    def increase_time(self, by):
        self.population.time += by

    def degrade(self):
        '''
        Degrades the network until a node fails. 
        
        At each timestep, randomly select a node 
        and decrease its strength by 1:

            If strength == 1, t = t + 1 and repeat.
            
            If strength == 0, break.
        '''
        # select a random node and decrease strength by 1:
        node = np.random.choice(self.population.nodes)
        self.increase_strength(node, -1)
        self.increase_time(1)
        # print('Node:', node, 'Strength:', self.population.nodes[node]['strength'])

        # if strength == 1, t = t + 1 and repeat.
        if self.population.nodes[node]['strength'] == 1:
            self.degrade()

        # if strength == 0, break.
        else:
            return
        

if __name__ == '__main__':

    # Generate network
    n_nodes = 10_000
    pr_edge = 0.05
    network = nx.fast_gnp_random_graph(n=n_nodes, p=pr_edge)

    # Initialize status of nodes (0 = failed, 1 = weak, 2 = strong)
    node_status = np.ones(n_nodes, dtype=int)
    nx.set_node_attributes(network, node_status, 'strength')

    # Initialize time
    time = 0

    # 
    print('------------------')