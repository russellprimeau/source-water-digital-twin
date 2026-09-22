"""Solver throughput of the reported configuration, from the coefficient sweep.

Appendix F quotes a median wall-clock time and a ratio of simulated time to wall-clock
time. Both come from a nine-iteration sweep over the heat-exchange and turbulence
coefficients, run on the mesh and vertical discretization of the thermal simulation over
a window inside its period.

The simulated period is read from each iteration's own configuration rather than assumed.
The ratio is the one number in the article that cannot be checked against a figure, so
the quantity it divides by has to come from the record too.

Usage:
    .venv/Scripts/python src/model/BuildThroughputBenchmark.py
    .venv/Scripts/python src/model/BuildThroughputBenchmark.py --extract
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
# The sweep inside the solver run tree, which --extract is told where to find.
SWEEP_SUBDIR = "tuner_fixed"
sys.path.insert(0, str(REPO / "src"))
import external_runs                                                     # noqa: E402
OUT = REPO / "data" / "thermal_simulation" / "throughput" / "benchmark_runs.csv"

MPI_PARTITIONS = 12
# The sweep varies these four and nothing else.
COEFFICIENTS = ["Xlozmidov", "maxItVerticalForester", "Dalton", "Stanton"]

STAMP = re.compile(r"^\[(\d\d:\d\d:\d\d)\]")
ITER = re.compile(r"iter\s+(\d+):")


def elapsed_minutes(log_text):
    """Wall-clock minutes per iteration, from the sweep log.

    Each iteration opens with an `iter N:` line and closes when the solver's history
    file is reported. The sweep ran overnight and iterations 3 onward start after
    midnight, so a negative difference is one that wrapped the day.
    """
    starts, ends = [], []
    for line in log_text.splitlines():
        stamp = STAMP.match(line)
        if not stamp:
            continue
        when = datetime.strptime(stamp.group(1), "%H:%M:%S")
        if ITER.search(line) and "=" in line:
            starts.append(when)
        elif "HIS:" in line:
            ends.append(when)
    if len(starts) != len(ends):
        raise SystemExit(f"{len(starts)} iterations started but {len(ends)} finished")

    out = []
    for start, end in zip(starts, ends):
        seconds = (end - start).total_seconds()
        if seconds < 0:
            seconds += 86_400
        out.append(seconds / 60.0)
    return out


def read_mdu(path):
    """Simulated period in days, and the tuned coefficients, from one iteration."""
    text = path.read_text(errors="replace")

    def value(key):
        m = re.search(rf"(?im)^{key}\s*=\s*(\S+)", text)
        return m.group(1) if m else None

    start, stop = float(value("tStart")), float(value("tStop"))
    row = {"simulated_days": (stop - start) / 86_400.0}
    for name in COEFFICIENTS:
        v = value(name)
        row[name] = float(v) if v is not None else float("nan")
    return row


def extract(sweep):
    """Reduce the sweep log and its archived configurations to the committed table."""
    log = sweep / "tune_log.txt"
    if not log.exists():
        raise SystemExit(f"missing {log}; the sweep archive is not published")
    minutes = elapsed_minutes(log.read_text(errors="replace"))

    runs = sorted(p for p in sweep.glob("*iter_*") if p.is_dir())
    if len(runs) != len(minutes):
        raise SystemExit(f"{len(runs)} archived runs but {len(minutes)} timings")

    rows = []
    for i, (run, mins) in enumerate(zip(runs, minutes)):
        row = {"iteration": i}
        row.update(read_mdu(run / "FlowFMnew.mdu"))
        row["wallclock_minutes"] = round(mins, 2)
        rows.append(row)

    table = pd.DataFrame(rows)
    days = table["simulated_days"].unique()
    if len(days) != 1:
        raise SystemExit(f"iterations cover different periods: {days}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT, index=False)
    print(f"wrote {OUT.relative_to(REPO)}")


def main() -> int:
    if "--extract" in sys.argv:
        extract(external_runs.resolve(external_runs.argv_option(sys.argv))
                / SWEEP_SUBDIR)
    if not OUT.exists():
        raise SystemExit(
            f"missing {OUT.relative_to(REPO)}; run with --extract to rebuild it from "
            "the coefficient sweep, which is not published")
    table = pd.read_csv(OUT)

    days = float(table["simulated_days"].iloc[0])
    median = float(table["wallclock_minutes"].median())
    ratio = days * 86_400.0 / (median * 60.0)

    print(f"Coefficient sweep: {len(table)} runs of {days:.1f} simulated days each, "
          f"under {MPI_PARTITIONS} MPI partitions\n")
    print(table.to_string(index=False, float_format=lambda v: f"{v:g}"))
    print(f"\nmedian wall clock            {median:.1f} minutes")
    print(f"simulated s per wall-clock s  {ratio:.0f}")
    print(f"\nread {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
