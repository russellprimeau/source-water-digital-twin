"""What the clustering neighbourhood is worth, and where its value comes from.

The retained cells are grouped before they are routed, so that a mission does not
spend its budget visiting three cells forty metres apart. The neighbourhood that
grouping uses needs a stated basis, and its effect on the plan needs reporting.

Two things are computed here.

The semivariogram of the score field. The neighbourhood ought to be the distance over
which the score stays effectively constant, because two cells that close are the same
sampling target: one profile answers for both. That distance is a property of the
field, not a preference, and the empirical semivariogram measures it.

The sweep. Grouping at a radius and then routing under the distance budget gives a
plan; doing it across a range of radii shows what the choice actually decides. It
turns out to decide how finely the mission is divided rather than where it goes.

Both read published files only. The score field comes from the ensemble precursor that
src/model/BuildSamplingPriority.py writes, and the launch point and distance budget come
from route_solver, so this script and the reported plan cannot disagree.

Usage:
    .venv/Scripts/python src/PathPlanning/ClusterRadius.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from geopy.distance import geodesic
from netCDF4 import Dataset
from sklearn.cluster import DBSCAN

sys.path.insert(0, str(Path(__file__).resolve().parent))
import route_solver                                                      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SPREAD_FILE = ROOT / "data" / "transport_ensemble" / "ensemble" / "spread_by_horizon.nc"
RETAINED = ROOT / "data" / "sampling_plan" / "1.Sampling_Priority.csv"
OUT_DIR = ROOT / "data" / "sampling_plan"

# The horizon the article evaluates, in days after the release.
HORIZON_DAYS = 6.0
# Matches src/model/BuildSamplingPriority.py; cells below it have negligible predicted signal for this analysis.
MODEL_SIGNAL_FRACTION = 1e-3
# Radii swept, in metres, spanning from well inside the mesh spacing to well beyond
# the separation of the retained patches.
RADII = (40, 50, 60, 75, 100, 125, 150, 200, 250, 300)
# Lag bins for the semivariogram, in metres.
LAG_STEP, LAG_MAX = 25.0, 1600.0
# Pairs are drawn from a sample of the eligible cells; the full set would be
# six million pairs for no gain in the answer.
SAMPLE, SEED = 2000, 1

LAT0 = 62.47
KMLON = 111320.0 * np.cos(np.deg2rad(LAT0))


def score_field():
    """Ranked score and cell coordinates at the evaluation horizon."""
    if not SPREAD_FILE.exists():
        raise SystemExit(
            f"missing {SPREAD_FILE.relative_to(ROOT)}; build it with "
            "src/model/BuildSamplingPriority.py --extract")
    with Dataset(SPREAD_FILE) as ds:
        fx = np.asarray(ds.variables["face_x"][:], dtype=float)
        fy = np.asarray(ds.variables["face_y"][:], dtype=float)
        hours = np.asarray(ds.variables["time"][:], dtype=float)
        idx = int(np.argmin(np.abs(hours - HORIZON_DAYS * 24.0)))
        sigma = np.asarray(ds.variables["sigma"][idx], dtype=float)
        cell_mean = np.asarray(ds.variables["cell_mean"][idx], dtype=float)
    ranked = np.where(cell_mean >= MODEL_SIGNAL_FRACTION * cell_mean.max(), sigma, np.nan)
    return ranked, fx, fy, hours[idx] / 24.0


def semivariogram(values, lon, lat):
    """Empirical semivariance by lag, normalised by the field's variance.

    Half the mean squared difference between pairs of cells a given distance apart.
    Where that is small relative to the sill, the field has barely changed over the
    separation, so the two cells are interchangeable as sampling targets.
    """
    rng = np.random.default_rng(SEED)
    take = rng.choice(len(values), min(SAMPLE, len(values)), replace=False)
    x, y, v = lon[take] * KMLON, lat[take] * 111320.0, values[take]
    d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
    g = 0.5 * (v[:, None] - v[None, :]) ** 2
    iu = np.triu_indices(len(v), 1)
    d, g, sill = d[iu], g[iu], float(np.var(v))

    rows = []
    edges = np.arange(0.0, LAG_MAX + LAG_STEP, LAG_STEP)
    for lo, hi in zip(edges[:-1], edges[1:]):
        keep = (d >= lo) & (d < hi)
        if keep.sum() < 30:
            continue
        rows.append({"lag_lower_m": lo, "lag_upper_m": hi, "pairs": int(keep.sum()),
                     "semivariance": float(g[keep].mean()),
                     "fraction_of_sill": float(g[keep].mean() / sill)})
    return pd.DataFrame(rows), sill


def reaches(frame, fraction):
    """Mid-lag at which the semivariance first reaches a fraction of the sill."""
    hit = frame[frame["fraction_of_sill"] >= fraction]
    if hit.empty:
        return float("nan")
    row = hit.iloc[0]
    return 0.5 * (row["lag_lower_m"] + row["lag_upper_m"])


def group(lon, lat, radius_m):
    return DBSCAN(eps=radius_m / route_solver.EARTH_RADIUS_M, min_samples=1,
                  metric="haversine").fit_predict(
        np.radians(np.column_stack([lat, lon])))


def plan(lon, lat, weight, labels):
    """Cluster centroids, their weights, and the best route within the budget."""
    keys = sorted(set(labels))
    centroids = [(lat[labels == k].mean(), lon[labels == k].mean()) for k in keys]
    weights = np.array([weight[labels == k].sum() for k in keys])
    points = [route_solver.LAUNCH_POINT] + centroids + [route_solver.LAUNCH_POINT]
    matrix = np.array([[geodesic(a, b).meters for b in points] for a in points])
    order, total, length = route_solver.solve(matrix, weights,
                                              route_solver.MAX_PATH_LENGTH_M)
    return keys, centroids, weights, order, total, length


def spans(lon, lat, labels):
    """Greatest distance between two cells in the same group, per group."""
    x, y = lon * KMLON, lat * 111320.0
    out = {}
    for k in sorted(set(labels)):
        px, py = x[labels == k], y[labels == k]
        out[k] = (0.0 if len(px) < 2
                  else float(np.hypot(px[:, None] - px[None, :],
                                      py[:, None] - py[None, :]).max()))
    return out


def main() -> int:
    ranked, fx, fy, days = score_field()
    ok = np.isfinite(ranked)
    print(f"score field at {days:.2f} days after the release: "
          f"{int(ok.sum())} of {len(ranked)} cells above the model-signal threshold")

    vario, sill = semivariogram(ranked[ok], fx[ok], fy[ok])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    vario.to_csv(OUT_DIR / "score_semivariogram.csv", index=False)
    eps = route_solver.CLUSTER_EPS_M
    at_eps = vario[(vario["lag_lower_m"] <= eps) & (vario["lag_upper_m"] > eps)]
    print(f"semivariogram: sill {sill:.5f}; "
          f"{float(at_eps['fraction_of_sill'].iloc[0]):.2f} of it at {eps:.0f} m; "
          f"a quarter at {reaches(vario, 0.25):.0f} m; "
          f"half at {reaches(vario, 0.5):.0f} m; "
          f"range (95% of sill) at {reaches(vario, 0.95):.0f} m")

    cells = pd.read_csv(RETAINED)
    lon = cells["Longitude"].to_numpy()
    lat = cells["Latitude"].to_numpy()
    weight = cells["Model-spread score"].to_numpy()
    weight = weight / weight.max()

    print(f"\n{'radius':>7s} {'groups':>7s} {'stations':>9s} {'widest group':>13s} "
          f"{'route':>22s} {'length':>8s} {'score':>7s}")
    rows = []
    for radius in RADII:
        labels = group(lon, lat, radius)
        keys, _, weights, order, total, length = plan(lon, lat, weight, labels)
        widest = max(spans(lon, lat, labels).values())
        visited = "-".join(chr(64 + i) for i in order)
        rows.append({"radius_m": radius, "groups": len(keys), "stations": len(order),
                     "widest_group_m": round(widest), "route": visited,
                     "length_m": round(length, 1), "score": round(total, 4)})
        print(f"{radius:7d} {len(keys):7d} {len(order):9d} {widest:11.0f} m "
              f"{visited:>22s} {length:7.0f} m {total:7.2f}")
    pd.DataFrame(rows).to_csv(OUT_DIR / "cluster_radius_sweep.csv", index=False)

    labels = group(lon, lat, eps)
    by_group = spans(lon, lat, labels)
    sizes = {k: int((labels == k).sum()) for k in by_group}
    multi = [f"{chr(65 + k)} {sizes[k]} cells spanning {by_group[k]:.0f} m"
             for k in sorted(by_group) if sizes[k] > 1]
    print(f"\nat the reported {eps:.0f} m: " + "; ".join(multi)
          + f"; {sum(1 for k in sizes if sizes[k] == 1)} single-cell groups")
    print(f"\nwrote {(OUT_DIR / 'score_semivariogram.csv').relative_to(ROOT)} "
          f"and {(OUT_DIR / 'cluster_radius_sweep.csv').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
