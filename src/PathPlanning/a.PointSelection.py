"""
PointSelection.py

Clusters the coordinates from Sampling_Priority.csv file using DBSCAN and saves the clustered data to a clustered_coordinates.csv. 
Also generates a plot of the clusters with a basemap and saves cluster information (centroid and weight) to cluster_info.csv.
"""

import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'

# Load the CSV file
file_path = DATA_DIR / '1.Sampling_Priority.csv'
data = pd.read_csv(file_path)

# Normalise the sensitivity values as sigma' = sigma / max(S), per Eq. 8 of the
# manuscript.  Dividing by a single positive constant is a monotone rescaling, so
# it changes neither the ranking of cells, the relative cluster weights, nor the
# route selected; it makes the reported weights dimensionless and comparable
# between runs.  Earlier versions defined this normalisation but summed the raw
# values, which is the inconsistency Reviewer 2 identified.
SENSITIVITY_COLUMN = 'Depth-averaged uncertainty'
_max_sensitivity = data[SENSITIVITY_COLUMN].max()
if _max_sensitivity <= 0:
    raise ValueError(f"{file_path}: maximum sensitivity is {_max_sensitivity}; cannot normalise.")
data[SENSITIVITY_COLUMN] = data[SENSITIVITY_COLUMN] / _max_sensitivity

# Extract the latitude and longitude values
coordinates = data[['Latitude', 'Longitude']].values

# Convert latitude and longitude to radians for Haversine distance calculation
coordinates = np.radians(coordinates)

# Perform DBSCAN clustering using Haversine distance
# eps is in radians, so you need to convert your desired distance (e.g., 500 meters) to radians
eps = 100 / 6371000  # x meters converted to radians (Earth's radius is approximately 6371000 meters)
dbscan = DBSCAN(eps=eps, min_samples=1, metric='haversine')
clusters = dbscan.fit_predict(coordinates)

# Add the cluster labels to the original data
data['cluster'] = clusters

# Calculate the centroid and number of points in each cluster
cluster_info = data.groupby('cluster').agg(
    Latitude=('Latitude', 'mean'),
    Longitude=('Longitude', 'mean'),
    Weight=('Depth-averaged uncertainty', 'sum')
).reset_index()



# Create a legend for the discrete cluster labels
unique_clusters = data['cluster'].unique()

# Plot the clusters with a basemap
fig, ax = plt.subplots(figsize=(10, 10))

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.viridis(i / len(unique_clusters)), markersize=10, label=f'Cluster {i+1}') for i in unique_clusters]
ax.legend(handles=handles, title='Cluster Labels')

scatter = ax.scatter(data['Longitude'], data['Latitude'], c=data['cluster'], cmap='viridis', marker='o')
ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, crs='EPSG:4326')
ax.set_aspect('equal', 'box')
# plt.title('DBSCAN Clustering with Basemap')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
min_longitude, max_longitude = (6.384, 6.55)
min_latitude, max_latitude = (62.461, 62.488)
plt.xlim(min_longitude, max_longitude)
plt.ylim(min_latitude, max_latitude)
# plt.colorbar(scatter, label='Cluster Label')
plt.show()

# Save the clustered data to a new CSV file
output_file_path = DATA_DIR / '2.clustered_coordinates.csv'
data.to_csv(output_file_path, index=False)
print(f"Clustering analysis completed. The results are saved to {output_file_path}.")

# Save the cluster information to a new CSV file
cluster_info_file_path = DATA_DIR / '3.cluster_info.csv'
cluster_info.to_csv(cluster_info_file_path, index=False)
print(f"Cluster information saved to {cluster_info_file_path}.")
