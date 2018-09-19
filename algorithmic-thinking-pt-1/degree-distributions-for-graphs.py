"""
Degree Distributions for Graphs
Algorithmic Thinking (Part 1)
Cliff Nelson
September 18, 2018
"""

# Part 1: Representing directed graphs

EX_GRAPH0 = {0: set([1,2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1,4,5]),
             1: set([2,6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1,4,5]),
             1: set([2,6]),
             2: set([3,7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1,2]),
             9: set([0,3,4,5,6,7])}

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

# Part 2: Computing degree distributions

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