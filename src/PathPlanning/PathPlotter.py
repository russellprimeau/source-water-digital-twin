"""
PathPlotter.py

Several alternative methods to plot CSV files containing a list of coordinates,
such as those which the path planning utilities in the BrusdalsvatnetDT post-processing module produce.

Methods include:
- Static matplotlib figure with coordinate points labelled and connected by lines.
- Folium-based interactive map written to an html file (can open in browser).
- Plotly-based interactive map displayed in browser.
- Animated matplotlib figure which draws a thick line to connect points, at constant speed which can be specified.
Animation can be written to filea as .gif.

"""
import pandas as pd
import matplotlib.pyplot as plt
import folium
import plotly.graph_objects as go
import plotly.express as px
import contextily as ctx
import cartopy.crs as ccrs
import numpy as np
from geopy.distance import geodesic
from matplotlib.animation import FuncAnimation, PillowWriter, ImageMagickWriter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'



def read_coordinates(file_name):
    raw = pd.read_csv(file_name, dtype={'label': str}, sep=',', header=0, names=['label', 'sensitivity', 'longitude', 'latitude', 'time'],  index_col=None)
    columns = ['latitude', 'longitude', 'label', 'sensitivity']
    coordinates = [tuple(x) for x in raw[columns].values]
    print('coordinates', coordinates)
    # with open(file_name, 'r') as file:
    #     lines = file.readlines()
    #     coordinates = []
    #     for line in lines:
    #         parts = line.strip().split(',')
    #         print(parts)
    #         lat = float(parts[3])
    #         lon = float(parts[4])
    #         label = parts[1]
    #         coordinates.append((lat, lon, label))
    #     print(coordinates)
    return coordinates


def read_cluster_coordinates(file_name):
    raw = pd.read_csv(file_name, dtype={'cluster': str}, sep=',', header=0, names=['label', 'sensitivity', 'longitude', 'latitude', 'time', 'cluster'],  index_col=None)
    columns = ['latitude', 'longitude', 'cluster' ]
    coordinates = [tuple(x) for x in raw[columns].values]
    print('cluster coordinates', coordinates)
    # with open(file_name, 'r') as file:
    #     lines = file.readlines()
    #     coordinates = []
    #     for line in lines:
    #         parts = line.strip().split(',')
    #         print(parts)
    #         lat = float(parts[3])
    #         lon = float(parts[4])
    #         label = parts[1]
    #         coordinates.append((lat, lon, label))
    #     print(coordinates)
    return coordinates


def matplotllib_method(file_name):
    """
    Matplotlib figure with coordinate points labelled and connected by lines.
    Pros: static image; labels visible by default; lines connecting points; quickest to format in code.
    Cons: no default basemap; no interactivity.

    :param file_name: path to .csv file or similar with columns 'latitude', 'longitude', 'label'.
    :return: none.
    """

    # Read the coordinates from the file
    coordinates = read_coordinates(file_name)

    # Create a map
    # fig, ax = plt.figure(figsize=(12, 8))
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

    # OPTION (incomplete): use contextily to add for basemap instead of mpl_toolkits.basemap
    # ctx.add_basemap(ax, crs='epsg:4326', source=ctx.providers.OpenTopoMap)  # or other providers

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()

    # Plot the coordinates
    for i in range(len(coordinates)):
        lat, lon, label = coordinates[i]
        x, y = m(lon, lat)
        m.plot(x, y, 'bo')  # Plot the point
        plt.text(x, y, f' {label}', fontsize=12)  # Label the point

        if i > 0:
            prev_lat, prev_lon, prev_label = coordinates[i - 1]
            prev_x, prev_y = m(prev_lon, prev_lat)
            m.plot([prev_x, x], [prev_y, y], 'k-')  # Draw line between points

    plt.title('Coordinate Points on World Map')
    plt.show()


