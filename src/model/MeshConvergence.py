"""Solute-transport convergence of the contamination scenario.

The model-configuration comparison examined how the hydrodynamic solution responds to mesh
resolution. That is a different question from whether the transport of a released
constituent has converged, and it is the second question the scenario results rest
on. This script answers it by carrying one release on four couplings that differ only
in discretization: two horizontal meshes crossed with two vertical resolutions.

Fields on different meshes have no cell-by-cell correspondence, so the comparison is
made on quantities that do not depend on the discretization: the depth-averaged
concentration in the water column at each monitoring point, which is a fixed
geographic location, and the whole-domain mass balance.

The obvious comparison, the station history files, is the wrong one. Those are written
for a single segment, the surface layer, and that layer is twice as thick when the
layer count is halved. A release that stays near the surface is then averaged over
twice the depth, and the reported concentration falls by about half, for reasons that
have nothing to do with whether the transport has converged. Comparing surface values
across vertical resolutions compares two different sampling volumes.

Usage:
    .venv/Scripts/python src/model/MeshConvergence.py
    .venv/Scripts/python src/model/MeshConvergence.py --extract --runs-dir PATH
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src'))
import external_runs                                                     # noqa: E402
OUT = REPO / "data" / "transport_ensemble" / "mesh_convergence.csv"

SUBSTANCE = "cTR1"
RELEASED_G = 3600.0            # 1.0 g/s for one hour
# Fixed geographic locations, as (latitude, longitude). The release cell and its
# neighbour hold most of the release and are governed by the cell footprint, which
# genuinely differs between meshes; the downstream points are where convergence of
# the transport is actually tested.
STATIONS = {
    "Source": (62.468821, 6.390936),
    "Spjelkavikelva": (62.466005, 6.388955),
    "Vasstrandlia": (62.471035, 6.417630),
    "Profiler": (62.474425, 6.461499),
}
# FarField is excluded: within this window it holds around 1e-10 g/m3, so ratios
# between cases there are dominated by single-precision noise.

# tag, horizontal cells, vertical layers
CASES = [
    ("fine40", 4935, 40),
    ("fine20", 4935, 20),
    ("coarse40", 2603, 40),
    ("coarse20", 2603, 20),
]


KMLON = 111000.0 * np.cos(np.radians(62.47))


def read_columns(runs, tag):
    """Depth-averaged and surface concentration at each station, from the map file."""
    path = runs / f"Convergence_{tag}" / "output" / "WAQ" / f"convergence_{tag}_map.nc"
    ds = Dataset(path)
    fx = np.asarray(ds.variables["mesh2d_face_x"][:], dtype=float)
    fy = np.asarray(ds.variables["mesh2d_face_y"][:], dtype=float)
    conc = np.asarray(ds.variables[f"mesh2d_{SUBSTANCE}"][:], dtype=float)
    vol = np.asarray(ds.variables["mesh2d_volume"][:], dtype=float)

    out = {}
    for name, (lat, lon) in STATIONS.items():
        i = int(np.hypot((fx - lon) * KMLON, (fy - lat) * 111000.0).argmin())
        c, v = conc[:, :, i], vol[:, :, i]
        column = v.sum(axis=1)
        # Volume-weighted mean over the water column: the same physical quantity
        # whatever the layer count, unlike the concentration in the top layer.
        depth_avg = np.where(column > 0, (c * v).sum(axis=1) / np.maximum(column, 1e-30),
                             0.0)
        out[name] = {"surface": c[:, 0].max(), "depth_avg": depth_avg.max()}
    return out


def read_balance(runs, tag):
    """Whole-domain budget for the conservative tracer, from the monitor file.

    DELWAQ writes one block per reporting interval, and the load, inflow and outflow
    lines in a block are that interval's changes rather than running totals: at the
    end of a block, mass = mass at its start + loads + inflows - outflows + processes.
    Closing the budget over the run therefore means accumulating those terms and
    comparing the total against the final mass. Taking the last block's numbers alone
    would compare a whole-run mass against one interval's outflow.

    Returns (final mass, cumulative loads, cumulative outflows, residual), all in g,
    for the first substance in the input.
    """
    path = runs / f"Convergence_{tag}" / "output" / "WAQ" / f"convergence_{tag}.mon"
    if not path.exists():
        return None
    first = lambda line: float(re.findall(r"-?\d\.\d+E[+-]\d+", line)[0])  # noqa: E731

    mass = 0.0
    loads = inflow = outflow = process = 0.0
    for line in path.read_text(errors="replace").splitlines():
        if "TOTAL MASS IN SYSTEM" in line:
            mass = first(line)
        elif "CHANGES BY LOADS" in line:
            loads += first(line)
        elif "CHANGES BY PROCESSES" in line:
            process += first(line)
        elif "BOUNDARY INFLOWS" in line:
            inflow += first(line)
        elif "BOUNDARY OUTFLOWS" in line:
            outflow += first(line)
    residual = mass - (loads + inflow - outflow + process)
    return mass, loads, outflow, residual


RELEASE_TABLE = REPO / "output" / "release_balance_table.tex"
CONVERGENCE_TABLE = REPO / "output" / "convergence_table.tex"
# The case whose discretization the scenario simulation uses; its budget is the
# release balance the article reports on its own.
REPORTED_CASE = "fine20"


def write_tables(table):
    """Emit the two tabulars the appendices read, from the committed table.

    Both carry the whole tabular rather than only its rows, because \\input inside
    a tabularx upsets the alignment.
    """
    eol = chr(92) * 2
    row = table.set_index("case").loc[REPORTED_CASE]
    load, out, final = row["loads_g"], row["outflow_g"], row["final_mass_g"]
    residual = final - (load - out)

    lines = [f"% Generated by {Path(__file__).name}; do not edit by hand.",
             r"    \footnotesize",
             r"    \begin{tabularx}{\textwidth}{@{}l r@{}}",
             r"    \toprule",
             r"        \textbf{Term} & \textbf{Released tracer (g N)} " + eol,
             r"    \midrule",
             f"        Initial stock in domain & 0.0 {eol}",
             f"        Applied load & $+{load:,.1f}$ {eol}".replace(",", "{,}"),
             f"        Boundary outflow & $-{out:,.1f}$ {eol}".replace(",", "{,}"),
             f"        Final stock in domain & {final:,.1f} {eol}",
             r"    \midrule",
             f"        Residual (unaccounted) & {abs(residual):.2f} {eol}",
             f"        Residual / applied load & {row['residual_ppm']:.0f}~ppm {eol}",
             r"    \bottomrule",
             r"    \end{tabularx}"]
    RELEASE_TABLE.parent.mkdir(parents=True, exist_ok=True)
    RELEASE_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = [f"% Generated by {Path(__file__).name}; do not edit by hand.",
             r"    \footnotesize",
             r"    \begin{tabularx}{\textwidth}{@{}c c r r r r r r@{}}",
             r"    \toprule",
             r"        \textbf{Cells} & \textbf{Layers} & \textbf{Source} & "
             r"\textbf{Spjelkavik-} & \textbf{Vasstrand-} & \textbf{Profiler} & "
             r"\textbf{Retained} & \textbf{Residual} " + eol,
             r"        & & & \textbf{elva} & \textbf{lia} & & \textbf{(\%)} & "
             r"\textbf{(ppm)} " + eol,
             r"    \midrule"]
    for _, r in table.iterrows():
        cells = [f"{r['cells']:,}", f"{r['layers']:.0f}"]
        for s in STATIONS:                       # micrograms per cubic metre
            v = r[f"depthavg_{s}"] * 1e6
            # Three significant figures across four orders of magnitude.
            cells.append(f"{v:,.0f}" if v >= 100 else
                         f"{v:.1f}" if v >= 10 else f"{v:.2f}")
        cells += [f"{r['retained_pct']:.1f}", f"{r['residual_ppm']:.1f}"]
        lines.append("        " + " & ".join(cells) + f" {eol}")
    lines += [r"    \bottomrule", r"    \end{tabularx}"]
    CONVERGENCE_TABLE.parent.mkdir(parents=True, exist_ok=True)
    CONVERGENCE_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {RELEASE_TABLE.relative_to(REPO)} and "
          f"{CONVERGENCE_TABLE.relative_to(REPO)}")


def extract(runs):
    """Reduce the four solver records to the committed table."""
    rows = []
    for tag, cells, layers in CASES:
        try:
            cols = read_columns(runs, tag)
        except (FileNotFoundError, OSError):
            print(f"{tag}: no output; skipped")
            continue
        bal = read_balance(runs, tag)
        row = {"case": tag, "cells": cells, "layers": layers}
        for s, vals in cols.items():
            row[f"depthavg_{s}"] = vals["depth_avg"]
            row[f"surface_{s}"] = vals["surface"]
        if bal:
            mass, loads, outflow, residual = bal
            row["final_mass_g"] = mass
            row["loads_g"] = loads
            row["outflow_g"] = outflow
            row["retained_pct"] = 100.0 * mass / RELEASED_G
            # How far the budget fails to close, relative to what was released.
            row["residual_ppm"] = 1e6 * residual / RELEASED_G
        rows.append(row)

    if not rows:
        raise SystemExit("no convergence runs found")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"wrote {OUT.relative_to(REPO)}")


def main() -> int:
    if "--extract" in sys.argv:
        extract(external_runs.resolve(external_runs.argv_option(sys.argv)))
    if not OUT.exists():
        raise SystemExit(
            f"missing {OUT.relative_to(REPO)}; run with --extract to rebuild it from "
            "the solver output, which is not published")
    table = pd.read_csv(OUT)
    write_tables(table)
    rows = table.to_dict("records")
    pd.set_option("display.width", 220)
    print("Peak depth-averaged concentration at each monitoring point, g/m3\n")
    print(table[["case", "cells", "layers"] + [f"depthavg_{s}" for s in STATIONS]]
          .to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print("\nPeak surface-layer concentration at the same points, g/m3 -- shown to "
          "make the\nsampling-volume effect visible, not as a convergence measure\n")
    print(table[["case", "cells", "layers"] + [f"surface_{s}" for s in STATIONS]]
          .to_string(index=False, float_format=lambda v: f"{v:.4g}"))

    if "final_mass_g" in table:
        print(f"\nWhole-domain budget for {SUBSTANCE}, against {RELEASED_G:.0f} g "
              "released\n")
        print(table[["case", "cells", "layers", "loads_g", "outflow_g", "final_mass_g",
                     "retained_pct", "residual_ppm"]]
              .to_string(index=False, float_format=lambda v: f"{v:.4g}"))

    # Pairwise differences isolating one axis of refinement at a time
    print("\nEffect of refinement, as a relative difference in the station peaks")
    pairs = [("coarse40", "fine40", "horizontal, at 40 layers"),
             ("coarse20", "fine20", "horizontal, at 20 layers"),
             ("fine20", "fine40", "vertical, on the fine mesh"),
             ("coarse20", "coarse40", "vertical, on the coarse mesh")]
    have = {r["case"] for r in rows}
    indexed = table.set_index("case")
    for prefix, what in (("depthavg", "depth-averaged"), ("surface", "surface layer")):
        print(f"  on the {what} concentration:")
        for a, b, label in pairs:
            if a not in have or b not in have:
                continue
            ta, tb = indexed.loc[a], indexed.loc[b]
            diffs = [abs(ta[f"{prefix}_{s}"] - tb[f"{prefix}_{s}"])
                     / max(abs(tb[f"{prefix}_{s}"]), 1e-30)
                     for s in STATIONS if f"{prefix}_{s}" in table]
            if diffs:
                print(f"    {label:30s} median {np.median(diffs):7.1%}   "
                      f"max {max(diffs):7.1%}")

    print(f"\nread {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
