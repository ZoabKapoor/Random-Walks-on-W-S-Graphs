from __future__ import division
import random
import networkx
import math

class Point:
    def __init__(self, x, y):
        # x value corresponds to f(t * beta^{alpha})
        self.x = x
        # y value corresponds to s(t)/sqrt(t)
        self.y = y
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

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

def generate_runs(N, t, reps, betas):
    """Creates large W-S graphs with varying rewiring probability, averages
    reps random walks for t timesteps in these graphs, returns list of Run objects. 
    
    Parameters: 
        N - number of nodes in the W-S graph
        reps - number of times to repeat each random walk
        t - number of timesteps to run the random walks for
        betas - list of rewiring probabilities to create W-S graphs with"""
    
    NUM_NEIGHBORS = 2
    runs = []
    
    for beta in betas:
        graph = networkx.watts_strogatz_graph(N, NUM_NEIGHBORS, beta)
        list_of_s = [simulate_random_walk(graph,t) for x in range(reps)]
        s_avg = map(mean, zip(*list_of_s))
        runs.append(Run(beta,s_avg))

    return runs

def transform(L, alpha):
    """Transforms a list of Run objects into 2 plot ready lists of [s(t)/sqrt(t)] and [t * beta^{alpha}]
    to be plotted.

    Parameters:
        L - the list of runs to transform
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