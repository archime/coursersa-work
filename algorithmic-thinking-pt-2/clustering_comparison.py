"""
Application #3: Comparison of Clustering Algorithms
Algorithmic Thinking (Part 2)
Cliff Nelson
October 7, 2018
"""

import alg_cluster
import alg_project3_viz as viz_tools
import clustering
import math
import matplotlib.pyplot as plt
import random
import time

# Data table URLs

DATA_3108_URL = viz_tools.DATA_3108_URL
DATA_896_URL = viz_tools.DATA_896_URL
DATA_290_URL = viz_tools.DATA_290_URL
DATA_111_URL = viz_tools.DATA_111_URL

######################################################
# Question 1

def gen_random_clusters(num_clusters):
    cluster_list = [alg_cluster.Cluster(set([]), random.random(), random.random(), 0, 0)
                    for dummy in range(num_clusters)]
    return cluster_list

# Time slow_closest_pair vs. fast_closest_pair
input_size = []
slow_closest_pair_times = []
fast_closest_pair_times = []

def plot_q1():
    for num in range(2, 201):

        input_size.append(num)

        # Test slow_closest_pair_time
        random_cluster_list = gen_random_clusters(num)
        start_time = time.process_time()
        clustering.slow_closest_pair(random_cluster_list)
        end_time = time.process_time()
        slow_closest_pair_times.append(end_time - start_time)

        #Test fast_closest_pair_time
        random_cluster_list = gen_random_clusters(num)
        start_time = time.process_time()
        clustering.fast_closest_pair(random_cluster_list)
        end_time = time.process_time()
        fast_closest_pair_times.append(end_time - start_time)


    # Plot results of timing
    fig = plt.figure('Efficiency of fast_closest_pair vs. slow_closest_pair (Desktop Python)')
    plt.title('Efficiency of fast_closest_pair vs. slow_closest_pair (Desktop Python)')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Running Time')

    x1 = input_size
    y1 = slow_closest_pair_times

    x2 = input_size
    y2 = fast_closest_pair_times

    plt.plot(x1, y1, '-bo', markersize=1, label='slow_closest_pair')
    plt.plot(x2, y2, '-go', markersize=1, label='fast_closest_pair')

    plt.legend(loc='best')

    plt.show()

#plot_q1()

######################################################
# Question 2

#viz_tools.visualize_data(15, DATA_3108_URL, 'hierarchical_clustering', True)

######################################################
# Question 3

#viz_tools.visualize_data((15, 5), DATA_3108_URL, 'kmeans_clustering', True)

######################################################
# Question 4

"""
k-means clustering is faster

Hierarchical clustering: If n is number of input clusters and i is number of
clusters in output, the function makes n-i calls to fast_closest_pair. Since
fast_closes_pair is running time O(n * log2(n)), running time for hierarchical
clustering is O(n**2 * log(n))

K-means clustering: Running time is O(n), so much faster than hierarchical
clustering
"""

######################################################
# Question 5

#viz_tools.visualize_data(9, DATA_111_URL, 'hierarchical_clustering', True)

######################################################
# Question 6

#viz_tools.visualize_data((9, 5), DATA_111_URL, 'kmeans_clustering', True)

######################################################
# Question 7

def compute_distortion(cluster_list, data_table):
    """
    Computes distortion of list of clusters, where data_table is the
    original data input to compute cluster_list
    """
    return sum([cluster.cluster_error(data_table) for cluster in cluster_list])

# Test function

def test_compute_distortion():
    # Load data
    table290 = viz_tools.load_data_table(DATA_290_URL)
    
    # Formate data as Clusters
    singleton_list = []
    for line in table290:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    # Note: K-means tested first b/c clustering.hierarchical_clustering
    # mutates list of clusters

    # Test 2: Expect 2.323×10^11
    kmeans_clusters = clustering.kmeans_clustering(singleton_list, 16, 5)
    k_distortion = compute_distortion(kmeans_clusters, table290)
    print("K-means Distortion: {}".format(k_distortion))

    # Test 1: Expect 2.575×10^11
    hierarchical_clusters = clustering.hierarchical_clustering(singleton_list, 16)
    h_distortion = compute_distortion(hierarchical_clusters, table290)
    print("Hierarchical Distortion: {}".format(h_distortion))

#test_compute_distortion()

