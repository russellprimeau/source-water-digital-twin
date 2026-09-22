"""
PathOptimization2.py

Finds the highest-scoring path through all points in cluster_info.csv, starting and ending at specified points,
subject to a constraint on the total path length.

Writes the path to 4.highscore_path.csv: latitude, longitude, the summed model-spread score of the cluster visited, and a sequential label for each point in the path.
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations
from geopy.distance import geodesic
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import route_solver

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data' / 'sampling_plan'

# Finds the highest-scoring path through all points in the dataframe, starting and ending at specified points,
# subject to a constraint on the total path length

def highest_scoring_path(df, start, end, max_distance):
    # Extract coordinates and scores from the dataframe
    coordinates = df[['Latitude', 'Longitude']].values
    scores = df['Weight'].values

    # Add the starting and ending points to the coordinates
    coordinates = np.vstack([start, coordinates, end])
    print('coordinates:', len(coordinates))

    # Calculate the pairwise distances between all points using geodesic distance
    distance_matrix = np.zeros((len(coordinates), len(coordinates)))
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            distance_matrix[i, j] = geodesic(coordinates[i], coordinates[j]).meters

    print('distance_matrix', distance_matrix)

    # Enumerating every ordering of every subset costs sum_r P(n, r) routes, about
    # 2,000 for six clusters but 1.2e11 for fourteen. route_solver.solve() returns
    # the same answer from a dynamic program over (visited set, last point); see the
    # module docstring for why the two are equivalent.
    order, highest_score, pathlength = route_solver.solve(
        distance_matrix, scores, max_distance)
    if not order:
        return None, highest_score, pathlength, order

    best_path = [0] + list(order) + [len(coordinates) - 1]
    best_path_coordinates = coordinates[best_path]
    return best_path_coordinates, highest_score, pathlength, order


# Example usage:
# Create a dataframe with latitude, longitude values, and scores
# data = {'latitude': [34.052235, 36.169941, 40.712776],
#         'longitude': [-118.243683, -115.139832, -74.005974],
#         'score': [10, 20, 30]}
# df = pd.DataFrame(data)

# Load the CSV file
file_path = DATA_DIR / '3.cluster_info.csv'
df = pd.read_csv(file_path, sep=',', usecols=['Latitude', 'Longitude', 'Weight'])

print('input', df)

# Define the starting and ending points
start_point = np.array(route_solver.LAUNCH_POINT)  # Vasstrandlia ramp
end_point = np.array(route_solver.LAUNCH_POINT)

# Define the maximum path length constraint
# Shared with c.StabilityAnalysis.py so the planner and its stability check cannot
# be run against different budgets.
max_path_length = route_solver.MAX_PATH_LENGTH_M

# Find the highest-scoring path within the distance constraint
path_coordinates, total_score, pathlength, order = highest_scoring_path(df, start_point, end_point, max_path_length)

for i in range(len(order)):
    order[i] -= 1

if path_coordinates is None:
    print("No path found within the distance constraint.")
    exit()
else:
    print("Highest-scoring path:")
    print('0,',order,'0')
    print(path_coordinates)
    print(f"Total score: {total_score}")
    print(f"Path length: {pathlength}")
    print(df.loc[order, 'Weight'])

    # Save the optimized data to a new CSV file
    output_file_path = DATA_DIR / '4.highscore_path.csv'

    # Convert the NumPy array to a DataFrame to output to CSV
    header = ['latitude', 'longitude']
    names = ['label', 'Cluster weight', 'time']
    df_out = pd.DataFrame(path_coordinates, columns=header)
    df_out.reset_index(inplace=True)
    df_out['label'] = df_out.index + 1
    df_out['Cluster weight'] = [0] + df.loc[order, 'Weight'].tolist() + [0]
    df_out['time'] = np.nan
    print(df_out)
    new_order = ['label', 'Cluster weight', 'longitude', 'latitude', 'time']
    df_out = df_out[new_order]
    df_out.to_csv(output_file_path, index=False)
