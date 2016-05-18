from __future__ import division
import random
import networkx
import math

class Run:
    """Stores the average (s(t),t) and beta for a run of the
    simulation."""

    def __init__(self, beta, s):
        self.beta = beta
        self.s = s

    def __repr__(self):
        return "beta is: " + str(self.beta) + " and array of s(t)'s indexed by t is: " + str(self.s)


def mean(L):
    return sum(L)/len(L)

def create_WS_graphs(N, betas):
    """Creates list of Newman W-S graphs with N nodes and rewiring probabilities corresponding to the values in betas"""
    NUM_NEIGHBORS = 2

    graphs = []
    for beta in betas:
        graphs.append(networkx.watts_strogatz_graph(N, NUM_NEIGHBORS, beta))
    return graphs

def create_newman_WS_graphs(N, betas):
    NUM_NEIGHBORS = 2

    graphs = []
    for beta in betas:
        graphs.append(networkx.newman_watts_strogatz_graph(N, NUM_NEIGHBORS, beta))
    return graphs

def simulate_random_walk(g, t):
    """simulates a random walk on graph g for t steps. Returns a list containing
    the number of unique nodes of the graph visited, indexed by number of elapsed timesteps."""

    num_uniq_visited = []
    visited = set()
    for step in range(t):
        if step == 0:
            pos = random.choice(g.nodes())
        else:
            neighbors = g.neighbors(pos)
            next = random.choice(neighbors)
            pos = next
        visited.add(pos)
        num_uniq_visited.append(len(visited))
    return num_uniq_visited

def avg_randwalks(graphs, t, reps):
    """Averages reps random walks for t timesteps in the input graphs, returns list of 
    the number of unique nodes of the graph visited in each timestep.
    
    Parameters: 
        graphs - the list of graphs to do the random walks over
        reps - number of times to repeat each random walk
        t - number of timesteps to run each random walk for"""
    
    NUM_NEIGHBORS = 2
    averages = []
    
    for graph in graphs:
        list_of_s = [simulate_random_walk(graph,t) for x in range(reps)]
        s_avg = map(mean, zip(*list_of_s))
        averages.append(s_avg)

    return averages

def transform(L, alpha):
    """Transforms a list of Run objects into 2 plot ready lists of [s(t)/sqrt(t)] and [t * beta^{alpha}]
    to be plotted.

    Parameters:
        L - the list of Runs to transform
        alpha - our guess at the alpha that will collapse the plot into a smooth function"""

    x_vals = []
    y_vals = []
    for run in L:
        beta = run.beta
        s_vals = run.s
        for i in range(1, len(s_vals)):
            x = i * beta**alpha
            y = s_vals[i]/math.sqrt(i)
            x_vals.append(x)
            y_vals.append(y)
    return x_vals, y_vals

## Ideas

# Python pickle? 
# Could save output to files & aggregate by reading in the files

# How to curve fit? Can pyplot do this?
# Fiddle with parameter by hand and see how the plot responds
# Make sure to save plot to file so you don't have to rerun it