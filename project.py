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


def simulate_random_walk(g, t, reps, beta):
    """simulates a random walk on graph g for t steps reps times. Returns a list of Points."""
    # list = []
    # for rep in range(reps):
    visited = set()
    pos = random.choice(g.nodes())
    visited.add(pos)
    for step in range(t):
        neighbors = g.neighbors(pos)
        next = random.choice(neighbors)
        pos = next
        visited.add(pos)
    print visited
    return visited