import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class NodeNetworkSimulator:

    '''
    Class to simulate the failure of nodes in a network.

    TODO: Split this class into two classes: one for the network
    and one for the simulation.
    '''

    def __init__(self, n_nodes, pr_edge, epsilon=0.2):
        '''
        Description
        -----------
        Initialize the population.

        Parameters
        ----------
        `n_nodes` : int
            The number of nodes in the network.
        `pr_edge` : float
            The probability that two nodes will be connected.
        `epsilon` : float
            The probability that a weak node will be repaired as strong.
        '''
        self.number_of_nodes = n_nodes
        self.pr_edge = pr_edge
        self.network = self.initialize_network()
        self.current_step = 0
        self.epsilon = epsilon


    def initialize_network(self):
        '''
        Initializes a network with random edges and assigns
        a status of 1 to each node.
        
        TODO: Add a parameter to allow the user to specify
        the number of nodes or probability.
        '''
        G = nx.gnp_random_graph(self.number_of_nodes, self.pr_edge)
        nx.set_node_attributes(G, 1, 'status')
        return G


    def random_node(self):
        '''
        Returns a random node from the network.
        '''
        return np.random.choice(self.network.nodes)


    def update_status(self, node, by):
        '''
        Description
        -----------
        Update a node's status.

        Parameters
        ----------
        `node` : int
            The node to update.
        `by` : int
            The amount to update the node's status by.
            A negative value will decrease the node's status.
            A positive value will increase the node's status.
        '''
        self.network.nodes[node]['status'] += by
        failed = self.network.nodes[node]['status'] == 0

        # # show the network
        # self.visualize_network()

        return failed


    def process_neighbors(self):
        '''
        Check the status of each neighbor of a failed node.
        If the neighbor is weak, it fails.
        '''
        # TODO: Refactor to keep track of failed nodes and only process those
        changed = False
        for node in self.network.nodes:
            if self.network.nodes[node]['status'] == 0:
                for neighbor in self.network.neighbors(node):
                    if self.network.nodes[neighbor]['status'] == 1:
                        self.network.nodes[neighbor]['status'] = 0
                        changed = True
        
        # # show the network
        # self.visualize_network()
        
        return changed


    def repair_nodes(self):
        '''
        Repair all failed nodes.
        
        TODO: Refactor to include CC version
        '''
        for node in self.network.nodes:
            self.network.nodes[node]['status'] = 1 if np.random.rand() > self.epsilon else 2


    def _get_failure_size(self):
        '''
        Returns the proportion of nodes with status = 0.
        '''
        data = self.network.nodes.data()
        state = [node[1]['status'] for node in data]
        rel_size = 1 - (np.count_nonzero(state) / len(state))
        return rel_size


    def _visualize_network(self):
        '''
        Visualize the network with yellow nodes representing
        weak nodes and red nodes representing strong nodes.
        '''
        # TODO: Refactor this method to be more efficient and readable
        color_map = ['yellow' if self.network.nodes[node]['status'] == 1 else ('red' if self.network.nodes[node]['status'] == 0 else 'green') for node in self.network.nodes]
        nx.draw(self.network, node_color=color_map)
        plt.title(f"Time Step: {self.current_step}")
        # plt.show()
        plt.savefig(f"images/{self.current_step}.png")


    def simulate(self, steps):
        
        failure_sizes = []

        for _ in range(steps):
            
            # # show the network
            # self.visualize_network()
            
            # print(f"Time Step: {self.current_step}, n_nodes: {self.number_of_nodes}, n_edges: {self.network.number_of_edges()}, n_weak: {len([node for node in self.network.nodes if self.network.nodes[node]['status'] == 1])}, n_strong: {len([node for node in self.network.nodes if self.network.nodes[node]['status'] == 2])}", end='\r')

            # update the status of a random node
            # TODO: Refactor this dirty solution:
            node = self.random_node()
            failed = self.update_status(node, -1)  # returns True if updated node failed
            if failed:
                while self.process_neighbors():
                    pass
                
                rel_size = self._get_failure_size()
                failure_sizes.append(rel_size)
                print(f'Relative failure size: {rel_size}               ', end='\r')
                self.repair_nodes()

            self.current_step += 1

        return failure_sizes
            
# sim = NodeNetworkSimulator(n_nodes=20_000)
# sim.simulate(steps=10_000)

# # Usage
# def run_multiple_sims():
#     for n_nodes in [10, 100, 1_000, 10_000]:
#         for episolon in np.linspace(0, 0.1, 11):
simulation = NodeNetworkSimulator(n_nodes=2000, pr_edge=0.1, epsilon=0.2)
simulation.simulate(100)

# print(f'Average relative failure size: {failure_sizes} for episolon = {simulation.epsilon}')

            # # save results to file
            # with open(f'size_{n_nodes}.txt', 'a') as f:
            #     f.write(f'{simulation.epsilon},{failure_sizes}\n')

# run_multiple_sims()