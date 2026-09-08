"""
c.StabilityAnalysis.py

Stability of the sampling-plan result under resampling of the evidence.

Reviewer 2 observed that the model spread driving the sampling plan is computed
from only three alternative model configurations, and asked how stable the
resulting clusters and route are.  Adding further model runs is a separate piece
of work; what this script establishes instead is how sensitive the *downstream*
result -- the clustering and the selected route -- is to the particular set of
cells that entered it.

Three tests are run against the same inputs, clustering parameters and optimizer
used by a.PointSelection.py and b.PathOptimization2.py:

  1. Leave-one-out.  Each cell is dropped in turn and the analysis repeated.
     Reports how often the selected route changes.
  2. Bootstrap.  Cells are resampled with replacement and the analysis repeated.
     Reports the distribution over selected routes.
  3. Co-association.  Across bootstrap replicates, how often each pair of cells
     is assigned to the same cluster.  A cluster whose members always travel
     together is stable; one that fragments is not.

Writes data/validation/sampling_plan_stability.csv and prints a summary.

Note: this script deliberately does not import contextily, so it runs in
environments where the basemap dependency chain is unavailable.
"""

from __future__ import annotations

import itertools
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from geopy.distance import geodesic
from sklearn.cluster import DBSCAN

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
OUT_DIR = DATA_DIR / "validation"

SENSITIVITY_COLUMN = "Depth-averaged uncertainty"
EPS_METRES = 100.0
EARTH_RADIUS_M = 6_371_000.0
MAX_PATH_LENGTH_M = 6_000.0
LAUNCH_POINT = np.array([62.465779, 6.401947])  # Vasstrandlia ramp
N_BOOTSTRAP = 2_000
RANDOM_SEED = 20240401


def cluster_cells(frame: pd.DataFrame) -> pd.DataFrame:
    """Cluster cells exactly as a.PointSelection.py does, and return centroids."""
    coords = np.radians(frame[["Latitude", "Longitude"]].to_numpy(float))
    labels = DBSCAN(
        eps=EPS_METRES / EARTH_RADIUS_M, min_samples=1, metric="haversine"
    ).fit_predict(coords)
    work = frame.copy()
    work["cluster"] = labels
    return work.groupby("cluster").agg(
        Latitude=("Latitude", "mean"),
        Longitude=("Longitude", "mean"),
        Weight=(SENSITIVITY_COLUMN, "sum"),
    ).reset_index(), work


