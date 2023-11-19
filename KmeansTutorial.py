# # Import necessary libraries
# from sklearn.cluster import KMeans
# from sklearn.datasets import load_iris
# import matplotlib.pyplot as plt

# # Load the iris dataset
# iris = load_iris()
# X = iris.data[:, :2]  # we only take the first two features for visualization.

# # Create a KMeans instance and fit the data
# kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# # Predict the cluster labels
# labels = kmeans.predict(X)
# print(labels)

# # Plot the data points with different colors for different clusters
# plt.scatter(X[:, 0], X[:, 1], c=labels)

# # Plot the cluster centers
# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
# plt.show()

import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

# creating dataset with 5 clusters
X, y = make_blobs(
   n_samples=1000, n_features=2,
   centers=5, cluster_std=5,
   shuffle=True, random_state=16
)

# apply kmeans
kmeans = KMeans(
    n_clusters=5, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = kmeans.fit_predict(X)

# visualize
for i in range(5):
    plt.scatter(
        X[y_km == i, 0], X[y_km == i, 1],
        s=50, 
        label=f'cluster {i}'
    )

# plot the centroids
plt.scatter(
    kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
    s=250, marker='*',
    c='red', edgecolor='black',
    label='centroids'
)

plt.legend()
plt.show()