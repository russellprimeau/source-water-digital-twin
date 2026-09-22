# Sampling plan

Inputs and outputs for Figure 9, the stability analysis in Appendix G, and the
clustering-radius analysis in Table A10.

| File | Contents |
| --- | --- |
| `1.Sampling_Priority.csv` | The 60 retained cells and their model-spread scores from the transport ensemble. |
| `2.clustered_coordinates.csv` | Retained cells with cluster labels and scores normalized by the maximum retained score. |
| `3.cluster_info.csv` | Cluster centroids and weights (sums of normalized cell scores). |
| `4.highscore_path.csv` | Route waypoints in visit order, with cluster weights. The starting and ending launch-point rows have zero weight. |
| `sampling_plan_stability.csv`, `sampling_route_frequencies.csv`, `sampling_stability_summary.json` | Stability-analysis summaries. |
| `cluster_radius_sweep.csv`, `score_semivariogram.csv` | Clustering-radius sweep and score semivariogram. |
| `lake_outline_segments.csv` | Shoreline segments derived from the mesh boundary for Figures 7 and 9. |
| `clusters_diagnostic.png` | Clustering diagnostic, not used in the article. |

Follow the [sampling commands](../../README.md#sampling-plan) to regenerate these
files. `BuildSamplingPriority.py` selects the cells, `a.PointSelection.py` clusters
them, and `b.PathOptimization2.py` computes the route. `make_fig9.py` draws the figure.
The stability and radius analyses use the retained cells and, for the radius
analysis, the ensemble score field; they do not depend on each other's outputs.

[route_solver.py](../../src/PathPlanning/route_solver.py) defines the distance
budget, clustering radius, and launch point.
[ExportLakeOutline.py](../../src/model/ExportLakeOutline.py) regenerates the shoreline.
