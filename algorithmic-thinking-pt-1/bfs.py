"""
Project #2: Breadth-first search
Algorithmic Thinking (Part 1)
Cliff Nelson
September 23, 2018
"""

import unittest
import cna_provided as provided
from collections import deque


###################################
# Section 1: Breadth-first search

def bfs_visited(ugraph,start_node):
    """
    Takes undirected graph and node start_node
    Returns set with all nodes visited by BFS starting at start_node
    """
    
    queue = deque()
    visited = set([start_node])
    queue.appendleft(start_node)
    while len(queue) != 0:
        current_node = queue.pop()
        for adjacent_node in ugraph[current_node]:
            if adjacent_node not in visited:
                visited.update(set([adjacent_node]))
                queue.appendleft(adjacent_node)
    return visited

###################################
# Section 2: Connected components

def cc_visited(ugraph):
    """
    Takes undirected graph ugraph and returns a list of sets, where each set
    consists of all the nodes (and nothing else) in a connected component,
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.
    """
    
    remaining_nodes = set(list(ugraph.keys()))
    connected_components = []
    while len(remaining_nodes) != 0:
        current_node = remaining_nodes.pop()
        visited_set = bfs_visited(ugraph, current_node)
        connected_components.append(visited_set)
        for node in visited_set:
            remaining_nodes.discard(node)
    return connected_components

def largest_cc_size(ugraph):
    """
    Takes undirected graph ugraph
    Returns integer size of largest connected component
    """
    connected_components = cc_visited(ugraph)
    max_len = 0
    for component in connected_components:
        if len(component) > max_len:
            max_len = len(component)
    return max_len

###################################
# Section 3: Graph resilience

def compute_resilience(ugraph, attack_order):
    """
    Takes undirected graph ugraph and list of nodes attack_order
    For each node in list, removes node and edges from graph and computes size
    of largest connected component for resulting graph
    Returns list whose k + 1th entry is size of largest connected component in
    the graph after removal of the first k nodes in attack_order. First entry
    is the size of the largest connected component in the original graph
    """
    graph_copy = provided.copy_graph(ugraph)
    largest_cc_list = [largest_cc_size(graph_copy)]
    for node in attack_order:
        provided.delete_node(graph_copy, node)
        largest_cc_list.append(largest_cc_size(graph_copy))
    return largest_cc_list

###################################
# Define tests

class TestFunctions(unittest.TestCase):
    
    def test_bfs_visited(self):
        test_ugraph = {0: {1}, 1: {0, 2}, 2: {1}, 3: {}}
        self.assertEqual(bfs_visited(test_ugraph, 0), {0, 1, 2})
        self.assertEqual(bfs_visited(test_ugraph, 3), {3})

    def test_cc_visited(self):
        test_ugraph = {0: {1}, 1: {0, 2}, 2: {1}, 3: {}}
        self.assertEqual(cc_visited(test_ugraph), [{0, 1, 2}, {3}])

    def test_largest_cc_size(self):
        test_ugraph = {0: {1}, 1: {0, 2}, 2: {1}, 3: {}}
        self.assertEqual(largest_cc_size(test_ugraph), 3)
 
    def test_compute_resilience(self):
        test_ugraph = {0: {1}, 1: {0, 2}, 2: {1}, 3: {}}
        test_attack_order = [1, 3]
        self.assertEqual(compute_resilience(test_ugraph, test_attack_order), [3, 1, 1])

###################################
# Run tests

if __name__ == '__main__':
    unittest.main()
