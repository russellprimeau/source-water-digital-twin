"""Write the lake outline used as the background of the planning figures.

The outline is the boundary of the computational mesh: every edge that belongs to
one cell rather than two. It is derived from the grid geometry the water-quality
coupling already publishes, so it adds no data beyond what the repository holds and
needs no third-party shoreline product.

Writes data/sampling_plan/lake_outline_segments.csv with one segment per row as
x1, y1, x2, y2, which is the shape src/figures/make_fig9.py reshapes to (-1, 2, 2).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from netCDF4 import Dataset

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "sampling_plan" / "lake_outline_segments.csv"
# The published mesh geometry. Every coupling on the 4,935-cell mesh carries an
# identical one; the copies differ only in the metadata the solver stamps on them,
# so one file per discretization is published and this reads that.
DEFAULT_GRID = REPO / "data" / "transport_ensemble" / "geometry" / "waqgeom_fine40.nc"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--grid", type=Path, default=DEFAULT_GRID)
    args = ap.parse_args()

    ds = Dataset(args.grid)
    node_x = np.asarray(ds.variables["mesh2d_node_x"][:], dtype=float)
    node_y = np.asarray(ds.variables["mesh2d_node_y"][:], dtype=float)
    edge_nodes = np.asarray(ds.variables["mesh2d_edge_nodes"][:], dtype=int)
    edge_faces = np.ma.asarray(ds.variables["mesh2d_edge_faces"][:])

    start = int(edge_nodes.min())          # the file may be 0- or 1-based
    edge_nodes = edge_nodes - start

    # a boundary edge has a single adjoining cell: the other entry is absent or zero
    faces = np.ma.filled(edge_faces, 0).astype(int)
    on_boundary = (faces <= 0).sum(axis=1) == 1

    segs = np.column_stack([
        node_x[edge_nodes[on_boundary, 0]], node_y[edge_nodes[on_boundary, 0]],
        node_x[edge_nodes[on_boundary, 1]], node_y[edge_nodes[on_boundary, 1]],
    ])
    if len(segs) == 0:
        raise SystemExit(f"{args.grid}: no boundary edges found")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(segs, columns=["x1", "y1", "x2", "y2"]).to_csv(OUT, index=False)
    print(f"{len(edge_nodes)} edges, {on_boundary.sum()} on the boundary")
    print(f"  lon {segs[:, [0, 2]].min():.6f} .. {segs[:, [0, 2]].max():.6f}")
    print(f"  lat {segs[:, [1, 3]].min():.6f} .. {segs[:, [1, 3]].max():.6f}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
