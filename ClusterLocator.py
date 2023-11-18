# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth
from collections import Counter

# Load your CSV into a DataFrame
csv_path = "VotingSampleData.csv" 
df = pd.read_csv(csv_path)
  
# Assign columns to variables
user_ids = df['userid']
x_values = df['x']
y_values = df['y']
votes = df['vote']

# Create a list of tuples where each tuple is a pair of X,Y
points = np.array(list(zip(x_values, y_values)))

# Estimate bandwidth for mean shift
bandwidth = estimate_bandwidth(points, quantile=0.2, n_samples=500)

# Create Mean Shift Model
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(points)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

df['clusterId'] = labels

# If there are more than 5 clusters, combine the nearest ones
while len(set(labels)) > 5:
    # Calculate pairwise distances of cluster_centers, get the minimum
    dists = np.sqrt(((cluster_centers[:, None, :] - cluster_centers) ** 2).sum(-1))
    np.fill_diagonal(dists, np.inf)
    min_cluster_pair = np.unravel_index(dists.argmin(), dists.shape)

    # Combine the two nearest clusters
    labels[labels == min_cluster_pair[1]] = min_cluster_pair[0]
    cluster_centers = np.delete(cluster_centers, min_cluster_pair[1], axis=0)

# Create scatter plot for visualization
plt.scatter(x_values, y_values, c=labels)
plt.show()

# Create vote dictionary
cluster_vote_dict = {}
for cluster_id in set(labels):
    cluster_votes = votes[labels == cluster_id]
    cluster_vote_dict[cluster_id] = dict(Counter(cluster_votes))

print(cluster_vote_dict)