def compute_q5_q6():
    # Load data
    table111 = viz_tools.load_data_table(DATA_111_URL)
    
    # Formate data as Clusters
    singleton_list = []
    for line in table111:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]),
                                                  line[1],
                                                  line[2],
                                                  line[3],
                                                  line[4]))
    
    # Note: K-means tested first b/c clustering.hierarchical_clustering
    # mutates list of clusters

    # K-means
    kmeans_clusters = clustering.kmeans_clustering(singleton_list, 9, 5)
    k_distortion = compute_distortion(kmeans_clusters, table111)
    print("K-means Distortion: {}".format(k_distortion))

    # Hierarchical
    hierarchical_clusters = clustering.hierarchical_clustering(singleton_list, 9)
    h_distortion = compute_distortion(hierarchical_clusters, table111)
    print("Hierarchical Distortion: {}".format(h_distortion))

# compute_q5_q6()
# K-means: 271254226924.20047
# Hierarchical: 175163886915.83047

######################################################
# Question 8

"""
Hierarchical clustering has lower distortion than k-means clustering
in this example.

Hierarchical clustering resulted in three clusters on the west coast,
approximately at San Francisco, LA/San Diego, and Seattle.

K-means clustering resulted in three clusters on the west coast,
approximately at Los Angeles, San Diego, and between San Francisco
and Seattle.

K-means clustering has higher distortion because of centers that are
far away from large population centers, e.g. the center between SF and
Seattle.

K-means clustering initializes centers based on highest population, so
the initial clusters include high population counties in southern California
but none in northern California the Pacific Northwest
"""

######################################################
# Question 9

"""
Hierarchical clustering requires less human supervision to produce clusters
with relatively low distortion.
"""

######################################################
# Question 10

def q10(plot_key):
    # Load data
    table111 = viz_tools.load_data_table(DATA_111_URL)
    table290 = viz_tools.load_data_table(DATA_290_URL)
    table896 = viz_tools.load_data_table(DATA_896_URL)
    
    # Create cluster function
    create_cluster = lambda line: alg_cluster.Cluster(set([line[0]]),
                                                      line[1], line[2],
                                                      line[3], line[4])
    
    # Formate data as Clusters
    klist111 = [create_cluster(line) for line in table111]
    klist290 = [create_cluster(line) for line in table290]
    klist896 = [create_cluster(line) for line in table896]
    hlist111 = [create_cluster(line) for line in table111]
    hlist290 = [create_cluster(line) for line in table290]
    hlist896 = [create_cluster(line) for line in table896]
    
    # Initialize distortion lists
    distortion111k, distortion290k, distortion896k = [], [], []
    distortion111h, distortion290h, distortion896h = [], [], []

    # Calculate distortion lists
    for num in range(20, 5, -1):
        if plot_key == 111:
            kmeans_cluster111 = clustering.kmeans_clustering(klist111, num, 5)
            h_cluster111 = clustering.hierarchical_clustering(hlist111, num)
            distortion111k.append(compute_distortion(kmeans_cluster111, table111))
            distortion111h.append(compute_distortion(h_cluster111, table111))
        elif plot_key == 290:
            kmeans_cluster290 = clustering.kmeans_clustering(klist290, num, 5)
            h_cluster290 = clustering.hierarchical_clustering(hlist290, num)
            distortion290k.append(compute_distortion(kmeans_cluster290, table290))
            distortion290h.append(compute_distortion(h_cluster290, table290))
        elif plot_key == 896:
            kmeans_cluster896 = clustering.kmeans_clustering(klist896, num, 5)
            h_cluster896 = clustering.hierarchical_clustering(hlist896, num)
            distortion896k.append(compute_distortion(kmeans_cluster896, table896))
            distortion896h.append(compute_distortion(h_cluster896, table896))

    # Plot results
    fig = plt.figure('Distortion for Different Clustering Methods')
    plt.title('Distortion for Different Clustering Methods: {} Points'.format(plot_key))
    plt.xlabel('Number of Clusters')
    plt.ylabel('Distortion')

    x = list(range(20, 5, -1))

    if plot_key == 111:
        y1, y4 = distortion111k, distortion111h
        plt.plot(x, y1, '-bo', markersize=1, label='K-means (111)')
        plt.plot(x, y4, '-co', markersize=1, label='Hierarchical (111)')
    elif plot_key == 290:
        y2, y5 = distortion290k, distortion290h
        plt.plot(x, y2, '-go', markersize=1, label='K-means (290)')
        plt.plot(x, y5, '-mo', markersize=1, label='Hierarchical (290)')
    elif plot_key == 896:
        y3, y6 = distortion896k, distortion896h
        plt.plot(x, y3, '-ro', markersize=1, label='K-means (896)')
        plt.plot(x, y6, '-yo', markersize=1, label='Hierarchical (896)')

    plt.legend(loc='best')

    plt.show()

#q10(111)
#q10(290)
#q10(896)

######################################################
# Question 11

"""
For the 111 county data set, hierarchical clustering has the least distortion.
For the other data sets, neither method is consistently the least distortion.
"""
