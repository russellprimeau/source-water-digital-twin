"""Publish what the thermal temperature comparison reads.

The thermal simulation is evaluated by comparing modelled temperature against the
profiler's measured profiles. This script writes both sides of that comparison into
data/thermal_simulation/profiler/, so everything downstream runs from this repository
alone. It needs the solver history file and the profiler's instrument log, neither of
which is published, so it runs where those are held.

The instrument log is written out for the reported period, carrying the datalogger's
own columns with each field copied across verbatim. Which of its readings enter the
comparison is decided by src/model/profiler_pairing.py at run time, not here.

The history file carries every variable at every station, far more than this
comparison reads, so the modelled side is reduced.

Two details are worth stating, because neither is recoverable from the reduced files
once they are written.

The model carries forty layers, but only thirty-five of them exist at the profiler:
the five deepest sit below the bed there and the solver marks them with a -999
sentinel. Only the thirty-five real layers are published.

Each layer is published with two depths. The nominal depth is the layer's mean over
the whole run and every station, rounded to a decimetre, which is what the solver's
own labelling reports. The true depth is that layer's actual depth at the profiler at
each output time. For a sigma layer the two differ: the shallowest layer here is
nominally 0.9 m deep but in truth moves between 1.09 m and 1.48 m as the water level
changes. The comparison uses the true depth wherever it varies, so both are published.

Usage:
    .venv/Scripts/python src/model/ExportProfilerRecord.py --extract --log PATH
    .venv/Scripts/python src/model/ExportProfilerRecord.py --extract --his PATH
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from netCDF4 import Dataset

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profiler_pairing                                                  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / 'data' / 'thermal_simulation' / 'profiler'
MODEL = OUTDIR / 'model_profile.nc'
LOG = OUTDIR / 'Profiler_Step.csv'

# The datalogger's own columns are published; the station position that was
# annotated onto each row afterwards is not.
ANNOTATED_COLUMNS = ('lat', 'lon')
# The last year any reported period covers.
LAST_YEAR = 2024

# The solver history file, inside this repository's own output tree, which is the
# solver's working directory and is never published.
DEFAULT_HIS = ROOT / 'data' / 'thermal_simulation' / 'output' / 'FlowFMnew_his.nc'

STATION = profiler_pairing.STATION


def write_log(source):
    """The instrument log over the reported period, in the logger's own columns.

    Field text is copied across verbatim rather than parsed and reformatted, so
    the published record reads exactly as the datalogger left it.
    """
    OUTDIR.mkdir(parents=True, exist_ok=True)
    with open(source, newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        header = next(reader)
        keep = [i for i, name in enumerate(header)
                if name.strip() not in ANNOTATED_COLUMNS]
        if profiler_pairing.OBS_TIME_COL not in header:
            raise SystemExit('%s has no %s column'
                             % (source, profiler_pairing.OBS_TIME_COL))
        stamp_at = header.index(profiler_pairing.OBS_TIME_COL)

        kept = later = unreadable = 0
        with open(LOG, 'w', newline='', encoding='utf-8') as out:
            writer = csv.writer(out)
            writer.writerow([header[i] for i in keep])
            for row in reader:
                if len(row) <= stamp_at:
                    unreadable += 1
                    continue
                try:
                    when = datetime.fromisoformat(
                        row[stamp_at].strip().replace('T', ' '))
                except ValueError:
                    unreadable += 1
                    continue
                if when.year > LAST_YEAR:
                    later += 1
                    continue
                writer.writerow([row[i] for i in keep])
                kept += 1

    print('wrote %s  (%d reading(s), %.2f MB)'
          % (LOG.relative_to(ROOT), kept, LOG.stat().st_size / 1e6))
    if unreadable:
        print('  %d row(s) carried no readable timestamp' % unreadable)


def write_model(profile, dropped):
    """The reduced model record, one variable per quantity the comparison needs."""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    times = profile.times
    epoch = times[0]
    with Dataset(MODEL, 'w', format='NETCDF4') as ds:
        ds.title = ('Thermal simulation: modelled temperature and layer depths at the '
                    'profiler station')
        ds.station = STATION
        ds.note = ('nominal_depth is each layer mean over the run and every station, '
                   'to a decimetre; true_depth is that layer depth at this station at '
                   'each output time. They differ for sigma layers.')
        ds.createDimension('time', len(times))
        ds.createDimension('layer', profile.n_layers)

        v = ds.createVariable('time', 'f8', ('time',))
        v.units = 'seconds since ' + epoch.strftime('%Y-%m-%d %H:%M:%S')
        v.calendar = 'standard'
        v[:] = [(t - epoch).total_seconds() for t in times]

        v = ds.createVariable('nominal_depth', 'f8', ('layer',))
        v.units = 'm'
        v.long_name = 'layer depth, negative below the surface'
        v[:] = profile.nominal_depth

        for name, arr, units, note in (
            ('true_depth', profile.true_depth, 'm',
             'layer depth at this station, negative below the surface'),
            ('temperature', profile.temperature, 'degC', 'modelled water temperature'),
        ):
            v = ds.createVariable(name, 'f8', ('time', 'layer'),
                                  zlib=True, complevel=4)
            v.units = units
            v.long_name = note
            v[:] = arr

    size = MODEL.stat().st_size / 1e6
    print('wrote %s  (%d times x %d layers, %.2f MB)'
          % (MODEL.relative_to(ROOT), len(times), profile.n_layers, size))
    if dropped:
        print('  %d layer(s) lie below the bed at %s and are not published'
              % (dropped, STATION))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--extract', action='store_true',
                    help='rebuild the published record from the solver history '
                         'file, which is not in this repository')
    ap.add_argument('--his', type=Path, default=DEFAULT_HIS,
                    help='the solver history file to reduce')
    ap.add_argument('--log', type=Path,
                    help='the profiler instrument log to publish')
    args = ap.parse_args()

    if not args.extract:
        print('Nothing to do without --extract; the reduced record is already in %s'
              % OUTDIR.relative_to(ROOT))
        return 0

    if not args.his.is_file():
        raise SystemExit('history file not found: %s' % args.his)
    profile, dropped = profiler_pairing.model_from_his(args.his)
    write_model(profile, dropped)

    if args.log is None:
        print('no --log given; the modelled side was rebuilt, the instrument log '
              'was left as it is')
        return 0
    if not args.log.is_file():
        raise SystemExit('instrument log not found: %s' % args.log)
    write_log(args.log)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
