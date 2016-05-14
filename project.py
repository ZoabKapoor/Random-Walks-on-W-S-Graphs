from __future__ import division
import random
import networkx

class Point:
    def __init__(self, t, s, beta):
        self.t = t
        self.s = s
        self.beta = beta
    
    def __repr__(self):
        print "Timestep is: " + t
        print "Number of visited nodes is: " + s
        print "Rewiring probabability is: " + beta

def run_the_damn_simulation(N, t, reps, betas):
    """Creates large W-S graphs with varying rewiring probability, simulates reps random walks for t timesteps in these 
    graphs, and plots s(t)/sqrt(t) against 
    t*beta^{alpha} using (t, s(t), beta) tuples. 
    
    Parameters: 
        N - number of nodes in the W-S graph
        reps - number of times to repeat each random walk
        t - number of timesteps to run the random walk for
        betas - list of rewiring probabilities to create W-S graphs with"""
    
    NUM_NEIGHBORS = 2
    points = []
    
    for beta in betas:
        graph = networkx.watts_strogatz_graph(N, NUM_NEIGHBORS, beta)
        # run the simulation & get avg (t,s,beta) points
        points += simulate_random_walk(graph,t,reps,beta)
        
    # graph the thing


def simulate_random_walk(g, t):
    """simulates a random walk on graph g for t steps. Returns a list containing
    the fraction of the graph visited, indexed by number of elapsed timesteps."""

    fraction_visited = []
    visited = set()
    for step in range(t):
        if step == 0:
            pos = random.choice(g.nodes())
        else:
            neighbors = g.neighbors(pos)
            next = random.choice(neighbors)
            pos = next
        visited.add(pos)
        frac = len(visited)/networkx.number_of_nodes(g)
        fraction_visited.append(frac)
    return fraction_visited

## Questions

# 1. How to aggregate the Points over multiple runs on the same graph?

# Use a list where index is timestep and value is fraction covered
# Aggregating before returning means you don't have to store beta while you aggregate 
# Python pickle? 
# Could save output to files & aggregate by reading in the files

# 2. How to curve fit? Can pyplot do this?
# Fiddle with parameter by hand and see how the plot responds
# Make sure to save plot to file so you don't have to rerun it for different alphas

# 3. How to store the points for easiest graphing? List of tuples? List of lists? 
# List of 2-element dumb data structure? 
# Can pass 2 lists into plt.plot
# If you want to be fancy, can do scatterplots that use additional attributes (color, size, shape)
# List of tuples may not be possible