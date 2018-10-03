"""
Project #3: Closest Pairs & Clustering Algorithms
Algorithmic Thinking (Part 2)
Cliff Nelson
October 2, 2018

Student will implement five functions:

[X] slow_closest_pair(cluster_list)
[X] fast_closest_pair(cluster_list)
[X] closest_pair_strip(cluster_list, horiz_center, half_width)
[X] hierarchical_clustering(cluster_list, num_clusters)
[X] kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import alg_cluster
import math
import unittest


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """

    dist, idx1, idx2 = float('Inf'), -1, -1
    for idx_i in range(len(cluster_list)):
        for idx_j in range(len(cluster_list)):
            if idx_i == idx_j:
                pass
            else:
                dist, idx1, idx2 = min((dist, idx1, idx2), pair_distance(cluster_list , idx_i, idx_j))
    return (dist, idx1, idx2)

def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """

    indices_in_strip = [i for i, x in enumerate(cluster_list) if abs(x.horiz_center() - horiz_center) < half_width]
    indices_in_strip.sort(key = lambda idx: cluster_list[idx].vert_center())
    num_clusters = len(indices_in_strip)
    dist, idx_i, idx_j = float('Inf'), -1, -1
    for idx_u in range(0, num_clusters-1):
        for idx_v in range(idx_u+1, min(idx_u+4, num_clusters)):
            dist, idx_i, idx_j = min((dist, idx_i, idx_j),
                                     pair_distance(cluster_list, indices_in_strip[idx_u], indices_in_strip[idx_v]))
    return (dist, idx_i, idx_j)

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """

    cluster_list.sort(key = lambda x: x.horiz_center())

    num_clusters = len(cluster_list)
    if num_clusters <= 3:
        dist, idx_i, idx_j = slow_closest_pair(cluster_list)
    else:
        midpt = int(num_clusters / 2)
        p_left = cluster_list[:midpt]
        p_right = cluster_list[midpt:]
        dist_l, idx_il, idx_jl = fast_closest_pair(p_left)
        dist_r, idx_ir, idx_jr = fast_closest_pair(p_right)
        # Adjust idx_ir, idx_jr to reference cluster_list
        dist_r, idx_ir, idx_jr = dist_r, idx_ir + midpt, idx_jr + midpt
        dist, idx_i, idx_j = min((dist_l, idx_il, idx_jl), (dist_r, idx_ir, idx_jr))
        center_line = 0.5 * (cluster_list[midpt - 1].horiz_center() + cluster_list[midpt].horiz_center())
        dist, idx_i, idx_j = min((dist, idx_i, idx_j), closest_pair_strip(cluster_list, center_line, dist))
    return dist, idx_i, idx_j

######################################################################
# Code for hierarchical clustering

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """

    while len(cluster_list) > num_clusters:
        # Find closest pair
        closest_pair = fast_closest_pair(cluster_list)
        # Remove closest pair from list
        closest2 = cluster_list.pop(closest_pair[2])
        closest1 = cluster_list.pop(closest_pair[1])
        # Merge closest pair into single cluster
        closest1.merge_clusters(closest2)
        # Add merged closest pair as single cluster
        cluster_list.append(closest1)
    return cluster_list

######################################################################
# Code for k-means clustering
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # Copy cluster list and sort by descending total population to get initial centers
    cluster_list_copy = cluster_list[:] # Sliced instead of list.copy() for Python 2 compatibility
    cluster_list_copy.sort(key = lambda x: -x.total_population())
    center_positions = [(cluster_list_copy[idx].horiz_center(),
                         cluster_list_copy[idx].vert_center()) for idx in range(num_clusters)]

    for dummy in range(num_iterations):

        # Initialize list of k empty clusters at center_positions for merging
        center_clusters = [alg_cluster.Cluster(set([]),
                                               position[0],
                                               position[1],
                                               0, 0) for position in center_positions]

        for cluster in cluster_list_copy:
            # Find closest element of center_positions to indexed cluster
            closest_center_idx, closest_dist = None, float('Inf')
            for idx, position in enumerate(center_positions):
                dist = cluster.distance(alg_cluster.Cluster(set([]), position[0], position[1], 0, 0))
                if dist < closest_dist:
                    closest_dist = dist
                    closest_center_idx = idx
            # Closest center replace/merge with cluster
            center_clusters[closest_center_idx].merge_clusters(cluster)

        # Update center_positions
        for idx in range(len(center_positions)):
            center_positions[idx] = (center_clusters[idx].horiz_center(), center_clusters[idx].vert_center())

    return center_clusters

######################################################################
# Code for testing

class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        self.cluster1 = alg_cluster.Cluster(set([]), 0, 0, 1, 0)
        self.cluster2 = alg_cluster.Cluster(set([]), 1, 0, 1, 0)
        self.cluster3 = alg_cluster.Cluster(set([]), 2, 0, 1, 0)
        self.cluster_list1 = [alg_cluster.Cluster(set([]), 0.02, 0.39, 1, 0),
                              alg_cluster.Cluster(set([]), 0.19, 0.75, 1, 0),
                              alg_cluster.Cluster(set([]), 0.35, 0.03, 1, 0),
                              alg_cluster.Cluster(set([]), 0.73, 0.81, 1, 0),
                              alg_cluster.Cluster(set([]), 0.76, 0.88, 1, 0),
                              alg_cluster.Cluster(set([]), 0.78, 0.11, 1, 0)]

    def tearDown(self):
        del self.cluster1
        del self.cluster2
        self.widget = None

    def test_init_cluster(self):
        self.assertNotEqual(self.cluster1, None)
        self.assertEqual(self.cluster1.distance(alg_cluster.Cluster(set([]), 0, 0, 1, 0)), 0.0)

    def test_slow_closest_pair(self):
        self.assertTrue(slow_closest_pair([self.cluster1, self.cluster2]) == (1.0, 0, 1))

    def test_closest_pair_strip(self):
        self.assertTrue(closest_pair_strip([self.cluster1,
                                           self.cluster2,
                                           self.cluster3], 1.5, 1.0) == (1.0, 1, 2))

    def test_fast_closest_pair(self):
        ans = fast_closest_pair(self.cluster_list1)
        self.assertTrue(ans == (0.07615773105863904, 3, 4))

######################################################################
# Run tests

if __name__ == '__main__':
    unittest.main()