def best_route(clusters: pd.DataFrame) -> tuple[tuple[int, ...], float, float]:
    """Highest-scoring route within the distance budget.

    Mirrors highest_scoring_path() in b.PathOptimization2.py: maximise summed
    weight subject to the path-length constraint, breaking ties on shorter
    distance.  Returned as the tuple of visited cluster indices.
    """
    coords = np.vstack([LAUNCH_POINT, clusters[["Latitude", "Longitude"]].to_numpy(float), LAUNCH_POINT])
    weights = clusters["Weight"].to_numpy(float)
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = geodesic(coords[i], coords[j]).meters
            dist[i, j] = dist[j, i] = d

    best_score, best_len, best_order = -np.inf, np.inf, ()
    interior = range(1, n - 1)
    for r in range(1, n - 1):
        for combo in itertools.permutations(interior, r):
            path = (0,) + combo + (n - 1,)
            length = sum(dist[path[k], path[k + 1]] for k in range(len(path) - 1))
            if length > MAX_PATH_LENGTH_M:
                continue
            score = sum(weights[i - 1] for i in combo)
            if score > best_score or (score == best_score and length < best_len):
                best_score, best_len, best_order = score, length, combo
    # identify visited clusters by their centroid, order-independent
    visited = tuple(sorted(int(clusters.iloc[i - 1]["cluster"]) for i in best_order))
    return visited, best_score, best_len


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cells = pd.read_csv(DATA_DIR / "1.Sampling_Priority.csv")
    cells[SENSITIVITY_COLUMN] = cells[SENSITIVITY_COLUMN] / cells[SENSITIVITY_COLUMN].max()
    n_cells = len(cells)

    base_clusters, base_assign = cluster_cells(cells)
    base_route, base_score, base_len = best_route(base_clusters)
    print(f"Baseline: {n_cells} cells -> {len(base_clusters)} clusters")
    print(f"  cluster weights: {np.round(base_clusters['Weight'].to_numpy(float), 4).tolist()}")
    print(f"  selected clusters: {base_route}  score={base_score:.4f}  length={base_len:.0f} m")

    # --- 1. leave-one-out --------------------------------------------------
    loo_same_route = 0
    loo_same_count = 0
    loo_routes: Counter = Counter()
    for drop in range(n_cells):
        sub = cells.drop(cells.index[drop])
        cl, _ = cluster_cells(sub)
        route, _, _ = best_route(cl)
        loo_routes[route] += 1
        loo_same_route += int(route == base_route)
        loo_same_count += int(len(cl) == len(base_clusters))
    print(f"\nLeave-one-out over {n_cells} cells:")
    print(f"  same cluster count : {loo_same_count}/{n_cells} ({100*loo_same_count/n_cells:.1f}%)")
    print(f"  same selected route: {loo_same_route}/{n_cells} ({100*loo_same_route/n_cells:.1f}%)")

    # --- 2. bootstrap ------------------------------------------------------
    rng = np.random.default_rng(RANDOM_SEED)
    boot_routes: Counter = Counter()
    boot_ncluster: Counter = Counter()
    co = np.zeros((n_cells, n_cells))
    together = np.zeros((n_cells, n_cells))
    for _ in range(N_BOOTSTRAP):
        idx = rng.integers(0, n_cells, n_cells)
        sub = cells.iloc[idx].reset_index(drop=True)
        cl, assign = cluster_cells(sub)
        route, _, _ = best_route(cl)
        boot_routes[route] += 1
        boot_ncluster[len(cl)] += 1
        lab = assign["cluster"].to_numpy()
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                together[i, j] += 1
                together[j, i] += 1
                if lab[a] == lab[b]:
                    co[i, j] += 1
                    co[j, i] += 1

    print(f"\nBootstrap ({N_BOOTSTRAP} replicates):")
    print("  cluster count distribution:")
    for k in sorted(boot_ncluster):
        print(f"    {k} clusters: {100*boot_ncluster[k]/N_BOOTSTRAP:5.1f}%")
    print("  most frequent selected cluster sets:")
    for route, count in boot_routes.most_common(5):
        marker = "  <-- baseline" if route == base_route else ""
        print(f"    {str(route):24s} {100*count/N_BOOTSTRAP:5.1f}%{marker}")

    # --- 3. co-association by baseline cluster ------------------------------
    with np.errstate(invalid="ignore", divide="ignore"):
        frac = np.where(together > 0, co / np.maximum(together, 1), np.nan)
    base_lab = base_assign["cluster"].to_numpy()
    rows = []
    print("\nCo-association within each baseline cluster:")
    for c in sorted(set(base_lab)):
        members = np.where(base_lab == c)[0]
        if len(members) < 2:
            rows.append(dict(cluster=int(c), n_cells=len(members), mean_co_association=np.nan))
            print(f"  cluster {c}: {len(members)} cell (singleton, not assessable)")
            continue
        vals = [frac[i, j] for i, j in itertools.combinations(members, 2) if np.isfinite(frac[i, j])]
        mean_co = float(np.mean(vals)) if vals else float("nan")
        rows.append(dict(cluster=int(c), n_cells=len(members), mean_co_association=mean_co))
        print(f"  cluster {c}: {len(members):2d} cells, mean co-association {mean_co:.3f}")

    out = pd.DataFrame(rows)
    out["baseline_weight"] = [
        float(base_clusters.loc[base_clusters["cluster"] == c, "Weight"].iloc[0]) for c in out["cluster"]
    ]
    out["in_selected_route"] = [int(c in base_route) for c in out["cluster"]]
    out.to_csv(OUT_DIR / "sampling_plan_stability.csv", index=False)
    print(f"\nWritten: {OUT_DIR / 'sampling_plan_stability.csv'}")


if __name__ == "__main__":
    main()