def folium_method(file_name):
    """
    Folium-based interactive map written to an html file (can open in browser).

    Pros: nice physical-political default basemap; points connected by lines; flags on each coordinate.
    Cons: flags do not show labels unless clicked on (requires interaction, not good for a static image);
        difficult to add a legend.
    :param file_name: path to .csv file or similar with columns 'latitude', 'longitude', 'label'.
    :return: none.
    """

    # Read the coordinates from the file
    coordinates = read_coordinates(file_name)

    # Create a map centered around the first coordinate
    map_center = [coordinates[0][0], coordinates[0][1]]
    mymap = folium.Map(location=map_center, zoom_start=2)

    # Add markers and lines to the map
    for i in range(len(coordinates)):
        lat, lon, label = coordinates[i]
        folium.Marker([lat, lon], popup=label).add_to(mymap)

        if i > 0:
            prev_lat, prev_lon, prev_label = coordinates[i - 1]
            folium.PolyLine([[prev_lat, prev_lon], [lat, lon]], color="blue").add_to(mymap)

    mymap.show_in_browser()

    # Save the map to an HTML file
    mymap.save(DATA_DIR / 'map.html')
    print(f"Map has been saved to {DATA_DIR / 'map.html'}")


def plotly_method(file_name):
    """
    Plotly-based interactive map displayed in browser.
    Pros: Labels visible by default; better interactions than folium, including legend by default.
    Cons: Lower-quality default basemap.
    :param file_name: path to .csv file or similar with columns 'latitude', 'longitude', 'label'.
    :return: none.
    """


    # Read the coordinates from the file
    coordinates = read_coordinates(file_name)

    # Extract labels, latitudes, and longitudes
    lats = [coord[0] for coord in coordinates]
    lons = [coord[1] for coord in coordinates]
    labels = [coord[2] for coord in coordinates]

    # Load the CSV file
    file_path = DATA_DIR / 'cluster_info.csv'
    df = pd.read_csv(file_path, sep=',', usecols=['Latitude', 'Longitude', 'Weight'])

    # Create a scatter plot with Plotly
    fig = go.Figure()

    # Add points to the map
    fig.add_trace(go.Scattermap(
        lon=lons,
        lat=lats,
        text=labels,
        mode='markers+text',
        marker=dict(size=8, color='black'),
        textposition='top center',
        textfont=dict(size=18),
        name='Data Collection Points'
    ))

    # Add lines between points
    for i in range(len(coordinates) - 1):
        if i == 0:
            fig.add_trace(go.Scattermap(
            lon=[coordinates[i][1], coordinates[i + 1][1]],
            lat=[coordinates[i][0], coordinates[i + 1][0]],
            mode='lines',
            line=dict(width=2, color='black'),
            name='Data Collection Path',
            showlegend=True
            ))
        else:
            fig.add_trace(go.Scattermap(
                lon=[coordinates[i][1], coordinates[i + 1][1]],
                lat=[coordinates[i][0], coordinates[i + 1][0]],
                mode='lines',
                line=dict(width=2, color='black'),
                showlegend=False
            ))

    clusterpoints = read_cluster_coordinates(DATA_DIR / 'clustered_coordinates.csv')

    # Extract labels, latitudes, and longitudes
    cluster_lats = [coord[0] for coord in clusterpoints]
    cluster_lons = [coord[1] for coord in clusterpoints]
    clusters = [coord[2] for coord in clusterpoints]

    # Get unique labels and sort them alphabetically
    unique_clusters = sorted(list(set(clusters)))

    # Generate colors for each unique label using Plotly's color sequence
    colors = px.colors.qualitative.Plotly

    # Create a dictionary to map labels to colors programmatically
    label_colors = {label: colors[i % len(colors)] for i, label in enumerate(unique_clusters)}

    for i, cluster in enumerate(unique_clusters):
        trace = go.Scattermap(
            lat=[x for x, l in zip(cluster_lats, clusters) if l == cluster],
            lon=[y for y, l in zip(cluster_lons, clusters) if l == cluster],
            mode='markers',
            marker=dict(color=label_colors[cluster]),
            name=f'Total cluster weight: {round(df["Weight"][i]*1E10, 2)}',
        )
        fig.add_trace(trace)

    # Update layout for better visualization with OpenStreetMap basemap
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            zoom=1,
            center=dict(lat=lats[1], lon=lons[1])),
        legend = dict(font=dict(
            size=18))  # Change the legend text size here
    )

    # Show the plot
    fig.show()


