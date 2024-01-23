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
        
        self.failed_edges = None
        self.failed_node = None


    def iterate(self, tot_timesteps=100, mechanism='IN', epsilon=0.5):
        '''
        Executes 1 timestep of the simulation.
        '''
        
        self.tot_timesteps = tot_timesteps
        
        while self.timestep < self.tot_timesteps:
            # 1. Degradation:   every timestep, select a random node and decrease strength by 1:
            #    if strength = 1:    node fails; repeat step 1. with t = t + 1
            #    elif strength = 2:    node becomes weak; continue to step 2.
            self.degrade()
            
            # 2. Cascade:   apply IN or CC failure-spreading mechanism, failed nodes remain failed during cascade
            #    if IN:   strong nodes cannot fail
            #    if CC:   strong nodes with 2 or more neighbors fail
            if self.failed_node:     
                self.cascade(mechanism)
                
                # 3. Repair: all failed nodes become unfailed (weak remains weak, strong remains strong)
                self.repair()

                # 4. Reinforcement:   every weak node that was repaired in step 3. has probability `epsilon`` to become strong
                self.reinforce(epsilon)
            

    
    def degrade(self):
        '''
        Degrades the network until a node fails. 
        
        At each timestep, randomly select a node 
        and decrease its strength by 1:

            If strength == 1, t = t + 1 and repeat.
            
            If strength == 0, break.
        '''
        # select a random node and decrease strength by 1:
        node = random.choice(self.nodes)
        self.node_status[node] -= 1
        self.original_node_status = self.node_status.copy()

        status = self.node_status[node]
        
        if status == 1:
            print('Node {} became weak at timestep {}.'.format(node, self.timestep))
            return
        
        self.failed_node = node
        self.timestep += 1
        print('Node {} failed during timestep {}.'.format(node, self.timestep))
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
            print('Found {} failed edges.'.format(self.failed_edges.shape[0]))
            # print('Failed edges:')
            # print(self.failed_edges)
            
            values, counts = np.unique(self.failed_edges, return_counts=True)        
            failed_nodes = values[(counts > 1) & (self.node_status[values] == 1)]
            print('Found {} failed nodes.'.format(failed_nodes.size))
            # print('Failed nodes:')
            # print(failed_nodes)

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
        self.failed_nodes = np.where(self.node_status != 0)[0]
        print('Found {} failed nodes.'.format(self.failed_nodes.size))
        print('Failed nodes:')
        print(self.failed_nodes)

        print('Repaired nodes:')
        print(self.failed_nodes)

        # TODO: FIX THIS SO THAT IT'S NOT STATIC
        print('Reverting failed nodes to original status...')
        print('Original node status:')
        print(self.original_node_status[self.failed_nodes])
        self.nodes[self.failed_nodes] = self.original_node_status[self.failed_nodes]

    
    def reinforce(self, epsilon):
        '''
        Applies the reinforcement mechanism.
        '''
        print('Reinforcing repaired weak nodes...')
        
        weak_nodes = np.where(self.node_status[self.failed_nodes] == 1)[0]
        for node in weak_nodes:
            if np.random.rand() < epsilon:
                self.node_status[self.failed_nodes[node]] = 2
                print('Node {} became strong.'.format(self.failed_nodes[node]))
            else:
                print('Node {} remained weak.'.format(self.failed_nodes[node]))
        print('Reinforcement finished.')
        self.timestep += 1


if __name__ == "__main__":

    example_simulation = Simulation(n_nodes=10, n_edges=50)
    example_simulation.iterate(tot_timesteps=10, mechanism='IN', epsilon=0.6)
