# Path Planning Workflow and Plotter Comparison

## Scope

This note summarizes the scripts in `src/PathPlanning/` and how they appear intended to pass data between each other. The workflow is file-based: scripts read and write CSV files in the repo-level `data/` directory.

## Scripts

- `src/PathPlanning/PointSelection.py`
- `src/PathPlanning/PathOptimization1.py`
- `src/PathPlanning/PathOptimization2.py`
- `src/PathPlanning/PathPlotter.py`
- `src/PathPlanning/PathPlotter2.py`

## Main Dataflow

The current intended workflow appears to be:

```text
data/Sampling_Priority.csv
        |
        v
PointSelection.py
        |
        +--> data/clustered_coordinates.csv
        +--> data/cluster_info.csv
                    |
                    v
          PathOptimization2.py
                    |
                    v
             data/highscore_path.csv
                    |
                    v
        PathPlotter.py or PathPlotter2.py
```

## Data Files

- `data/Sampling_Priority.csv`
  - Input to `PointSelection.py`.
  - Also read directly by `PathOptimization1.py`.
  - Expected columns include `Latitude`, `Longitude`, `Depth-averaged uncertainty`, and `time`.

- `data/clustered_coordinates.csv`
  - Written by `PointSelection.py`.
  - Contains the original sampling-priority rows plus a `cluster` column.
  - Read by `PathPlotter.py` and `PathPlotter2.py` to show original clustered points.

- `data/cluster_info.csv`
  - Written by `PointSelection.py`.
  - Contains one row per cluster with centroid `Latitude`, centroid `Longitude`, and summed `Weight`.
  - Read by `PathOptimization2.py` as candidate waypoints.
  - Read by both plotters to label or weight clusters.

- `data/highscore_path.csv`
  - Written by `PathOptimization2.py`.
  - Read by `PathPlotter.py` and `PathPlotter2.py`.
  - Current plotter-compatible schema:

```text
label,sensitivity,longitude,latitude,time
```

## Script Roles

### `PointSelection.py`

Clusters coordinates from `data/Sampling_Priority.csv` using DBSCAN with haversine distance. It writes:

- `data/clustered_coordinates.csv`
- `data/cluster_info.csv`

It also displays a Matplotlib/Contextily plot of clusters.

### `PathOptimization2.py`

This appears to be the current optimization script. It reads `data/cluster_info.csv`, uses cluster centroid coordinates and `Weight`, and searches for the highest-scoring route within `max_path_length = 6000` meters. The start and end point are both hard-coded as:

```python
np.array([62.465779, 6.401947])  # Vasstrandlia ramp
```

It writes `data/highscore_path.csv` with labels, sensitivities, longitude, latitude, and empty time values.

### `PathOptimization1.py`

This appears to be an older or prototype optimizer. It reads `data/Sampling_Priority.csv` directly and finds the shortest path through all raw points using brute-force permutations and Euclidean distance.

Important caveat: it writes `data/highscore_path.csv` with only:

```text
Latitude,Longitude
```

That schema is not compatible with the current plotters, which expect:

```text
label,sensitivity,longitude,latitude,time
```

So `PathOptimization1.py` should not be treated as interchangeable with `PathOptimization2.py` without adapting its output.

## Plotter Comparison

### Similar Core Inputs

The default/active plotting paths in `PathPlotter.py` and `PathPlotter2.py` use the same core files:

- `data/highscore_path.csv`
- `data/clustered_coordinates.csv`
- `data/cluster_info.csv`

Both can show the optimized path together with clustered sampling points and cluster weights.

### `PathPlotter.py`

`PathPlotter.py` is a multi-method plotting sandbox. It contains:

- `matplotllib_method(file_name)`
- `folium_method(file_name)`
- `plotly_method(file_name)`
- `animated_method(file_name)`

In its `__main__` block, only `plotly_method(input)` is currently active. The other calls are commented.

The active `plotly_method()` produces an interactive Plotly map in the browser. It includes:

- Optimized path points from `highscore_path.csv`
- Connecting path lines
- Clustered original points from `clustered_coordinates.csv`
- Cluster weights from `cluster_info.csv`

The other methods are not equivalent replacements:

- `matplotllib_method()` appears stale and likely broken because it uses `Basemap` without importing it.
- `folium_method()` plots route markers and lines, but does not overlay cluster points or cluster weights.
- `animated_method()` creates an animated route GIF and is a different output type. It currently reads with `sep=';'`, which does not match the comma-separated `highscore_path.csv` produced by `PathOptimization2.py`.

### `PathPlotter2.py`

`PathPlotter2.py` is simpler and more focused. Its `__main__` block calls:

```python
matplotlib_method_with_contextily(input)
```

It creates a static Matplotlib/Contextily map using:

- Optimized route from `highscore_path.csv`
- Original clustered points from `clustered_coordinates.csv`
- Cluster weights from `cluster_info.csv`

It saves:

- `data/clustered.png`

This appears to be the cleaner script for producing a static, publication-style figure.

## Conclusion

`PathPlotter.py::plotly_method()` and `PathPlotter2.py::matplotlib_method_with_contextily()` produce broadly similar figures in terms of data content: both combine the optimized path, original clustered points, and cluster weights. Their outputs differ mainly by medium:

- `PathPlotter.py` default: interactive Plotly browser map.
- `PathPlotter2.py` default: static high-resolution PNG.

The other plotting functions in `PathPlotter.py` are more fundamentally different or stale. They should be reviewed before use rather than assumed to be alternate implementations of the same final figure.
