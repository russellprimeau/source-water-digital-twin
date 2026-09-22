"""Publish the calibration events behind the profiler calibration history.

The profiler's sonde is calibrated against reference standards between deployments,
and the article reports how far each sensor had drifted when it was next checked. Each
check compares the sensor's reading against a standard of known value, before and after
adjustment, at one, two or three points depending on the sensor.

What this publishes is the measurement each check consists of: which sensor, when,
against what standard, and what the sensor read before and after adjustment. That is
what the fitted gain and offset the article reports are computed from.

One row per calibration point, rather than one per event, keeps the number of points a
check used visible in the record itself.

Two of the instrument's own bookkeeping fields decide which checks count, and they
are applied here because they are not published: a check is kept when the sonde
recorded it as completed rather than completed with warnings, and when the time it
reports for the previous calibration is present and no earlier in the year than the
check itself. A check failing either is an aborted or mis-stamped record rather than
a measurement of drift.

Calibration history is read against the surface sonde's operating record, so the
hours that instrument was logging are published beside the checks. Only the hours
are taken, not what was measured in them.

Usage:
    .venv/Scripts/python src/model/ExportCalibrationRecord.py --extract --source DIR
    .venv/Scripts/python src/model/ExportCalibrationRecord.py --extract --hourly PATH
"""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / 'data' / 'profiler_calibration'
EVENTS = OUTDIR / 'calibration_events.csv'
UPTIME = OUTDIR / 'surface_uptime_hours.csv'

# The columns carrying the measurement, and nothing else. A check records up to three
# points, each as a standard and the reading before and after adjustment.
TIME_COL = 'Calibration End Time'
TIME_COL_HOURLY = 'TIMESTAMP'
PARAMETER_COL = 'Parameter Type'
STATUS_COL = 'Calibration Status'
LAST_COL = 'Last Calibration Time'
START_COL = 'Calibration Start Time'
COMPLETED = 'Completed'
POINT_COLUMNS = (
    ('Standard', 'Pre Calibration Value', 'Post Calibration Value'),
    ('Standard 2', 'Pre Calibration Value 2', 'Post Calibration Value 2'),
    ('Standard 3', 'Pre Calibration Value 3', 'Post Calibration Value 3'),
)

NUMBER = re.compile(r'-?\d+(?:\.\d+)?')
TIME_FORMATS = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S',
                '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S')


def year(text):
    """The year of a timestamp field, or None if it carries no readable one."""
    text = (text or '').strip()
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(text, fmt).year
        except ValueError:
            continue
    return None


def counts_as_a_check(record):
    """Whether a row is a completed check with a coherent previous-calibration time."""
    if (record.get(STATUS_COL) or '').strip() != COMPLETED:
        return False
    last, start = year(record.get(LAST_COL)), year(record.get(START_COL))
    return last is not None and start is not None and last >= start


def number(text):
    """The leading number in a field, which may carry a unit, or None."""
    if text is None:
        return None
    found = NUMBER.search(text.strip())
    return float(found.group()) if found else None


def read_events(source):
    """Every calibration point in the instrument's summary tables."""
    rows = []
    for path in sorted(Path(source).glob('*.csv')):
        event = 0
        with open(path, newline='', encoding='utf-8-sig') as handle:
            for record in csv.DictReader(handle):
                when = (record.get(TIME_COL) or '').strip()
                parameter = (record.get(PARAMETER_COL) or '').strip()
                if not when or not parameter:
                    continue
                if not counts_as_a_check(record):
                    continue
                # The sonde occasionally stamps two checks with the same end
                # time, so points are numbered by check rather than by time.
                event += 1
                for index, (std, pre, post) in enumerate(POINT_COLUMNS, start=1):
                    if std not in record:
                        continue
                    standard = number(record.get(std))
                    before = number(record.get(pre))
                    after = number(record.get(post))
                    if standard is None or before is None:
                        continue
                    rows.append({
                        'parameter': parameter,
                        'event': event,
                        'calibration_end_time': when,
                        'point': index,
                        'standard': standard,
                        'pre_calibration_value': before,
                        'post_calibration_value': after,
                    })
    rows.sort(key=lambda r: (r['parameter'], r['event'], r['point']))
    return rows


def write_events(rows):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fields = ['parameter', 'event', 'calibration_end_time', 'point', 'standard',
              'pre_calibration_value', 'post_calibration_value']
    with open(EVENTS, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    events = {(r['parameter'], r['event']) for r in rows}
    by_parameter = {}
    for parameter, _when in events:
        by_parameter[parameter] = by_parameter.get(parameter, 0) + 1
    print('wrote %s  (%d point(s) across %d event(s))'
          % (EVENTS.relative_to(ROOT), len(rows), len(events)))
    for parameter in sorted(by_parameter):
        print('  %-22s %2d event(s)' % (parameter, by_parameter[parameter]))


def write_uptime(source):
    """The hours the surface sonde was logging, one timestamp per row."""
    hours = set()
    unreadable = 0
    with open(source, newline='', encoding='utf-8-sig') as handle:
        for record in csv.DictReader(handle):
            stamp = (record.get(TIME_COL_HOURLY) or '').strip()
            if not stamp:
                continue
            try:
                when = datetime.fromisoformat(stamp.replace('T', ' '))
            except ValueError:
                unreadable += 1
                continue
            hours.add(when.replace(minute=0, second=0, microsecond=0))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    with open(UPTIME, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['hour'])
        for when in sorted(hours):
            writer.writerow([when.strftime('%Y-%m-%d %H:00:00')])
    print('wrote %s  (%d hour(s), %.2f MB)'
          % (UPTIME.relative_to(ROOT), len(hours), UPTIME.stat().st_size / 1e6))
    if unreadable:
        print('  %d row(s) carried no readable timestamp' % unreadable)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--extract', action='store_true',
                    help='rebuild the published record from the instrument summary '
                         'tables, which are not in this repository')
    ap.add_argument('--source', type=Path,
                    help='directory of the instrument summary tables, one per sensor')
    ap.add_argument('--hourly', type=Path,
                    help="the surface sonde's hourly record, for the uptime strip")
    args = ap.parse_args()

    if not args.extract:
        print('Nothing to do without --extract; the record is already in %s'
              % OUTDIR.relative_to(ROOT))
        return 0
    if args.source is not None:
        if not args.source.is_dir():
            raise SystemExit('summary tables not found: %s' % args.source)
        write_events(read_events(args.source))
    if args.hourly is not None:
        if not args.hourly.is_file():
            raise SystemExit('hourly record not found: %s' % args.hourly)
        write_uptime(args.hourly)
    if args.source is None and args.hourly is None:
        raise SystemExit('--extract needs --source DIR and/or --hourly PATH')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
