# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from collections import Counter

import firebase_admin
from firebase_admin import credentials, firestore

def readInData(db):
    users_ = []
    ref = db.collection('users').get()
    for doc in ref:
        users_.append(doc.to_dict())
        
    df = pd.DataFrame(users_)
    print(df)
    
    InactiveUsers = df[df['vote'] == 0]
    active_users = df[df['vote'] != 0]
    cluster_center = df[df['ClusterId'] == 0]
    labels, cluster_centers, num_centers = FindMeans(active_users)
    all_labels, all_cluster_centers, unneeded = FindMeans(df)
    return df, InactiveUsers, active_users, labels, cluster_centers, all_labels, all_cluster_centers, num_centers


def FindMeans(df):  
    x_values = df['x']
    y_values = df['y']
    # Create a list of tuples where each tuple is a pair of X,Y
    points = np.array(list(zip(x_values, y_values)))

    # Estimate bandwidth for mean shift
    bandwidth = estimate_bandwidth(points, quantile=0.2, n_samples=100)

    # Create Mean Shift Model
    ms = MeanShift(bandwidth=.5, bin_seeding=True)
    ms.fit(points)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    
    # If there are more than 5 clusters, combine the nearest ones
    while len(set(labels)) > 5:
        # Calculate pairwise distances of cluster_centers, get the minimum
        dists = np.sqrt(((cluster_centers[:, None, :] - cluster_centers) ** 2).sum(-1))
        np.fill_diagonal(dists, np.inf)
        min_cluster_pair = np.unravel_index(dists.argmin(), dists.shape)

        # Combine the two nearest clusters
        labels[labels == min_cluster_pair[1]] = min_cluster_pair[0]
        cluster_centers = np.delete(cluster_centers, min_cluster_pair[1], axis=0)
    
    num_centers = len(set(labels))
    km = KMeans(n_clusters=num_centers, init=cluster_centers, n_init=1)
    km.fit(points)
    labels = km.labels_
    cluster_centers = km.cluster_centers_
    
    
    if len(set(labels)) < 5:
        for i in range(5 - len(set(labels))):
            cluster_centers = np.append(cluster_centers, [[0,0]], axis=0)
    return labels, cluster_centers, num_centers




def writeOutData(df, labels, cluster_centers, db):
    # Add a column with cluster id
    
    df['ClusterId'] = labels + 1  
    votes = df['vote']
    
    # Create vote dictionary
    cluster_vote_dict = {}
    for cluster_id in set(labels):
        cluster_votes = votes[labels == cluster_id]
        cluster_vote_dict[cluster_id] = dict(Counter(cluster_votes))
        
    # for Id in df['User_ID']:
    #     update_data = {
    #         'ClusterId': df['ClusterId'][Id],
    #     }
    #     db.collection('users').document(str(Id)).update(update_data)
    
    df_cluster_centers = pd.DataFrame(cluster_centers, columns=['x', 'y'])
    
    print(cluster_vote_dict)
    
    users = db.collection('users').get()
    iterator = 0
    for user in users:
        key = user.id
        clusterIDtag = int(df['ClusterId'][iterator])
        db.collection('users').document(key).update({
            'ClusterId': clusterIDtag,
        })
        iterator += 1
        
    for i in range(len(df_cluster_centers)):
        key = "Machine" + str(i+1)
        db.collection('VendingLocations').document(key).update({
            'x': df_cluster_centers['x'][i],
            'y': df_cluster_centers['y'][i]
        })

    
def visualizeData(df, cluster_centers, all_cluster_centers, num_centers):
    fig, axs = plt.subplots(2)
    
    
    # Create scatter plot for visualization
    only_active_users = df[df['vote'] != 0]
    only_inactive_users = df[df['vote'] == 0]
    colors=['r', 'g', 'b', 'y', 'c', 'm']

    # For each unique clusterId, create a separate scatter plot with a label
    for clusterId in only_active_users['ClusterId'].unique():
        clustered_data = only_active_users[only_active_users['ClusterId']==clusterId]
        axs[0].scatter(clustered_data['x'], clustered_data['y'], color=colors[clusterId % len(colors)], label= f"Cluster {clusterId}")

    
    axs[0].scatter(only_inactive_users['x'], only_inactive_users['y'], c='gray')

    axs[0].scatter(
        cluster_centers[:num_centers, 0], cluster_centers[:num_centers, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    axs[0].set_title('Active Clusters')
    img = plt.imread("map.png")
    axs[0].imshow(img)
    axs[0].legend()


    for clusterId in df['ClusterId'].unique():
        clustered_data = df[df['ClusterId']==clusterId]
        axs[1].scatter(clustered_data['x'], clustered_data['y'], color=colors[clusterId % len(colors)], label= f"Cluster {clusterId}")

    axs[1].scatter(
        all_cluster_centers[:num_centers, 0], all_cluster_centers[:num_centers, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    axs[1].set_title('All Clusters')   
    img = plt.imread("map.png")
    axs[1].imshow(img) 
    axs[1].legend()
    
    # Add labels for whole figure
    fig.suptitle('Cluster Visualization')

    plt.savefig("ClusterVisualization.png")

def main():
    csv_path = "VotingSampleData.csv"
    cluster_csv_path = "Clusters.csv"
    cred = credentials.Certificate("eatclusive-plant-data-firebase-adminsdk-3xb6s-cb1f31e924.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    df, InactiveUsers, active_users, labels, cluster_centers, all_labels, all_cluster_centers, num_centers = readInData(db)
    
    writeOutData(df, all_labels, cluster_centers, db)
    
    visualizeData(df, cluster_centers, all_cluster_centers, num_centers)

__init__ = main()
