"""Check that the committed scenario series came from the run they are attributed to.

The series plotted in the scenario time-series figure are published as CSV files. This
script matches each one, value by value at every timestep, against the history output of
the simulation named below, so that the figure's provenance is a verified fact rather
than an attribution.

The monitoring points in the run's own output carry generic names, so the mapping from
file to station is established by value rather than by position or label: each committed
series is compared against every station and must match exactly one.

The run output this checks against is not published: it is tens of gigabytes, and the
repository distributes the reduced series only. The check therefore runs on a machine
that holds the run, behind the same --extract flag the other scripts use to reach
outside the repository.

Usage:
    .venv/Scripts/python src/model/VerifyScenarioProvenance.py --extract
"""

from __future__ import annotations

import csv
import datetime as dt
import sys
from pathlib import Path

import numpy as np
from netCDF4 import Dataset, num2date

REPO = Path(__file__).resolve().parents[2]
COMMITTED = REPO / "data" / "scenario_simulation" / "series"
# Where the run sits inside the solver run tree.  Read only by --extract; the
# tree is outside this repository and is named on the command line, not here.
RUN_SUBPATH = (Path("Nitrogen") / "OneHourEUTROPH.dsproj_data" / "Water_Quality"
               / "output" / "deltashell_his.nc")
sys.path.insert(0, str(REPO / "src"))
import external_runs                                                     # noqa: E402

SPECIES = ["NH4", "NO3"]
SITES = ["Source", "Spjelkavikelva", "Vasstrandlia", "Profiler", "FarField"]

# A match must be this close relative to the series maximum. The committed files carry
# about twelve significant figures, so a true match is limited only by that.
TOLERANCE = 1e-9


def committed(species, site):
    with open(COMMITTED / f"{species}{site}.csv", newline="") as handle:
        reader = csv.reader(handle)
        next(reader)
        rows = [(dt.datetime.strptime(r[0], "%Y.%m.%d %H:%M:%S"), float(r[1]))
                for r in reader]
    return [t for t, _ in rows], np.array([v for _, v in rows])


def main() -> int:
    if "--extract" not in sys.argv:
        print("This check compares the committed scenario series against the run they")
        print("are attributed to. That run output is not published, so the check needs")
        print("--extract and a machine that holds it, named with --runs-dir.")
        return 0
    run = external_runs.resolve(external_runs.argv_option(sys.argv)) / RUN_SUBPATH
    if not run.exists():
        raise SystemExit(f"run output not found: {run}")
    ds = Dataset(run)
    timer = ds.variables["nTimesDlwq"]
    times = [num2date(v, timer.units) for v in timer[:]]
    stamps = {dt.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second): i
              for i, t in enumerate(times)}
    n_stations = len(ds.dimensions["nStations"])
    print(f"run   : {run.name}, {n_stations} monitoring points, {len(times)} timesteps")
    print(f"        {times[0]} to {times[-1]}\n")

    ok = True
    for species in SPECIES:
        field = np.asarray(ds.variables[species][:], dtype=float)
        for site in SITES:
            when, values = committed(species, site)
            rows = [stamps[t] for t in when if t in stamps]
            if len(rows) != len(when):
                print(f"  {species}{site}: only {len(rows)} of {len(when)} timestamps "
                      f"present in the run output")
                ok = False
                continue
            # Compare against every station; exactly one must match.
            scale = max(abs(values).max(), 1e-30)
            errors = [np.abs(field[rows, s] - values).max() / scale
                      for s in range(n_stations)]
            best = int(np.argmin(errors))
            matches = [s for s, e in enumerate(errors) if e <= TOLERANCE]
            verdict = "ok " if len(matches) == 1 and matches[0] == best else "FAIL"
            if verdict == "FAIL":
                ok = False
            print(f"  {verdict} {species}{site:16s} matches station {best + 1} "
                  f"of {n_stations}   relative difference {errors[best]:.2e}   "
                  f"({len(matches)} station{'' if len(matches) == 1 else 's'} within "
                  f"tolerance)")
        print()

    print("VERIFIED: every committed series is reproduced by this run"
          if ok else "MISMATCH: see above")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
