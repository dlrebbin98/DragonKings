import random

import numpy as np


class Network:
    

    def __init__(self, n_nodes, pr_edge=None, n_edges=None):
        
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        
        if pr_edge:
            self.pr_edge = pr_edge
            self.network = self.generate_random_network()
        elif n_edges:
            self.network = self.generate_random_network_w_edge()


    def generate_random_network(self):
        
        network = {}

        # TODO: move to __init__
        for i in range(self.n_nodes):
            network[i] = set()
        
        # TODO: replace with numpy
        for node1 in range(self.n_nodes):
            for node2 in range(self.n_nodes):
                if node1 != node2 and random.random() < self.pr_edge:
                    network[node1].add(node2)
                    network[node2].add(node1)


    def generate_random_network_w_edge(self):
        
        network = {}
        
        for i in range(self.n_nodes):
            network[i] = set()
        
        # TODO: replace with numpy.random.choice
        for _ in range(self.n_edges):
            node1 = random.randint(0, self.n_nodes - 1)
            node2 = random.randint(0, self.n_nodes - 1)
            network[node1].add(node2)
            network[node2].add(node1)
        
        return network


    def _get_adjacency_matrix(self):
        
        matrix = np.zeros((self.n_nodes, self.n_nodes))
        
        for node1 in self.network:
            for node2 in self.network[node1]:
                matrix[node1][node2] = 1
        
        return matrix
    

    def _get_degree_vector(self):
        
        vector = np.zeros(self.n_nodes)
        
        for node in self.network:
            vector[node] = len(self.network[node])
        
        return vector
    


if __name__ == "__main__":

    debug = Network(10, 10)
    print(debug.network)