"""
Citation Graphs
Algorithmic Thinking (Part 1)
Cliff Nelson
September 19, 2018
"""

###################################
# Import required packages

import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import random

###################################
# Helper functions for computing degree distributions

def compute_in_degrees(digraph):
    """
    Takes directed graph represented as dictionary and computes the in-degrees for each node
    Returns dict w/ same keys, values that are number of edges w/ head matching node
    """
    in_degree_dict = {}
    for key in digraph.keys():
        in_degree_dict.update({key: 0})
    for value_set in digraph.values():
        for value in value_set:
            in_degree_dict[value] += 1
    return in_degree_dict

def in_degree_distribution(digraph):
    """
    Takes a dict digraph. Computes unnormalized dist of in-degrees of the graph.
    Returns dict with keys corresponding to in-degrees of nodes in the graph.
    Value for each in-degree is number of nodes with that in-degree. In-degrees wit no nodes are not included.
    """
    in_degree_dict = compute_in_degrees(digraph)
    degree_dist_dict = {}
    for value in in_degree_dict.values():
        degree_dist_dict.update({value: 0})
    for value in in_degree_dict.values():
        degree_dist_dict[value] += 1
    return degree_dist_dict

def normalize_degree_distribution(deg_distribution):
    """
    Takes a degree distribution formatted as dictionary (e.g. output of in_degree_distribution)
    Returns dictionary where keys are number of nodes, values are normalized distribution values
    """
    total_values = float(sum(deg_distribution.values()))
    normalized_distribution = {}
    for key in deg_distribution.keys():
        normalized_distribution.update({key : deg_distribution[key] / total_values})
    return normalized_distribution

def random_digraph(num_nodes, p):
    """
    Returns directed graph as dictionary with num_nodes nodes where p is the probability that a given ordered
    pair of nodes has an edge
    """
    nodes = range(num_nodes)
    rand_digraph = {}
    for node in nodes:
        rand_digraph.update({node: set([])})
    for key in rand_digraph.keys():
        for node in nodes:
            if key != node and random.random() <= p:
                rand_digraph[key].add(node)
    return rand_digraph

def make_complete_graph(num_nodes):
    """
    Takes number of nodes
    Returns dictionary representation of complete directed graph with specified number of nodes
    """
    output_dict = {}
    if num_nodes <= 0:
        return output_dict
    for num in range(num_nodes):
        output_dict.update({num: set(list(filter(lambda x: x != num, range(num_nodes))))})
    return output_dict

def algo_dpa_graph(n, m):
    """
    Iteratively generates synthetic directed graph given n (final number of nodes) and m (number of existing nodes 
    to which each new node is connected). Returns synthetic directed graph.
    """
    
    # Create complete directed graph on m nodes
    digraph = make_complete_graph(m)
    
    # add n - m nodes, where each new node connects to m random existing nodes (eliminate parallel edges)
    while len(digraph) < n:
        new_node_key = len(digraph)
        new_node_values = set([])
        for dummy in range(m):
            new_node_values.add(random.choice(list(digraph.keys())))
        digraph.update({new_node_key: new_node_values})
    return digraph

###################################
# Load citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL for a text representation of the graph
    Returns a dictionary that models a graph
    """
    graph_file = urllib.request.urlopen(graph_url)
    graph_text = str(graph_file.read())
    graph_lines = graph_text.split('\\r\\n')
    graph_lines = graph_lines[ : -1]
    graph_lines[0] = graph_lines[0][2:]
    
    print("Loaded graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)

###################################
# Question 1

# Compute in-degree distribution
cit_graph_deg_distribution = in_degree_distribution(citation_graph)

# Normalize distribution
cit_graph_normalized_distribution = normalize_degree_distribution(cit_graph_deg_distribution)

# Create figure with appropriate axis labels
fig = plt.figure('Normalized Degree Distribution - Sample')
plt.title("Normalized Citation Frequency - Sample")
plt.xlabel('Number of Citations')
plt.ylabel('Frequency')

# Add plot data and make plot
x = cit_graph_normalized_distribution.keys()
y = cit_graph_normalized_distribution.values()
plt.plot(x, y, 'bo', markersize=2)

# Make log/log scale and show
plt.xscale("log")
plt.yscale("log")
plt.show()

###################################
# Question 2

# Create random directed graph with 1,000 nodes, 5% chance of edge between any two given nodes
rand_graph = random_digraph(1000, 0.05)

# Compute normalized in-degree distribution
rand_graph_deg_distr = in_degree_distribution(rand_graph)
rand_graph_norm_deg_distr = normalize_degree_distribution(rand_graph_deg_distr)

# Create figure with appropriate axis labels
fig = plt.figure('Normalized Degree Distribution - Random')  # an empty figure with no axes
plt.title("Normalized Citation Frequency - Random")
plt.xlabel('Number of Citations')
plt.ylabel('Frequency')

# Add plot data and make plot
xrand = rand_graph_norm_deg_distr.keys()
yrand = rand_graph_norm_deg_distr.values()
plt.plot(xrand, yrand, 'bo', markersize=2)

# Make log/log scale and show
plt.xscale("log")
plt.yscale("log")
plt.show()

###################################
# Questions 3 & 4

# Set n to number of nodes in graph from Q1
n = len(citation_graph)

# Set m based on average in degrees for graph from Q1
total_citations = sum([len(citation_graph[key]) for key in list(citation_graph.keys())])
m = int(total_citations / float(n))

# Create graph, compute in-degree distribution, and normalize
generated_graph = algo_dpa_graph(n, m)
gen_graph_deg_distribution = in_degree_distribution(generated_graph)
gen_graph_normalized_distribution = normalize_degree_distribution(gen_graph_deg_distribution)

# Create figure with appropriate axis labels
fig = plt.figure('Normalized Degree Distribution - Generated')
plt.title("Normalized Citation Frequency - Generated")
plt.xlabel('Number of Citations')
plt.ylabel('Frequency')

# Add plot data and make plot
xgen = gen_graph_normalized_distribution.keys()
ygen = gen_graph_normalized_distribution.values()
plt.plot(xgen, ygen, 'bo', markersize=2)
plt.plot(x, y, 'go', markersize=2)
plt.legend(['Generated', 'Sample'])

# Make log/log scale and show
plt.xscale("log")
plt.yscale("log")
plt.show()

###################################
# Question 5

# No code, question only