"""Draw the profiler calibration history from the published calibration record.

Each time the sonde is calibrated, every sensor is compared against a standard of known
value and adjusted. A check records that at one, two or three points depending on the
sensor.

The correction applied at a point is the reading after adjustment less the magnitude of
the reading before it. The magnitude matters: a sensor reading 0.86 FNU below a zero
turbidity standard is 0.86 out, exactly as one reading 0.86 above it is, and in both
cases the adjustment pulls the reading toward the standard. Taking the reading as
signed would record the first as a positive correction and the second as a negative
one, which would put drift of the same size on opposite sides of zero.

Across the points of a check, the correction is modelled as

    correction = offset + gain * reading

and the offset is what this figure plots: the part of the correction that does not
depend on where in the sensor's range the reading falls, which is the drift accumulated
since the sensor was last set right. A check with a single point cannot separate the two
terms, so the gain is held at zero and the whole correction is the offset.

Usage:
    .venv/Scripts/python src/figures/make_fig10.py
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
EVENTS = ROOT / 'data' / 'profiler_calibration' / 'calibration_events.csv'
UPTIME = ROOT / 'data' / 'profiler_calibration' / 'surface_uptime_hours.csv'
OUT = ROOT / 'output' / 'Fig10.png'

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_style import use, open_frame, check_font, WIDTH  # noqa: E402

DPI = 600

# The order the panels are stacked in, and the label each carries.
SENSORS = (
    ('DO (% Sat)', 'DO Offset\n(% Sat)'),
    ('fDOM (QSU)', 'fDOM Offset\n(QSU)'),
    ('fDOM (RFU)', 'fDOM Offset\n(RFU)'),
    ('pH', 'pH Offset'),
    ('Sp Cond (µS/cm)', 'Specific Cond. Offset\n(µS/cm)'),
    ('Turbidity (FNU)', 'Turbidity Offset\n(FNU)'),
)

# A check is drawn by how many points it used, which is what decides whether the
# gain could be separated from the offset at all.
POINT_COLOURS = {1: '#1f77b4', 2: '#ff7f0e', 3: '#2ca02c'}

PANEL_H = 0.62

# The window the history is drawn over.
WINDOW = (datetime(2020, 4, 1), datetime(2025, 4, 1))
# Consecutive surface readings this far apart or less mean the instrument was
# logging continuously between them; a longer break is an outage.
UPTIME_GAP = timedelta(hours=2)


def read_events(path=EVENTS):
    """The published record, grouped into checks."""
    if not Path(path).is_file():
        raise SystemExit('missing %s' % Path(path).relative_to(ROOT))
    checks = defaultdict(list)
    for row in csv.DictReader(open(path, newline='', encoding='utf-8')):
        after = row['post_calibration_value'].strip()
        if not after:
            continue          # a point the sonde never completed carries no correction
        before = abs(float(row['pre_calibration_value']))
        after = float(after)
        key = (row['parameter'], int(row['event']))
        checks[key].append((datetime.fromisoformat(row['calibration_end_time']),
                            after, after - before))
    return checks


def uptime_spans(path=UPTIME, window=WINDOW):
    """The intervals the surface sonde was logging, and how many hours it logged."""
    if not Path(path).is_file():
        raise SystemExit('missing %s' % Path(path).relative_to(ROOT))
    hours = sorted({datetime.fromisoformat(row['hour'])
                    for row in csv.DictReader(open(path, newline='',
                                                   encoding='utf-8'))})
    counted = sum(1 for h in hours if window[0] <= h < window[1])
    spans = []
    for left, right in zip(hours[:-1], hours[1:]):
        if right <= window[0] or left >= window[1]:
            continue
        if right - left > UPTIME_GAP:
            continue
        start, end = max(left, window[0]), min(right, window[1])
        if end > start:
            spans.append((start, end))
    return spans, counted


def offsets(checks):
    """The fitted offset of every check, by sensor."""
    by_sensor = defaultdict(list)
    for (parameter, _event), points in checks.items():
        when = points[0][0]
        reading = np.array([p[1] for p in points], dtype=float)
        correction = np.array([p[2] for p in points], dtype=float)
        if len(points) == 1:
            offset = float(correction[0])
        else:
            offset = float(np.polyfit(reading, correction, 1)[1])
        by_sensor[parameter].append((when, offset, len(points)))
    for parameter in by_sensor:
        by_sensor[parameter].sort()
    return by_sensor


def draw(by_sensor, spans, hours):
    use()
    fig, all_axes = plt.subplots(len(SENSORS) + 1, 1,
                                 figsize=(WIDTH, (len(SENSORS) + 1) * PANEL_H),
                                 sharex=True, layout='constrained')
    strip, axes = all_axes[0], all_axes[1:]

    for start, end in spans:
        strip.axvspan(start, end, color='#1f3b57', linewidth=0)
    strip.set_ylim(0, 1)
    strip.set_yticks([])
    strip.set_ylabel('Surface (Hourly) Uptime\n- %s Hours'
                     % format(hours, ','),
                     rotation=0, ha='right', va='center', labelpad=6)
    for side in ('left', 'right', 'top', 'bottom'):
        strip.spines[side].set_visible(side == 'bottom')

    for ax, (parameter, label) in zip(axes, SENSORS):
        events = by_sensor.get(parameter, [])
        ax.axhline(0, color='0.45', lw=0.6, zorder=1)
        for points in sorted(POINT_COLOURS):
            subset = [e for e in events if e[2] == points]
            if not subset:
                continue
            ax.scatter([e[0] for e in subset], [e[1] for e in subset], s=7,
                       color=POINT_COLOURS[points], linewidths=0, zorder=2)
        ax.set_ylabel('%s - %d events' % (label, len(events)), rotation=0,
                      ha='right', va='center', labelpad=6)
        ax.grid(True, axis='y', alpha=0.25)
        open_frame(ax)

    axes[-1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for tick in axes[-1].get_xticklabels():
        tick.set_rotation(90)
    axes[-1].set_xlabel('Calibration End Time')

    # Built from the colour table rather than from one panel's contents: no single
    # sensor uses every point count, so a panel's own handles would under-report.
    used = {n for events in by_sensor.values() for _, _, n in events}
    handles = [Line2D([], [], marker='o', linestyle='', markersize=3.5,
                      color=POINT_COLOURS[n], label='%d-point' % n)
               for n in sorted(used)]
    fig.legend(handles=handles, loc='lower left', frameon=True,
               bbox_to_anchor=(0.02, 0.01))

    check_font()
    axes[-1].set_xlim(*WINDOW)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI)
    plt.close(fig)
    print('%d check(s) across %d sensors -> %s'
          % (sum(len(v) for v in by_sensor.values()), len(SENSORS),
             OUT.relative_to(ROOT)))


def main():
    by_sensor = offsets(read_events())
    for parameter, label in SENSORS:
        events = by_sensor.get(parameter, [])
        counts = {n: sum(1 for e in events if e[2] == n) for n in sorted(POINT_COLOURS)}
        print('  %-18s %2d check(s)  %s' % (
            parameter, len(events),
            ', '.join('%d-point %d' % (n, c) for n, c in counts.items() if c)))
    spans, hours = uptime_spans()
    print('  %-18s %s logging hour(s) in the window' % ('surface sonde', format(hours, ',')))
    draw(by_sensor, spans, hours)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
