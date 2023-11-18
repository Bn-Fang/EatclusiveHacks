# Import necessary libraries
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# Load the iris dataset
iris = load_iris()
X = iris.data[:, :2]  # we only take the first two features for visualization.

# Create a KMeans instance and fit the data
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# Predict the cluster labels
labels = kmeans.predict(X)

# Plot the data points with different colors for different clusters
plt.scatter(X[:, 0], X[:, 1], c=labels)

# Plot the cluster centers
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
plt.show()