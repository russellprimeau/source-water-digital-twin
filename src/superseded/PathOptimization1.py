"""

PathOptimization1.py

Finds the shortest path through all points in the dataframe, starting and ending at specified points. 
The optimized path is saved to highscore_path.csv.
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'

# Finds the shortest path through all points in the dataframe, starting and ending at specified points
def shortest_path_through_all_points(df, start, end):
    # Extract coordinates from the dataframe
    coordinates = df[['Latitude', 'Longitude']].values

    # Add the starting and ending points to the coordinates
    coordinates = np.vstack([start, coordinates, end])

    # Calculate the pairwise distances between all points
    distance_matrix = squareform(pdist(coordinates, metric='euclidean'))

    # Generate all possible permutations of the points (excluding start and end)
    points = list(range(1, len(coordinates) - 1))
    all_permutations = permutations(points)

    shortest_distance = float('inf')
    best_path = None

    # Iterate through all permutations to find the shortest path
    for perm in all_permutations:
        path = [0] + list(perm) + [len(coordinates) - 1]
        distance = sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))

        if distance < shortest_distance:
            shortest_distance = distance
            best_path = path

    # Convert the best path indices to coordinates
    best_path_coordinates = coordinates[best_path]

    return best_path_coordinates, shortest_distance


# Example usage:
# Create a dataframe with latitude and longitude values
data = {'Latitude': [34.052235, 36.169941, 40.712776],
        'Longitude': [-118.243683, -115.139832, -74.005974]}
df = pd.DataFrame(data)

# Load the CSV file
file_path = DATA_DIR / '1.Sampling_Priority.csv'
df = pd.read_csv(file_path, sep=',', usecols=['Latitude', 'Longitude'])

# Define the starting and ending points
start_point = np.array([62.465779, 6.401947])  # Vasstrandlia ramp
end_point = np.array([62.465779, 6.401947])

# Find the shortest path through all points
path_coordinates, total_distance = shortest_path_through_all_points(df, start_point, end_point)

print("Shortest path coordinates:")
print(path_coordinates)
print(f"Total distance: {total_distance} units")

# Save the optimized data to a new CSV file
pd.DataFrame(path_coordinates, columns=['Latitude', 'Longitude']).to_csv(DATA_DIR / 'superseded_shortest_path.csv', index=False)
