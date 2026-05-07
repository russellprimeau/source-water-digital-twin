import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'


def index_to_alphabet(index):
    """Converts a zero-based index to an alphabetical character (a-z)."""
    if 0 <= index < 26:
        return chr(ord('A') + index)
    else:
        return None  # Or raise an exception for indices outside the range

def read_coordinates(file_name):
    raw = pd.read_csv(file_name, dtype={'label': str}, sep=',', header=0, names=['label', 'sensitivity', 'longitude', 'latitude', 'time'],  index_col=None)
    columns = ['latitude', 'longitude', 'label', 'sensitivity']
    coordinates = [tuple(x) for x in raw[columns].values]
    return coordinates

def read_cluster_coordinates(file_name):
    raw = pd.read_csv(file_name, dtype={'cluster': str}, sep=',', header=0, names=['label', 'sensitivity', 'longitude', 'latitude', 'time', 'cluster'],  index_col=None)
    columns = ['latitude', 'longitude', 'cluster' ]
    coordinates = [tuple(x) for x in raw[columns].values]
    return coordinates

def matplotlib_method_with_contextily(file_name):
    # Read the coordinates from the file
    coordinates = read_coordinates(file_name)

    # Extract labels, latitudes, and longitudes
    lats = [coord[0] for coord in coordinates]
    lons = [coord[1] for coord in coordinates]
    labels = [coord[2] for coord in coordinates]

    # Load the CSV file
    file_path = DATA_DIR / 'cluster_info.csv'
    df = pd.read_csv(file_path, sep=',', usecols=['Latitude', 'Longitude', 'Weight'])

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 4))
    fontsizer = 17

    clusterpoints = read_cluster_coordinates(DATA_DIR / 'clustered_coordinates.csv')

    # Extract labels, latitudes, and longitudes
    cluster_lats = [coord[0] for coord in clusterpoints]
    cluster_lons = [coord[1] for coord in clusterpoints]
    clusters = [coord[2] for coord in clusterpoints]

    # Get unique labels and sort them alphabetically
    unique_clusters = sorted(list(set(clusters)))

    # Generate colors for each unique label using a colormap
    colors = plt.get_cmap('spring', len(unique_clusters))

    # Create a dictionary to map labels to colors programmatically
    label_colors = {label: colors(i) for i, label in enumerate(unique_clusters)}

    for i, cluster in enumerate(unique_clusters):
        cluster_lats_i = [x for x, l in zip(cluster_lats, clusters) if l == cluster]
        cluster_lons_i = [y for y, l in zip(cluster_lons, clusters) if l == cluster]
        ax.scatter(cluster_lons_i, cluster_lats_i, color=label_colors[cluster], s=1, label=f'Cluster {index_to_alphabet(i)}, weight: {round(df["Weight"][i], 2)}')

    # Add points to the map
    scatter = ax.scatter(lons, lats, c='black', s=1, label='Data collection waypoint')

    # Add text labels to the points
    for i, label in enumerate(labels):
        if i + 1 < len(labels):
            ax.text(lons[i], lats[i], label, fontsize=fontsizer, ha='center', va='bottom')

    # Add lines between points
    for i in range(len(coordinates) - 1):
        if i == 0:
            ax.plot([coordinates[i][1], coordinates[i + 1][1]], [coordinates[i][0], coordinates[i + 1][0]], 'k-',
                    linewidth=1, label='USV path')
        else:
            ax.plot([coordinates[i][1], coordinates[i + 1][1]], [coordinates[i][0], coordinates[i + 1][0]], 'k-',
                linewidth=1)

    ax.set_xlabel("Longitude", fontsize=fontsizer)
    ax.set_ylabel("Latitude", fontsize=fontsizer)
    ax.tick_params(axis='x', labelsize=fontsizer)
    ax.tick_params(axis='y', labelsize=fontsizer)
    xmin, xmax = (6.384, 6.574)
    ymin, ymax = (62.461, 62.488)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Add the basemap using Contextily
    ctx.add_basemap(ax=ax, zoom=15, crs='EPSG:4326', source=ctx.providers.OpenTopoMap, attribution=False)

    ax.legend(bbox_to_anchor=(0.5,1), fontsize=fontsizer-3, loc='lower center', markerscale=3, ncols=4)
    ax.set_aspect('equal', 'box')  # Prevents map distortion

    # Adjust the bottom margin
    plt.subplots_adjust(top=1.02)  # Increase margin

    # Set the linewidth of the axes' spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)  # Change the value to adjust thickness

    plt.tight_layout()  # Keeps the legend from extending out of the figure
    plt.savefig(DATA_DIR / 'clustered.png', dpi=600)
    plt.show()

if __name__ == '__main__':
    # input_file = 'manual_path.csv'
    input_file = 'highscore_path.csv'
    input = DATA_DIR / input_file

    # To create a matplotlib figure with lines connecting the points and a Contextily basemap:
    matplotlib_method_with_contextily(input)
