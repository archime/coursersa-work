"""
Application #2: Analysis of a Computer Network
Algorithmic Thinking (Part 1)
Cliff Nelson
September 27, 2018
"""


import bfs
import cna_provided as provided
from collections import deque
import math
import matplotlib.pyplot as plt
import random
import time
import unittest
import urllib.request as urlrequest

###################################
# Load source graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def load_graph(graph_url):
    """
    Loads a graph given the URL for a text representation of the graph
    Returns a dictionary that models a graph
    """
    graph_file = urlrequest.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.decode('utf-8').split('\r\n')
    graph_lines = graph_lines[:-1]

    print("Loaded graph with", len(graph_lines), "nodes\n")

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

###################################
# Helper functions

def er_algo(num_nodes, prob):
    """
    Returns graph as dict with specified number of nodes where probability of
    an edge between each pair of nodes is given by prob
    """
    
    # List all possible pairs
    poss_pairs = set()
    for node1 in range(num_nodes):
        for node2 in range(num_nodes):
            if node1 != node2:
                poss_pairs.add(tuple(sorted([node1, node2])))

    # Iterate through poss_pairs and add to set of edges
    edges = set()
    for pair in poss_pairs:
        if random.random() < prob:
            edges.add(pair)

    # Build graph from set of edges
    graph = dict()
    for node in range(num_nodes):
        graph[node] = set()
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])
    return graph

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def make_complete_ugraph(num_nodes):
    """
    Takes number of nodes
    Returns complete undirected graph as dict w/ specified number of nodes
    """
    output_dict = {}
    if num_nodes <= 0:
        return output_dict
    for num in range(num_nodes):
        output_dict.update({num: set(list(filter(lambda x: x != num, range(num_nodes))))})
    return output_dict

def algo_upa_graph(n, m):
    """
    Iteratively generates synthetic ugraph given n (final number of nodes)
    and m (number of existing nodes to which each new node is connected).
    Returns synthetic undirected graph.
    """

    # Create complete directed graph on m nodes
    ugraph = make_complete_ugraph(m)

    # add n - m nodes, where each new node connects to m random existing nodes (eliminate parallel edges)
    while len(ugraph) < n:
        new_node_key = len(ugraph)
        new_node_values = set([])
        for dummy in range(m):
            new_node_values.add(random.choice(list(ugraph.keys())))
        ugraph.update({new_node_key: new_node_values})
        for value in new_node_values:
            ugraph[value].add(new_node_key)
    return ugraph

def random_order(graph):
    """
    Takes graph and returns list of nodes in a random order
    """
    node_list = list(graph.keys())
    random_list = []
    while len(node_list) != 0:
        random_list.append(node_list.pop(random.randrange(0, len(node_list))))
    return random_list

