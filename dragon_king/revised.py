import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class NodeNetworkSimulation:
    def __init__(self, n_nodes):
        self.number_of_nodes = n_nodes
        self.network = self.initialize_network()
        self.current_step = 0

    def initialize_network(self):
        '''
        Initializes a network with random edges and assigns
        a status of 1 to each node.
        
        TODO: Add a parameter to allow the user to specify
        the number of nodes or probability.
        '''
        G = nx.fast_gnp_random_graph(self.number_of_nodes, 0.5)
        nx.set_node_attributes(G, 1, 'status')
        return G

    def random_node(self):
        '''
        Returns a random node from the network.
        '''
        return np.random.choice(self.network.nodes)

    def update_status(self, node, by):
        '''
        Randomly select a node and decrease its status by 1.
        '''
        self.network.nodes[node]['status'] += by
        failed = self.network.nodes[node]['status'] == 0

        # show the network
        self.visualize_network()

        return failed

    def process_neighbors(self):
        '''
        Check the status of each neighbor of a failed node.
        If the neighbor is weak, it fails.
        '''
        changed = False
        for node in self.network.nodes:
            if self.network.nodes[node]['status'] == 0:
                for neighbor in self.network.neighbors(node):
                    if self.network.nodes[neighbor]['status'] == 1:
                        self.networkW.nodes[neighbor]['status'] = 0
                        changed = True
        # show the network
        self.visualize_network()
        return changed

    def repair_nodes(self):
        for node in self.network.nodes:
            self.network.nodes[node]['status'] = 1 if np.random.rand() > 0.2 else 2

    def visualize_network(self):
        '''
        Visualize the network with yellow nodes representing
        weak nodes and red nodes representing strong nodes.
        '''
        # TODO: Refactor this method to be more efficient and readable
        color_map = ['yellow' if self.network.nodes[node]['status'] == 1 else ('red' if self.network.nodes[node]['status'] == 0 else 'green') for node in self.network.nodes]
        nx.draw(self.network, node_color=color_map)
        plt.title(f"Time Step: {self.current_step}")
        plt.show()

    def simulate(self, steps):
        
        for _ in range(steps):
            
            # show the network
            self.visualize_network()

            # update the status of a random node
            node = self.random_node()
            failed = self.update_status(node, -1)  # returns True if updated node failed
            if failed:
                while self.process_neighbors():
                    pass
                self.repair_nodes()

            self.current_step += 1
            

# Usage
simulation = NodeNetworkSimulation(100)
simulation.simulate(10)
