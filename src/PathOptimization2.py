import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations
from geopy.distance import geodesic
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'

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

    # # Generate all possible permutations of the points (excluding start and end)
    # points = list(range(1, len(coordinates) - 1))
    # all_permutations = permutations(points)

    highest_score = float('-inf')
    best_path = None
    pathlength = None

    # Iterate through all combinations of points to find the highest-scoring path within the distance constraint
    for r in range(1, len(coordinates) - 1):
        for comb in permutations(range(1, len(coordinates) - 1), r):
            path = [0] + list(comb) + [len(coordinates) - 1]
            distance = sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
            score = sum(scores[i - 1] for i in comb)  # Subtract 1 to account for the starting point index
            print(f'range {r}, comb {comb}, distance ', distance, 'score ', score)

            if distance <= max_distance and score > highest_score:
                highest_score = score
                best_path = path
                pathlength = distance
                order = list(comb)
            elif distance <= max_distance and score == highest_score:
                if round(distance,3) < round(pathlength,3):
                    pathlength = distance
                    best_path = path
                    order = list(comb)

    # Convert the best path indices to coordinates
    best_path_coordinates = coordinates[best_path]
    return best_path_coordinates, highest_score, pathlength, order


# Example usage:
# Create a dataframe with latitude, longitude values, and scores
# data = {'latitude': [34.052235, 36.169941, 40.712776],
#         'longitude': [-118.243683, -115.139832, -74.005974],
#         'score': [10, 20, 30]}
# df = pd.DataFrame(data)

# Load the CSV file
file_path = DATA_DIR / 'cluster_info.csv'
df = pd.read_csv(file_path, sep=',', usecols=['Latitude', 'Longitude', 'Weight'])

print('input', df)

# Define the starting and ending points
start_point = np.array([62.465779, 6.401947])  # Vasstrandlia ramp
end_point = np.array([62.465779, 6.401947])

# Define the maximum path length constraint
max_path_length = 6000  # Example value in units consistent with the distance metric

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
    output_file_path = DATA_DIR / 'highscore_path.csv'

    # Convert the NumPy array to a DataFrame to output to CSV
    header = ['latitude', 'longitude']
    names = ['label', 'sensitivity', 'time']
    df_out = pd.DataFrame(path_coordinates, columns=header)
    df_out.reset_index(inplace=True)
    df_out['label'] = df_out.index + 1
    df_out['sensitivity'] = [0] + df.loc[order, 'Weight'].tolist() + [0]
    df_out['time'] = np.nan
    print(df_out)
    new_order = ['label', 'sensitivity', 'longitude', 'latitude', 'time']
    df_out = df_out[new_order]
    df_out.to_csv(output_file_path, index=False)