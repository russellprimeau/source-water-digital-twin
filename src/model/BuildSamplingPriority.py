"""Build the sampling-plan input from the contamination scenario's model ensemble.

Writes data/sampling_plan/1.Sampling_Priority.csv, the retained set of highest-scoring cells that
src/PathPlanning/a.PointSelection.py clusters and b.PathOptimization2.py routes.

The score is Equation (8) of the manuscript: for each horizontal cell, the arithmetic
mean over that cell's layers of the standard deviation across members of the predicted
concentration in that layer. It measures how far the alternatives diverge from one
another at a location, and is used only to rank locations against each other.

Every member releases the same nitrogen at the same cell and hour, and differs in the
hydrodynamic solution that carries it. That is what gives the field spatial structure.
Alternatives sharing one flow solution and differing only in the reaction applied to
the released material cannot serve: their spread is then a pointwise function of the
concentration field, so its largest values always fall in the single patch around the
release, wherever that patch happens to be, and the retained cells carry no
information about where a mission should go. The reaction treatments are compared
separately, over the same release, in the scenario results.

Two choices are recorded here rather than left implicit.

Membership. The model-configuration comparison explored vertical diffusivities from 1e-6 to
1e-3. Members are the five configurations whose seasonal temperature RMSE lies within
a factor of two of the best, 1.11 to 2.12 degC; the two at 1e-3 diffusivity score 2.91
and were not carried forward. Sensitivity of the retained set to the number of members
is reported, since that is what a reader needs in order to judge whether five is
enough.

Evaluation time. A fixed horizon after the release, not a time chosen from the
results. The default is seven days, the horizon at which a survey mounted in response
to a reported spill could realistically be in the water, and early enough that the
release is still distinguishable from a uniform background.

The ensemble fields themselves are five large solver files and are not published.
What is published is the pair of precursors under data/transport_ensemble/ensemble, which this
script reads by default and rebuilds with --extract.

Usage:
    .venv/Scripts/python src/model/BuildSamplingPriority.py
    .venv/Scripts/python src/model/BuildSamplingPriority.py --days 14 --dry-run
    .venv/Scripts/python src/model/BuildSamplingPriority.py --days 6 --extract --runs-dir PATH
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
from sklearn.cluster import DBSCAN

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "sampling_plan" / "1.Sampling_Priority.csv"

# Published precursors. Between them they carry everything the score, the horizon
# sweep and the member-count sensitivity need, reduced from the five solver fields
# so that this script and the figures below it run from the repository alone.
ARCHIVE = REPO / "data" / "transport_ensemble" / "ensemble"
SPREAD_FILE = ARCHIVE / "spread_by_horizon.nc"
MEMBER_FILE = ARCHIVE / "tracer_members.nc"

# The solver run tree --extract rebuilds those two files from. It is outside the
# repository and is not published, so it is named on the command line rather than
# here; see the module docstring.
sys.path.insert(0, str(REPO / "src"))
import external_runs                                                     # noqa: E402

# The conservative tracer: the released nitrogen with no reaction applied, so that the
# spread among members reflects transport alone.
VARIABLE = "mesh2d_cTR1"
RELEASE = pd.Timestamp("2024-08-01 04:00")
N_RETAINED = 60
# Cells whose ensemble-mean concentration falls below this fraction of the largest
# are not ranked: there is nothing there to measure, and the relative score is
# unbounded where the mean approaches zero.
MODEL_SIGNAL_FRACTION = 1e-3
# The DBSCAN neighbourhood, in metres. Held with the distance budget in the planning
# package, so the diagnostic cluster counts printed here cannot drift from the ones
# a.PointSelection.py actually produces.
sys.path.insert(0, str(REPO / "src" / "PathPlanning"))
import route_solver                                                      # noqa: E402
CLUSTER_EPS_M = route_solver.CLUSTER_EPS_M

# The model-configuration comparison record, from which the mixing settings and the
# seasonal RMSE of every candidate are read rather than transcribed.
COMPARISON = REPO / "data" / "configuration_comparison" / "calibration.csv"
ENSEMBLE_TABLE = REPO / "output" / "ensemble_table.tex"

# The seven configurations that carry the release: short name used by the run
# directories, the label they appear under in the comparison record, and the name the
# article prints. They share the mesh, the layer count and the simulated period, so
# their RMSE values are comparable with one another.
CANDIDATES = [
    ("vico6dico5", "40high_Vico6Dico5", "Vico6Dico5"),
    ("vicdic5", "40 Layer High Res VicoDicoww5", "VicoDicoww5"),
    ("novfilt", "40 Layer Full Season High Res noVfilter", "noVfilter"),
    ("base", "40 Layer Full Season High Res", "Base"),
    ("dico4", "40 Layer High Res Dicoww4", "Dicoww4"),
    ("vicdic3", "40 Layer High Res VicoDicoww3", "VicoDicoww3"),
    ("dico3", "40 Layer High Res Dicoww3", "Dicoww3"),
]
# A candidate joins the ensemble if its seasonal RMSE is within this factor of the
# best among the candidates. The comparison is among these seven and not across the
# whole comparison, because the shorter runs accumulate error over a
# different window and their RMSE is not comparable with a full season's.
QUALIFYING_FACTOR = 2.0


def candidates():
    """The seven, with their settings and RMSE from the comparison record."""
    table = pd.read_csv(COMPARISON, sep=";", encoding="utf-8-sig")
    table["Label"] = table["Label"].astype(str).str.strip()
    indexed = table.set_index("Label")
    rows = []
    for short, label, display in CANDIDATES:
        if label not in indexed.index:
            raise SystemExit(f"{COMPARISON.name}: no row labelled {label!r}")
        r = indexed.loc[label]
        rows.append({
            "short": short, "display": display,
            "vico": float(r["Vicoww"]), "dico": float(r["Dicoww"]),
            "filter": bool(int(r["VFF?"])),
            "rmse": float(r["Root Mean Squared Error"]),
        })
    rows.sort(key=lambda d: d["rmse"])
    cut = QUALIFYING_FACTOR * rows[0]["rmse"]
    for row in rows:
        row["member"] = row["rmse"] <= cut
    return rows, cut


def write_ensemble_table(rows, cut):
    """Emit the rows of Table A7, so it cannot drift from the comparison record."""
    eol = chr(92) * 2                      # a LaTeX row terminator

    def power(value):
        return f"$10^{{{round(np.log10(value))}}}$"

    # The whole tabular is generated, not just its rows: \input inside a tabularx
    # upsets the alignment, and keeping the column specification beside the rows
    # means the two cannot disagree about how many columns there are.
    lines = [f"% Generated by {Path(__file__).name}; do not edit by hand.",
             f"% Qualifying threshold {cut:.4f} degC "
             f"= {QUALIFYING_FACTOR:g} x the best of {len(rows)} candidates.",
             r"    \footnotesize",
             r"    \begin{tabularx}{\textwidth}{@{}l c c c r c@{}}",
             r"    \toprule",
             r"        \textbf{Configuration} & \textbf{Vertical} & \textbf{Vertical} "
             r"& \textbf{Vertical} & \textbf{RMSE} & \textbf{In} " + eol,
             r"        & \textbf{viscosity} & \textbf{diffusivity} & \textbf{filter} "
             r"& \textbf{($^{\circ}$C)} & \textbf{ensemble} " + eol,
             r"        & (m\textsuperscript{2}/s) & (m\textsuperscript{2}/s) & & & " + eol,
             r"    \midrule"]
    for r in rows:
        lines.append(
            f"        {r['display']:<15s} & {power(r['vico']):<9s} & "
            f"{power(r['dico']):<9s} & {'on' if r['filter'] else 'off':<3s} & "
            f"{r['rmse']:.3f} & {'yes' if r['member'] else 'no'} {eol}")
    lines += [r"    \bottomrule", r"    \end{tabularx}"]
    ENSEMBLE_TABLE.parent.mkdir(parents=True, exist_ok=True)
    ENSEMBLE_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    kept = sum(1 for r in rows if r["member"])
    print(f"wrote {ENSEMBLE_TABLE.relative_to(REPO)} "
          f"({kept} of {len(rows)} within {cut:.3f} degC)")


def describe_member(row):
    text = f"Vicoww {row['vico']:g}, Dicoww {row['dico']:g}"
    return text if row["filter"] else text + ", no vertical filter"


_CANDIDATE_ROWS, _QUALIFYING_RMSE = candidates()
# short name, hydrodynamic configuration, seasonal temperature RMSE
MEMBERS = [(r["short"], describe_member(r), r["rmse"])
           for r in _CANDIDATE_ROWS if r["member"]]


def open_solver(runs):
    """The five full solver fields. Only --extract needs these."""
    handles, fx, fy, times = {}, None, None, None
    for short, _, _ in MEMBERS:
        path = (runs / f"Transport_{short}" / "output" / "WAQ"
                / f"transport_{short}_map.nc")
        if not path.exists():
            raise SystemExit(f"missing {path}")
        ds = Dataset(path)
        handles[short] = ds
        if fx is None:
            fx = np.asarray(ds.variables["mesh2d_face_x"][:], dtype=float)
            fy = np.asarray(ds.variables["mesh2d_face_y"][:], dtype=float)
            tv = ds.variables["nTimesDlwq"]
            times = [pd.Timestamp(num2date(v, tv.units).isoformat()) for v in tv[:]]
        elif len(ds.dimensions["mesh2d_nFaces"]) != len(fx):
            raise SystemExit(f"{short}: mesh differs from the first member")
    return handles, fx, fy, times


def extract(runs, idx):
    """Reduce the solver fields to the two published files.

    The spread file carries the score and the ensemble mean at every output time,
    which is what the horizon sweep and any choice of model-signal threshold need: the
    threshold is applied to the mean, so it can be moved without the members. The
    member file carries the per-member layered tracer at one horizon only, which
    is what recomputing the score from a subset of members needs. Keeping every
    member at every horizon would cost an order of magnitude more, for a comparison
    the article
    reports at one time, so the horizon is a parameter of the extraction.
    """
    handles, fx, fy, times = open_solver(runs)
    names = [m[0] for m in MEMBERS]
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    sigma = np.empty((len(times), len(fx)), dtype=np.float64)
    cell_mean = np.empty_like(sigma)
    for i in range(len(times)):
        s, m = spread([member_field(handles, n, i) for n in names])
        sigma[i], cell_mean[i] = s, m

    with Dataset(SPREAD_FILE, "w", format="NETCDF4") as ds:
        ds.title = "Across-member spread of the released tracer, by horizon"
        ds.source = f"{len(names)} transport-ensemble members: {', '.join(names)}"
        ds.release = str(RELEASE)
        ds.createDimension("time", len(times))
        ds.createDimension("face", len(fx))
        t = ds.createVariable("time", "f8", ("time",))
        t.units = "hours since " + str(RELEASE)
        t[:] = [(x - RELEASE).total_seconds() / 3600.0 for x in times]
        for name, values, units in (("face_x", fx, "degrees_east"),
                                    ("face_y", fy, "degrees_north")):
            v = ds.createVariable(name, "f8", ("face",))
            v.units = units
            v[:] = values
        v = ds.createVariable("sigma", "f8", ("time", "face"), zlib=True, complevel=4)
        v.long_name = "layer mean of the across-member standard deviation over the mean"
        v[:] = sigma
        v = ds.createVariable("cell_mean", "f8", ("time", "face"), zlib=True, complevel=4)
        v.long_name = "layer mean of the across-member mean concentration"
        v.units = "g/m3"
        v[:] = cell_mean

    fields = np.stack([np.ma.filled(member_field(handles, n, idx), np.nan)
                       for n in names]).astype(np.float64)
    with Dataset(MEMBER_FILE, "w", format="NETCDF4") as ds:
        ds.title = "Per-member released tracer at the evaluation horizon"
        ds.horizon = f"{times[idx]:%Y-%m-%d %H:%M}"
        ds.hours_after_release = (times[idx] - RELEASE).total_seconds() / 3600.0
        ds.createDimension("member", len(names))
        ds.createDimension("layer", fields.shape[1])
        ds.createDimension("face", len(fx))
        ds.createVariable("member", str, ("member",))[:] = np.array(names, dtype=object)
        v = ds.createVariable("cTR1", "f8", ("member", "layer", "face"),
                              zlib=True, complevel=4)
        v.units = "g/m3"
        v[:] = fields

    for size, path in ((SPREAD_FILE.stat().st_size, SPREAD_FILE),
                       (MEMBER_FILE.stat().st_size, MEMBER_FILE)):
        print(f"wrote {path.relative_to(REPO)}  ({size / 1e6:.2f} MB)")


def member_field(handles, name, idx):
    return np.ma.masked_invalid(
        np.ma.asarray(handles[name].variables[VARIABLE][idx], dtype=float))


def load():
    """The published precursors, as (per-member fields at the archived horizon,
    sigma by time, cell mean by time, face x, face y, times, archived index)."""
    for path in (SPREAD_FILE, MEMBER_FILE):
        if not path.exists():
            raise SystemExit(
                f"missing {path.relative_to(REPO)}; run with --extract to rebuild it "
                "from the solver output, which is not published")
    with Dataset(SPREAD_FILE) as ds:
        fx = np.asarray(ds.variables["face_x"][:], dtype=float)
        fy = np.asarray(ds.variables["face_y"][:], dtype=float)
        hours = np.asarray(ds.variables["time"][:], dtype=float)
        sigma = np.asarray(ds.variables["sigma"][:], dtype=float)
        cell_mean = np.asarray(ds.variables["cell_mean"][:], dtype=float)
    times = [RELEASE + pd.Timedelta(hours=h) for h in hours]
    with Dataset(MEMBER_FILE) as ds:
        members = {n: np.ma.masked_invalid(np.asarray(v, dtype=float))
                   for n, v in zip(ds.variables["member"][:],
                                   np.asarray(ds.variables["cTR1"][:], dtype=float))}
        archived = float(ds.hours_after_release)
    idx = int(np.argmin(np.abs(hours - archived)))
    return members, sigma, cell_mean, fx, fy, times, idx


def spread(fields):
    """Model-spread score and ensemble mean per horizontal cell, before the eligibility threshold.

    The standard deviation across members scales with the concentration itself, so
    ranking cells by it ranks them by how much of the release they hold: the highest
    values always fall around the release, wherever that happens to be, and the
    answer to "where should we sample" is always "at the spill". Dividing by the
    ensemble mean asks a different question, and the one a sampling plan needs: where
    do the alternatives disagree about whether the plume is there at all.

    `fields` is one (layer, face) array per member.
    """
    stack = np.ma.stack(fields)                             # (M, layer, face)
    sd = stack.std(axis=0)
    mu = stack.mean(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.ma.masked_invalid(np.ma.where(mu > 0, sd / mu, np.ma.masked))
    return (np.ma.mean(ratio, axis=0).filled(np.nan),
            np.ma.mean(mu, axis=0).filled(0.0))


def ranked(sigma, cell_mean, threshold=MODEL_SIGNAL_FRACTION):
    """The score with the model-signal threshold applied, unranked cells set to NaN.

    The ratio is unbounded where there is nothing to measure. A cell holding a
    billionth of the release can differ tenfold between members while being far below
    the scale relevant to this analysis, and at the reported horizon those cells are
    the far field the plume has not reached. Cells whose ensemble mean falls below a
    fraction of the largest are therefore not ranked at all. Because the threshold is
    applied to the mean rather than to the score, it can be moved without going back
    to the members.
    """
    return np.where(cell_mean >= threshold * cell_mean.max(), sigma, np.nan)


def score(members, names, threshold=MODEL_SIGNAL_FRACTION):
    """The ranked score recomputed from a named subset of the members."""
    return ranked(*spread([members[n] for n in names]), threshold)


def retained(sigma, n=N_RETAINED):
    return np.argsort(np.nan_to_num(sigma, nan=-np.inf))[::-1][:n]


def shore_distances(lon, lat):
    """Distance from each point to the nearest shoreline vertex, in metres.

    A retained cell that sits on the shoreline can be sampled from the bank, so it
    does not motivate a vessel. Reporting how far the retained cells lie from shore
    is what shows whether the plan needs one.
    """
    path = REPO / "data" / "sampling_plan" / "lake_outline_segments.csv"
    if not path.exists():
        return None
    seg = pd.read_csv(path).to_numpy().reshape(-1, 2, 2)
    verts = seg.reshape(-1, 2)
    kmlon = 111000.0 * np.cos(np.radians(float(np.mean(lat))))
    d = np.hypot((lon[:, None] - verts[None, :, 0]) * kmlon,
                 (lat[:, None] - verts[None, :, 1]) * 111000.0)
    return d.min(axis=1)


def describe(label, sigma, order, fx, fy):
    top = sigma[order]
    lon, lat = fx[order], fy[order]
    kmlon = 111.0 * np.cos(np.radians(float(np.mean(lat))))
    labels = DBSCAN(eps=CLUSTER_EPS_M / 6371000, min_samples=1,
                    metric="haversine").fit_predict(
        np.radians(np.column_stack([lat, lon])))
    print(f"  {label:32s} max {top.max():.4g}  min/max {top.min() / top.max():6.4f}  "
          f"extent {(lon.max() - lon.min()) * kmlon:5.2f} x "
          f"{(lat.max() - lat.min()) * 111.0:4.2f} km  "
          f"clusters {len(set(labels)):3d}")
    shore = shore_distances(lon, lat)
    if shore is not None:
        print(f"  {'':32s} distance from shore: median {np.median(shore):5.0f} m, "
              f"min {shore.min():4.0f} m, max {shore.max():5.0f} m, "
              f"{int((shore < 50).sum())} of {len(shore)} within 50 m")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=float, default=7.0,
                    help="horizon after the release at which to evaluate the score")
    ap.add_argument("--scan", action="store_true",
                    help="report every available horizon and exit, without writing")
    ap.add_argument("--cells", type=int, default=N_RETAINED,
                    help="how many highest-scoring cells to retain")
    ap.add_argument("--threshold", type=float, default=MODEL_SIGNAL_FRACTION,
                    help="model-signal threshold as a fraction of the largest cell mean")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    ap.add_argument("--extract", action="store_true",
                    help="rebuild the published precursors from the solver output, "
                         "which is not in this repository, then continue")
    ap.add_argument("--runs-dir",
                    help="the solver run tree --extract reads; overrides $%s"
                         % external_runs.ENV_VAR)
    args = ap.parse_args()

    write_ensemble_table(_CANDIDATE_ROWS, _QUALIFYING_RMSE)
    names = [m[0] for m in MEMBERS]
    if args.extract:
        # The member file is written at the horizon this run evaluates, so the
        # extraction and the reported result cannot disagree about which that is.
        runs = external_runs.resolve(args.runs_dir)
        handles, _fx, _fy, solver_times = open_solver(runs)
        wanted = RELEASE + pd.Timedelta(days=args.days)
        extract(runs, int(np.argmin([abs((t - wanted).total_seconds())
                                     for t in solver_times])))
        for ds in handles.values():
            ds.close()

    members, sigma_all, mean_all, fx, fy, times, archived = load()
    print(f"{len(MEMBERS)} members, {VARIABLE} on {len(fx)} cells, "
          f"{len(times)} output times from {times[0]:%Y-%m-%d} to {times[-1]:%Y-%m-%d}")
    for short, desc, rmse in MEMBERS:
        print(f"  {short:12s} {desc:44s} seasonal RMSE {rmse:.4f}")

    if args.scan:
        # Which horizon gives a plan worth drawing: several clusters, spread along the
        # lake, and far enough offshore that reaching them needs a vessel.
        print("horizon   clusters  extent (km)   shore distance (m)      score max")
        for i, t in enumerate(times):
            days = (t - RELEASE).total_seconds() / 86400
            if days <= 0:
                continue
            sigma = ranked(sigma_all[i], mean_all[i], args.threshold)
            order = retained(sigma, args.cells)
            lon, lat = fx[order], fy[order]
            kmlon = 111.0 * np.cos(np.radians(float(np.mean(lat))))
            labels = DBSCAN(eps=CLUSTER_EPS_M / 6371000, min_samples=1,
                            metric="haversine").fit_predict(
                np.radians(np.column_stack([lat, lon])))
            shore = shore_distances(lon, lat)
            shore_txt = (f"median {np.median(shore):5.0f}  min {shore.min():4.0f}"
                         if shore is not None else "n/a")
            print(f"{days:5.2f} d    {len(set(labels)):5d}    "
                  f"{(lon.max() - lon.min()) * kmlon:5.2f} x "
                  f"{(lat.max() - lat.min()) * 111.0:4.2f}   {shore_txt}   "
                  f"{sigma[order].max():.4g}")
        return 0

    wanted = RELEASE + pd.Timedelta(days=args.days)
    idx = int(np.argmin([abs((t - wanted).total_seconds()) for t in times]))
    print(f"\nrelease {RELEASE:%Y-%m-%d %H:%M}, evaluated at {times[idx]:%Y-%m-%d %H:%M}"
          f" ({(times[idx] - RELEASE).total_seconds() / 86400:.2f} days after)\n")

    sigma = ranked(sigma_all[idx], mean_all[idx], args.threshold)
    order = retained(sigma, args.cells)
    describe(f"M={len(names)} (all members)", sigma, order, fx, fy)

    # The per-member fields are published at one horizon, so the two checks that
    # need them are reported there and skipped elsewhere rather than silently
    # computed from the wrong time.
    if idx != archived:
        print(f"\nper-member fields are published at {times[archived]:%Y-%m-%d %H:%M} "
              f"only; the distinctness check and the member-count sensitivity are "
              f"not reported at this horizon")
    else:
        seps = [(a, b, float(np.ma.abs(members[a] - members[b]).max()))
                for a, b in itertools.combinations(names, 2)]
        worst = min(seps, key=lambda s: s[2])
        print(f"\nmembers are distinct; closest pair {worst[0]}/{worst[1]} differs by "
              f"{worst[2]:.4g} g/m3")
        if worst[2] <= 0:
            raise SystemExit(f"{worst[0]} and {worst[1]} produced identical fields")

        print("\nsensitivity of the retained set to the number of members")
        reference = set(order.tolist())
        for m in range(3, len(names) + 1):
            overlaps = [
                len(set(retained(score(members, list(c), args.threshold),
                                 args.cells).tolist()) & reference) / float(args.cells)
                for c in itertools.combinations(names, m)]
            arr = np.array(overlaps)
            print(f"  M={m}  {len(overlaps):2d} subsets   overlap with M={len(names)}:"
                  f"  mean {arr.mean():.3f}  min {arr.min():.3f}  max {arr.max():.3f}")

    frame = pd.DataFrame({
        "Model-spread score": sigma[order],
        "Longitude": fx[order],
        "Latitude": fy[order],
        "time": times[idx].strftime("%Y-%m-%d"),
    })
    if args.dry_run:
        print(f"\ndry run; {OUT} not written")
        return 0
    frame.to_csv(OUT, index=False)
    print(f"\nwrote {OUT} with {len(frame)} cells")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
