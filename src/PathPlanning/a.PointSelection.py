"""
PointSelection.py

Clusters the coordinates from Sampling_Priority.csv file using DBSCAN and saves the clustered data to a clustered_coordinates.csv. 
Also generates a plot of the clusters with a basemap and saves cluster information (centroid and weight) to cluster_info.csv.
"""

import sys

import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances
import numpy as np
import matplotlib

# This script is a step in a pipeline, so it must not open a window and block the
# steps after it. The diagnostic plot is written to disk; pass --show to open it.
SHOW = '--show' in sys.argv
if not SHOW:
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route_solver

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data' / 'sampling_plan'

# Load the CSV file
file_path = DATA_DIR / '1.Sampling_Priority.csv'
data = pd.read_csv(file_path)

# Normalise the model-spread scores as sigma' = sigma / max(sigma).  This is the
# normalisation defined in Section 2.3 of the manuscript, in the prose just
# before Equation (8); Equation (8) itself is the top-r selection that consumes
# the normalised scores.  Dividing by a single positive constant is a monotone
# rescaling, so it changes neither the ranking of cells, the relative cluster
# weights, nor the route selected; it makes the reported weights dimensionless
# and comparable between runs.
#
# This is a ranking score derived from relative spread among model alternatives;
# it is not a calibrated uncertainty estimate. See Section 2.3.
SENSITIVITY_COLUMN = 'Model-spread score'
_max_sensitivity = data[SENSITIVITY_COLUMN].max()
if _max_sensitivity <= 0:
    raise ValueError(f"{file_path}: maximum sensitivity is {_max_sensitivity}; cannot normalise.")
data[SENSITIVITY_COLUMN] = data[SENSITIVITY_COLUMN] / _max_sensitivity

# Extract the latitude and longitude values
coordinates = data[['Latitude', 'Longitude']].values

# Convert latitude and longitude to radians for Haversine distance calculation
coordinates = np.radians(coordinates)

# Perform DBSCAN clustering using Haversine distance. The neighbourhood is held in
# route_solver with the distance budget, so the radius reported in the article, the
# radius the stability analysis resamples under and the radius swept by
# ClusterRadius.py are one value. The metric wants radians.
eps = route_solver.CLUSTER_EPS_M / route_solver.EARTH_RADIUS_M
dbscan = DBSCAN(eps=eps, min_samples=1, metric='haversine')
clusters = dbscan.fit_predict(coordinates)

# Add the cluster labels to the original data
data['cluster'] = clusters

# Calculate the centroid and number of points in each cluster
cluster_info = data.groupby('cluster').agg(
    Latitude=('Latitude', 'mean'),
    Longitude=('Longitude', 'mean'),
    Weight=(SENSITIVITY_COLUMN, 'sum')
).reset_index()



# Create a legend for the discrete cluster labels
unique_clusters = data['cluster'].unique()

# Plot the clusters with a basemap
fig, ax = plt.subplots(figsize=(10, 10))

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.viridis(i / len(unique_clusters)), markersize=10, label=f'Cluster {i+1}') for i in unique_clusters]
ax.legend(handles=handles, title='Cluster Labels')

scatter = ax.scatter(data['Longitude'], data['Latitude'], c=data['cluster'], cmap='viridis', marker='o')
# The shoreline comes from the published mesh rather than from downloaded map tiles:
# a script in this repository should not need the network to produce its output, and
# the mesh boundary is the coastline the model actually sees.
outline_path = DATA_DIR / 'lake_outline_segments.csv'
if outline_path.exists():
    segments = pd.read_csv(outline_path).to_numpy().reshape(-1, 2, 2)
    ax.add_collection(LineCollection(segments, color='0.6', lw=.8, zorder=1))
ax.set_aspect('equal', 'box')
# plt.title('DBSCAN Clustering with Basemap')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
min_longitude, max_longitude = (6.384, 6.55)
min_latitude, max_latitude = (62.461, 62.488)
plt.xlim(min_longitude, max_longitude)
plt.ylim(min_latitude, max_latitude)
# plt.colorbar(scatter, label='Cluster Label')
cluster_plot_path = DATA_DIR / 'clusters_diagnostic.png'
cluster_plot_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(cluster_plot_path, dpi=150, bbox_inches='tight')
if SHOW:
    plt.show()
plt.close(fig)
print(f"Cluster diagnostic plot saved to {cluster_plot_path}.")

# Save the clustered data to a new CSV file
output_file_path = DATA_DIR / '2.clustered_coordinates.csv'
data.to_csv(output_file_path, index=False)
print(f"Clustering analysis completed. The results are saved to {output_file_path}.")

# Save the cluster information to a new CSV file
cluster_info_file_path = DATA_DIR / '3.cluster_info.csv'
cluster_info.to_csv(cluster_info_file_path, index=False)
print(f"Cluster information saved to {cluster_info_file_path}.")