def fast_targeted_order(graph):
    """
    Fast version of provided.targeted_order
    """
    graph_copy = provided.copy_graph(graph)
    degree_sets = dict()
    for k in range(0, len(graph_copy)):
        degree_sets[k] = set()
    for i in range(0, len(graph_copy)):
        d = len(graph_copy[i]) # degree of i
        degree_sets[d].add(i)
    l = []
    for k in range(len(graph_copy) - 1, -1, -1):
        while degree_sets[k] != set():
            node = degree_sets[k].pop()
            for neighbor in graph_copy[node]:
                d = len(graph_copy[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d-1].add(neighbor)
            l.append(node)
            provided.delete_node(graph_copy, node)
    return l

###################################
# Question 1
# We will then compare the resilience of the network to the resilience of ER 
# and UPA graphs of similar size.

# Load provided graph and store number of nodes and edges
provided_graph = load_graph(NETWORK_URL)
num_nodes = len(provided_graph) # 1,239 nodes
num_edges = sum(len(value) for value in provided_graph.values()) / 2 # 3,047 edges

# ER graph where prob of edge is num_edges in provided divided by poss
# prob = 0.003972926209447663
prob = num_edges / nCr(num_nodes, 2)
er_graph = er_algo(num_nodes, prob)
# er_edges = sum(len(value) for value in er_graph.values()) / 2

# UPA graph
upa_graph = algo_upa_graph(1239, 3) # m = 3 --> ~3,700 edges
# upa_edges = sum(len(value) for value in upa_graph.values()) / 2

# Calculate resilience
attack_order_provided = random_order(provided_graph)
attack_order_er = random_order(er_graph)
attack_order_upa = random_order(upa_graph)

provided_resilience = bfs.compute_resilience(provided_graph, attack_order_provided)
er_graph_resilience = bfs.compute_resilience(er_graph, attack_order_er)
upa_graph_resilience = bfs.compute_resilience(upa_graph, attack_order_upa)

# Plots
fig = plt.figure('Network Resilience - Random Attack Order')
plt.title('Network Resilience - Random Attack Order')
plt.xlabel('Number of Nodes Removed')
plt.ylabel('Largest Connected Component')

x1 = range(len(provided_resilience))
y1 = provided_resilience

x2 = range(len(er_graph_resilience))
y2 = er_graph_resilience

x3 = range(len(upa_graph_resilience))
y3 = upa_graph_resilience

plt.plot(x1, y1, '-bo', markersize=1, label='provided')
plt.plot(x2, y2, '-go', markersize=1, label='er_graph, p = 0.004')
plt.plot(x3, y3, '-ro', markersize=1, label='upa_graph, m = 3')

plt.legend(loc='best')

plt.show()

###################################
# Question 2

provided_cc_20pct_removed = provided_resilience[int(len(provided_resilience) * 0.20)]
provided_cc_initial = provided_resilience[0]
provided_pct = provided_cc_20pct_removed / float(provided_cc_initial)

er_cc_20pct_removed = er_graph_resilience[int(len(er_graph_resilience) * 0.20)]
er_cc_initial = er_graph_resilience[0]
er_pct = er_cc_20pct_removed / float(er_cc_initial)

upa_cc_20pct_removed = upa_graph_resilience[int(len(upa_graph_resilience) * 0.20)]
upa_cc_initial = upa_graph_resilience[0]
upa_pct = upa_cc_20pct_removed / float(upa_cc_initial)

print("### RANDOM ###")
print("Provided graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(provided_pct))
print("ER graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(er_pct))
print("UPA graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(upa_pct))

###################################
# Question 3

# Targeted Order: O(n^2)
# Fast Targeted Order: O(n)

input_args = range(10,1000,10)
m = 5
reg_running_times = []
fast_running_times = []

for n in input_args:
    upa_test = algo_upa_graph(n, m)
    
    start_time = time.process_time()
    provided.targeted_order(upa_test)
    end_time = time.process_time()
    reg_running_times.append(end_time - start_time)
    
    start_time = time.process_time()
    fast_targeted_order(upa_test)
    end_time = time.process_time()
    fast_running_times.append(end_time - start_time)

# Plot
fig3 = plt.figure('Running Times')
plt.title('Running Times')
plt.xlabel('Number of Nodes in UPA Graph, m = 5')
plt.ylabel('Seconds')

x = input_args
y1 = reg_running_times
y2 = fast_running_times

plt.plot(x, y1, '-bo', markersize=1, label='targeted_order')
plt.plot(x, y2, '-go', markersize=1, label='fast_targeted_order')

plt.legend(loc='best')

plt.show()

###################################
# Question 4

# Determine attack orders
targeted_attack_order_provided = provided.targeted_order(provided_graph)
targeted_attack_order_er = fast_targeted_order(er_graph)
targeted_attack_order_upa = fast_targeted_order(upa_graph)

# Calculate resilience
targeted_provided_resilience = bfs.compute_resilience(provided_graph, targeted_attack_order_provided)
targeted_er_graph_resilience = bfs.compute_resilience(er_graph, targeted_attack_order_er)
targeted_upa_graph_resilience = bfs.compute_resilience(upa_graph, targeted_attack_order_upa)

# Plots
fig = plt.figure('Network Resilience - Targeted Attack Order')
plt.title('Network Resilience - Targeted Attack Order')
plt.xlabel('Number of Nodes Removed')
plt.ylabel('Largest Connected Component')

x1 = range(len(targeted_provided_resilience))
y1 = targeted_provided_resilience

x2 = range(len(targeted_er_graph_resilience))
y2 = targeted_er_graph_resilience

x3 = range(len(targeted_upa_graph_resilience))
y3 = targeted_upa_graph_resilience

plt.plot(x1, y1, '-bo', markersize=1, label='provided')
plt.plot(x2, y2, '-go', markersize=1, label='er_graph, p = 0.004')
plt.plot(x3, y3, '-ro', markersize=1, label='upa_graph, m = 3')

plt.legend(loc='best')

plt.show()

###################################
# Question 5

targeted_provided_cc_20pct_removed = targeted_provided_resilience[int(len(targeted_provided_resilience) * 0.20)]
targeted_provided_cc_initial = targeted_provided_resilience[0]
targeted_provided_pct = targeted_provided_cc_20pct_removed / float(targeted_provided_cc_initial)

targeted_er_cc_20pct_removed = targeted_er_graph_resilience[int(len(targeted_er_graph_resilience) * 0.20)]
targeted_er_cc_initial = targeted_er_graph_resilience[0]
targeted_er_pct = targeted_er_cc_20pct_removed / float(targeted_er_cc_initial)

targeted_upa_cc_20pct_removed = targeted_upa_graph_resilience[int(len(targeted_upa_graph_resilience) * 0.20)]
targeted_upa_cc_initial = targeted_upa_graph_resilience[0]
targeted_upa_pct = targeted_upa_cc_20pct_removed / float(targeted_upa_cc_initial)

print("### TARGETED ###")
print("Provided graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(targeted_provided_pct))
print("ER graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(targeted_er_pct))
print("UPA graph largest cc is {:0.0%} of orig. after removing 20% of nodes".format(targeted_upa_pct))

###################################
# Define tests

class TestFunctions(unittest.TestCase):
    
    def test_helpers(self):
        self.assertEqual(er_algo(4, 1), {0: {1, 2, 3}, 1: {0, 2, 3}, 2: {0, 1, 3}, 3: {0, 1, 2}})

###################################
# Run tests

if __name__ == '__main__':
    unittest.main()