def animated_method(file_name):
    """
    Animated matplotlib figure which draws a thick line to connect points, at constant speed which can be specified.
    Animation can be written to filea as .gif.
    :param file_name: path to .csv file or similar with columns 'latitude', 'longitude', 'label'.
    :return: none.
    """
    # Animated method
    ###################################################################################################################
    # Assuming the text file has columns 'latitude' and 'longitude'
    df = pd.read_csv(file_name, sep=';', header=0, names=['label', 'sensitivity', 'longitude', 'latitude', 'time'])
    print(df)

    min_longitude, max_longitude = (6.384, 6.57)

        # df['longitude'].min() - abs(0.05 * df['longitude'].min()), df[
        # 'longitude'].max() + abs(0.05 * df['longitude'].max()))
    min_latitude, max_latitude = (62.461, 62.488)
    # df['latitude'].min() - abs(0.05 * df['latitude'].min()), df['latitude'].max() + abs(
    #     0.05 * df['latitude'].max())

    # Interpolate between coordinates
    def interpolate_equidistant_points(df, distance_interval=1, repeat_factor=10):
        points = []
        for i in range(len(df) - 1):
            start = (df['latitude'][i], df['longitude'][i])
            end = (df['latitude'][i + 1], df['longitude'][i + 1])
            total_distance = geodesic(start, end).km
            num_points = int(total_distance / distance_interval)
            latitudes = np.linspace(start[0], end[0], num_points)
            longitudes = np.linspace(start[1], end[1], num_points)
            points.extend(zip(latitudes, longitudes))
            # Repeat the end point to create a pause
            points.extend([(end[0], end[1])] * repeat_factor)
        return pd.DataFrame(points, columns=['latitude', 'longitude'])

    interpolated_df = interpolate_equidistant_points(df, distance_interval=0.01, repeat_factor=5)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([min_longitude, max_longitude, min_latitude, max_latitude], crs=ccrs.PlateCarree())

    ctx.add_basemap(ax, crs='epsg:4326', source=ctx.providers.OpenTopoMap)  # or other providers

    # OPTION: instead of contextily basemap, use simpler cartopy basemap.
    # ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS)
    # ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.OCEAN)

    def update(num, interpolated_df, df, line, ax):
        line.set_data(interpolated_df['longitude'][:num], interpolated_df['latitude'][:num])
        # ax.clear()
        # ax.add_image(maptiler, 8)
        for i in range(len(df)):
            ax.text(df['longitude'][i], df['latitude'][i], df['label'][i], fontsize=12, color='blue', weight='bold',
                    ha='right', va='bottom', bbox=dict(facecolor='white', alpha=0.7))
        return line,

    line, = ax.plot([], [], 'r-', markersize=5)
    ani = FuncAnimation(fig, update, frames=len(interpolated_df), fargs=[interpolated_df, df, line, ax], interval=50,
                        blit=True, repeat=False)

    # To view the figure:
    # plt.show()

    # To export the animation as a GIF:
    writer = PillowWriter(fps=20, metadata={'title': 'Map Animation'}, bitrate=1800)
    # writer = ImageMagickWriter(fps=5, extra_args=['-loop', '1'])

    output_file = 'animated.gif'
    ani.save(DATA_DIR / output_file, dpi=80, writer=writer)


if __name__ == '__main__':
    # input_file = 'manual_path.csv'
    input_file = 'highscore_path.csv'
    input = DATA_DIR / input_file

    # To create a static matplotlib figure with lines connecting the points:
    # matplotllib_method(input)  # looks terrible

    # To create a folium map with markers and lines connecting the points:
    # folium_method(input)

    # # To create an interactive plotly figure with lines connecting the points:
    plotly_method(input)

    # # To create an animated matplotlib figure with lines connecting the points:
    # animated_method(input)

    pass
