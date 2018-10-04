"""
Application #3: Comparison of Clustering Algorithms
Algorithmic Thinking (Part 2)
Cliff Nelson
October 3, 2018

[X] Q1
[ ] Q2
[ ] Q3
[ ] Q4
[ ] Q5
[ ] Q6
[ ] Q7
[ ] Q8
[ ] Q9
[ ] Q10
[ ] Q11
"""

import alg_cluster
import alg_project_viz as viz_tools
import clustering as cluster_tools
import math
import matplotlib.pyplot as plt
import random
import time


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

for num in range(2, 201):

    input_size.append(num)

    # Test slow_closest_pair_time
    random_cluster_list = gen_random_clusters(num)
    start_time = time.process_time()
    cluster_tools.slow_closest_pair(random_cluster_list)
    end_time = time.process_time()
    slow_closest_pair_times.append(end_time - start_time)

    #Test fast_closest_pair_time
    random_cluster_list = gen_random_clusters(num)
    start_time = time.process_time()
    cluster_tools.fast_closest_pair(random_cluster_list)
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

######################################################
# Question 2
