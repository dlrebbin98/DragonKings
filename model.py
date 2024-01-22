import random

import numpy as np
import scipy.sparse as sp


class Population:
    
    '''
    A population of agents.
    '''
    
    def __init__(self, n_nodes):
        '''
        Initializes a network with `n_nodes` nodes and `n_edges` edges.
        '''
        self.n_nodes = n_nodes
        self.nodes = np.arange(n_nodes)
        
        self.edges = None


    def set_edges(self, n_edges, verbose=False):
        '''
        Sets `n_edges` edges between random node pairs.
        '''
        # TODO: Add (preferential) probability options
        i = np.random.randint(0, self.n_nodes, size=n_edges)
        j = np.random.randint(0, self.n_nodes, size=n_edges)
        self.edges = np.vstack((i, j)).T
        
        if verbose:
            print('Edges set:')
            print(self.edges)


    def get_state(self) -> np.ndarray:
        '''
        Returns the current state of the network.
        '''
        return self.edges


class Simulation(Population):
    
    '''
    Failure-based resource allocation simulation by Lin et al (2018).
    '''
    
    def __init__(self, n_nodes, n_edges):
        '''
        Initializes a network with `n_nodes` nodes and `n_edges` edges.
        '''
        super().__init__(n_nodes)

        # TODO: Make edges a sparse matrix
        self.set_edges(n_edges=n_edges, verbose=True)
        
        self.node_status = np.ones(n_nodes) # 0 = failure, 1 = weak, 2 = strong; initialize all as weak
        self.timestep = 0


    def iterate(self, tot_timesteps=100, mechanism='IN', epsilon=0.5):
        '''
        Executes 1 timestep of the simulation.
        '''
        # TODO: END FUNCTION IF T = T + 1

        self.tot_timesteps = tot_timesteps
        
        # 1. Degradation:   every timestep, select a random node and decrease strength by 1:
        #    if strength = 1:    node fails; repeat step 1. with t = t + 1
        #    elif strength = 2:    node becomes weak; continue to step 2.
        self.degrade()
         
        # 2. Cascade:   apply IN or CC failure-spreading mechanism, failed nodes remain failed during cascade
        #    if IN:   strong nodes cannot fail
        #    if CC:   strong nodes with 2 or more neighbors fail
        #
        # Repeat step 2. until no more failures occur 
        self.cascade(mechanism)
        
        # 3. Repair: all failed nodes become unfailed (weak remains weak, strong remains strong)
        self.repair()

        # 4. Reinforcement:   every weak node that was repaired in step 3. has probability `epsilon`` to become strong
        self.reinforce(epsilon)
        
        # Return to step 1. with t = t + 1

    
    def degrade(self):
        '''
        Degrades the network until a node fails. 
        
        At each timestep, randomly select a node 
        and decrease its strength by 1:

            If strength == 1, t = t + 1 and repeat.
            
            If strength == 0, break.
        '''
        self.original_node_status = self.node_status.copy()
        while True:
            # select a random node and decrease strength by 1:
            node = random.choice(self.nodes)
            self.node_status[node] -= 1

            status = self.node_status[node]
            if status == 0:
                self.failed_node = node
                print('Node {} failed during timestep {}.'.format(node, self.timestep + 1))
                break
            
            self.timestep += 1
            print('Node {} became weak at timestep {}.'.format(node, self.timestep))
        
        print('Degrading finished.')
    

    def cascade(self, mechanism):
        if mechanism == 'IN':
            self.in_cascade()
        elif mechanism == 'CC':
            self.cc_cascade()
    

    def in_cascade(self):
        '''
        Applies the IN failure-spreading mechanism.
        
        Strong nodes never fail.
        '''
        print('Finding failed edges...')
        while True:
            self.failed_edges = np.array([edge for edge in self.edges if self.failed_node in edge])
            print('Failed edges:')
            print(self.failed_edges)
            
            values, counts = np.unique(self.failed_edges, return_counts=True)        
            failed_nodes = values[(counts > 1) & (self.node_status[values] == 1)]
            print('Failed nodes:')
            print(failed_nodes)

            if failed_nodes.size > 0:
                print('Node {} failed during timestep {}.'.format(failed_nodes[0], self.timestep + 1))
                self.node_status[failed_nodes] = 0
                print('repeating cascade...')
            
            else:
                print('No more failures.')
                break
                

    def cc_cascade(self):
        '''
        Applies the CC failure-spreading mechanism.
        
        Strong nodes with 2 or more neighbors that failed will also fail.
        '''
        pass
    

    def repair(self):
        '''
        Repairs all failed nodes.
        '''
        print('Repairing failed nodes...')
        self.node_status = self.original_node_status

    
    def reinforce(self, epsilon):
        '''
        Applies the reinforcement mechanism.
        '''
        print('Reinforcing weak nodes...')
        weak_nodes = np.where(self.node_status == 1)[0]
        for node in weak_nodes:
            if np.random.rand() < epsilon:
                self.node_status[node] = 2
                print('Node {} became strong.'.format(node))
            else:
                print('Node {} remained weak.'.format(node))


if __name__ == "__main__":

    example_simulation = Simulation(n_nodes=10, n_edges=50)
    example_simulation.iterate(tot_timesteps=10, mechanism='IN', epsilon=0.5)
