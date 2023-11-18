# Import libraries
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

# Load the data
# Assume we have a CSV file 'data.csv' with columns 'population_density', 'mean_distance_to_food_center'

data = pd.read_csv('data.csv')

# Preprocess & normalize the data
scaler = MinMaxScaler()

scaler.fit(data[['mean_distance_to_food_center']])
data['mean_distance_to_food_center'] = scaler.transform(data[['mean_distance_to_food_center']])

scaler.fit(data[['population_density']])
data['population_density'] = scaler.transform(data[['population_density']])

# Apply KMeans
km = KMeans(n_clusters=3)  # Assume we want to create 3 clusters
y_predicted = km.fit_predict(data[['mean_distance_to_food_center', 'population_density']])

# Add the prediction to the data
data['cluster'] = y_predicted

# Visualize the clusters
df1 = data[data.cluster==0]
df2 = data[data.cluster==1]
df3 = data[data.cluster==2]

plt.scatter(df1.mean_distance_to_food_center, df1.population_density, color='green')
plt.scatter(df2.mean_distance_to_food_center, df2.population_density, color='red')
plt.scatter(df3.mean_distance_to_food_center, df3.population_density, color='blue')

plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1], color='purple', marker='*', label='centroid')
plt.legend()