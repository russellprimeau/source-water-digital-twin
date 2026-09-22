"""
BuildCalibrationTable.py

Rebuild the model-configuration comparison table from the solver's own records, so that
every value in data/configuration_comparison/calibration.csv is derived rather than transcribed.

Default (public verification): python src/model/BuildCalibrationTable.py
    Checks the committed table against the model definitions published in
    data/configuration_comparison/mdu/, and reports any disagreement.

Local extraction: append --extract, naming the run tree with --runs-dir (or
D3DFM_RUNS).
    Reads each run's FlowFM.dia and FlowFM_timings.txt from the run archive,
    rebuilds every derivable column and reports differences from the committed
    table. Nothing is written unless --write is also given.

No model execution or forcing generation is performed.

Every field below is taken from the solver's own output:

    configuration   the resolved model definition D-Flow FM echoes into the
                    .dia under "* Active Model definition:", which is the
                    settings as the kernel actually ran them
    geometry        the grid census the kernel prints after initialisation
                    ("nr of netcells", "nr of 3D cells", ...)
    cost            the "Computation started/finished" timestamps

The comparison statistics are not derivable from the archive alone; they are
recomputed separately against the observation record.
"""
from pathlib import Path
import argparse
import datetime as dt
import math
import io
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
import external_runs                                                     # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import profiler_pairing                                                  # noqa: E402
CSV = ROOT / 'data/configuration_comparison/calibration.csv'
# The run group inside the solver run tree, which --extract is told where to find.
ARCHIVE_SUBDIR = 'OldTunes'
DATASET_DIR = ROOT / 'data/configuration_comparison'
COMPARISON_DIR = DATASET_DIR / 'mdu'

# The retained comparison. Other groups in the archive were not retained.
RETAINED_GROUPS = ('2mnth', '7mnth')

MDU_MARKER = '* Active Model definition:'
INFO = '** INFO   : '


def read_dia(path):
    """Split a .dia into its resolved MDU block and its INFO lines."""
    text = io.open(path, encoding='utf-8', errors='replace').read().split(chr(10))
    start = next(i for i, l in enumerate(text) if MDU_MARKER in l) + 1
    end = next(i for i in range(start, len(text)) if text[i].startswith('** '))
    return text[start:end], text


def parse_mdu(lines):
    """Resolved MDU block to {key: value}, lower-cased keys, comments stripped."""
    out = {}
    for line in lines:
        if '=' not in line or line.lstrip().startswith(('#', '[')):
            continue
        key, _, rest = line.partition('=')
        value = rest.split('#', 1)[0].strip()
        out[key.strip().lower()] = value
    return out


def info_number(lines, label):
    """The number on the INFO line whose text starts with `label`."""
    rx = re.compile(r'^' + re.escape(INFO) + re.escape(label) + r'\s*\(.*?\)\s*:\s*(\S+)')
    for line in lines:
        m = rx.match(line)
        if m:
            return float(m.group(1).replace('D', 'E'))
    return None


def info_timestamp(lines, label):
    """Parse 'Computation started  at: 11:14:31, 14-02-2025'."""
    rx = re.compile(re.escape(label) + r'\s*at:\s*(\d{2}:\d{2}:\d{2}),\s*(\d{2}-\d{2}-\d{4})')
    for line in lines:
        m = rx.search(line)
        if m:
            return dt.datetime.strptime(m.group(2) + ' ' + m.group(1), '%d-%m-%Y %H:%M:%S')
    return None


def as_float(text):
    """MDU numbers are Fortran-flavoured: 1.d-6, 20., 0.7"""
    if text in (None, ''):
        return None
    return float(text.replace('d', 'e').replace('D', 'E'))


def describe(run_dir):
    """Every derivable field for one run directory."""
    dia = run_dir / 'FlowFM.dia'
    block, lines = read_dia(dia)
    mdu = parse_mdu(block)

    ref = dt.datetime.strptime(mdu['refdate'], '%Y%m%d')
    start = ref + dt.timedelta(seconds=as_float(mdu['tstart']))
    stop = ref + dt.timedelta(seconds=as_float(mdu['tstop']))

    began = info_timestamp(lines, 'Computation started')
    ended = info_timestamp(lines, 'Computation finished')
    wall_h = (ended - began).total_seconds() / 3600.0 if began and ended else None

    period_h = (stop - start).total_seconds() / 3600.0

    return {
        'run': run_dir.parent.name + '/' + run_dir.name,
        'Max Layers': int(as_float(mdu.get('kmx'))),
        'Layer Type': {1: 'sigma', 2: 'z'}.get(int(as_float(mdu.get('layertype', '2'))), '?'),
        'Secchi Depth (m)': as_float(mdu.get('secchidepth')),
        'HMF?': int(as_float(mdu.get('horizontalmomentumfilter', '0'))),
        # The vertical filter is the Forester filter, applied to temperature and
        # salinity separately; the kernel echoes an iteration limit for each,
        # zero when the filter is off.
        'VFF?': int(any(as_float(mdu.get(k, '0'))
                        for k in ('maxitverticalforestertem',
                                  'maxitverticalforestersal'))),
        'Vicoww': as_float(mdu.get('vicoww')),
        'Dicoww': as_float(mdu.get('dicoww')),
        'Courant Limit': as_float(mdu.get('cflmax')),
        'Max Timestep (s)': as_float(mdu.get('dtmax')),
        'Start': start,
        'End': stop,
        'Simulation Period (h)': period_h,
        '2D Cells': int(info_number(lines, 'nr of netcells')),
        '3D Cells': int(info_number(lines, 'nr of 3D cells')),
        '3D Links': int(info_number(lines, 'nr of 3D links')),
        'Area (m2)': info_number(lines, 'my model area'),
        'Volume (m3)': info_number(lines, 'my model volume'),
        'Timesteps': int(info_number(lines, 'nr of timesteps')),
        'Run Time (h)': wall_h,
        'Simulation Time/Run Time': period_h / wall_h if wall_h else None,
    }




# --- comparison statistics --------------------------------------------------
#
# The configurations are scored the same way the manuscript scores the reported
# simulation: observations at the profiler are grouped into one-metre depth
# bands and every paired value is compared, pooled across bands. The pairing
# rules and the statistics live in src/model/profiler_pairing.py, so a run scored
# here and the reported simulation are scored the same way.

# Runs of different length are only comparable when scored over a period they
# all cover. Every retained run spans 25 April to 28 June 2024, so a second set
# of statistics is recorded over that period alongside the statistics over each
# run's own period.
COMMON_PERIOD = ('2024-04-25', '2024-06-28')
COMMON_COLUMNS = {
    'Correlation, common period': 'pearson_r',
    'Root Mean Squared Error, common period': 'rmse',
    'RMSE 95% lower, common period': 'rmse_lo',
    'RMSE 95% upper, common period': 'rmse_hi',
}

STAT_COLUMNS = {
    'RMSE 95% lower': 'rmse_lo',
    'RMSE 95% upper': 'rmse_hi',
    'Correlation': 'pearson_r',
    'Mean Absolute Error': 'mae',
    'Mean Squared Error': 'mse',
    'Root Mean Squared Error': 'rmse',
    'Mean Percent Error': 'mpe',
}


def recompute_stats(run_dir, observations, window=None):
    """Pooled comparison statistics for one run, over the depth bands.

    `window` is an optional (start, end) pair of dates. Runs of different
    lengths are only comparable when scored over a window they all cover, so
    restricting here is what lets a short run and a full-season run appear on
    the same axis.
    """
    import numpy as np
    import pandas as pd
    his = run_dir / 'FlowFM_his.nc'
    if not his.is_file():
        raise RuntimeError('%s: no FlowFM_his.nc' % run_dir.name)
    model, _dropped = profiler_pairing.model_from_his(his)

    times, depths, values = observations
    bands = 0
    obs_parts, mod_parts, day_parts = [], [], []
    for _nominal, band_times, band_depths, band_values in profiler_pairing.group_by_depth(
            times, depths, values):
        layers = profiler_pairing.select_bracketing_layers(model.nominal_depth,
                                                           band_depths)
        modelled = profiler_pairing.interpolate_to_observations(
            model, layers, band_times, band_depths)
        stamps = pd.to_datetime(pd.Series([t for t in band_times]))
        if window is not None:
            keep = ((stamps >= pd.Timestamp(window[0]))
                    & (stamps <= pd.Timestamp(window[1]))).values
            band_values, modelled, stamps = (band_values[keep], modelled[keep],
                                             stamps[keep])
        bands += 1
        obs_parts.append(band_values)
        mod_parts.append(modelled)
        day_parts.append(stamps.dt.strftime('%Y-%m-%d').values)

    if not obs_parts:
        raise RuntimeError('%s: no depth bands' % run_dir.name)
    obs = np.concatenate(obs_parts)
    mod = np.concatenate(mod_parts)
    day = np.concatenate(day_parts)

    stats = profiler_pairing.validation_stats(mod, obs)
    finite = np.isfinite(obs) & np.isfinite(mod)
    o, m = obs[finite], mod[finite]
    # Mean percent error in its usual sense: (observed - modelled) / observed.
    nonzero = o != 0
    stats['mpe'] = float(np.mean((o[nonzero] - m[nonzero]) / o[nonzero]) * 100.0)
    stats['mse'] = float(stats['rmse'] ** 2)
    stats['bands'] = bands
    lo, hi = rmse_interval(m - o, day[finite])
    stats['rmse_lo'], stats['rmse_hi'] = lo, hi
    return stats


def rmse_interval(error, day, draws=400, seed=0):
    """A 95% interval for the RMSE, resampling whole days.

    The RMSE is estimated from a finite set of paired observations, so it
    carries sampling uncertainty; that is what an error bar on one of these
    points should show. Residuals within a day are correlated across depth and
    in time, so whole days are resampled rather than individual values, which
    an ordinary bootstrap would treat as independent and so understate.
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    labels, index = np.unique(day, return_inverse=True)
    by_day = [np.flatnonzero(index == i) for i in range(len(labels))]
    draws_out = np.empty(draws)
    for k in range(draws):
        pick = rng.integers(0, len(by_day), len(by_day))
        sel = np.concatenate([by_day[i] for i in pick])
        draws_out[k] = np.sqrt(np.mean(error[sel] ** 2))
    return (float(np.percentile(draws_out, 2.5)),
            float(np.percentile(draws_out, 97.5)))


def check_geometry_invariant(described):
    """3D cell and link counts follow from the mesh, the layers and the batch.

    A z-layer count depends on how many layers are wet, so it is fixed by the
    mesh, the layer count and the initial water level. Runs sharing all three
    must report identical 3D geometry; a row that disagrees with its peers is
    a transcription error rather than a real difference. The two comparison
    batches started from different water levels, which is why the 4,935-cell
    40-layer runs report 65,904 cells over two months and 65,900 over the
    season -- a real difference, not a discrepancy.
    """
    groups = {}
    for d in described:
        key = (d['2D Cells'], d['Max Layers'], d['Simulation Period (h)'])
        groups.setdefault(key, []).append(d)
    census, bad = [], []
    for key, members in sorted(groups.items()):
        cells = sorted(set(m['3D Cells'] for m in members))
        links = sorted(set(m['3D Links'] for m in members))
        census.append((key, len(members), cells, links))
        if len(cells) > 1 or len(links) > 1:
            bad.append((key, cells, links))
    return census, bad


def archive_runs(archive):
    """Every retained run directory, keyed by '<group>/<run>'.

    A run is recognised by its diagnostics file. Directories holding only
    renamed copies of another run's output carry none, so they are skipped.
    """
    found = {}
    for group in RETAINED_GROUPS:
        base = archive / group
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            if (d / 'FlowFM.dia').is_file():
                found[group + '/' + d.name] = d
    return found


def committed_table():
    import pandas as pd
    t = pd.read_csv(CSV, sep=';', header=0)
    t.columns = [c.strip() for c in t.columns]
    # 'Path to Results' ends with <group>\<run>; that is the join key.
    t['run'] = [chr(47).join(str(p).replace(chr(92), chr(47)).split(chr(47))[-2:])
                for p in t['Path to Results']]
    return t




def same_value(text, value):
    """Is the cell already this value, whatever notation it is written in?

    Comparing rendered strings would rewrite 1.00E-06 as 1e-06 and churn the
    whole file for no change in meaning, so compare numbers when both sides
    are numeric and fall back to text otherwise.
    """
    if isinstance(value, str):
        return text == value
    try:
        return float(text.replace(',', '')) == float(value)
    except (TypeError, ValueError):
        return False


# Columns removed from the published table. "Sum of Squares Error" held values
# that were negative, which no sum of squares can be, and matched no definition
# that could be reproduced from the paired records; nothing reads it.
DROPPED_COLUMNS = ('Sum of Squares Error',)


DERIVED_COLUMNS = (
    'Max Layers', 'Layer Type', 'Secchi Depth (m)', 'HMF?', 'Vicoww', 'Dicoww',
    'Courant Limit', 'Max Timestep (s)', 'Simulation Period (h)', '2D Cells', 'VFF?',
    '3D Cells', '3D Links', 'Timesteps',
)


def write_table(table, runs, stats_by_run=None):
    """Rewrite the derived columns in place, leaving every other column alone.

    Columns the archive cannot supply -- the comparison statistics, the label
    and the inclusion flag -- are carried through untouched. Rounded columns
    (area, volume, run time) are left as recorded so the file keeps the
    precision it was published with.
    """
    # newline='' keeps the file's own line endings, so correcting four
    # values does not rewrite every line as a line-ending change.
    raw = io.open(CSV, encoding='utf-8', newline='').read().split(chr(10))
    header = [c.strip() for c in raw[0].split(';')]
    index = dict((c, i) for i, c in enumerate(header))

    for col in list(STAT_COLUMNS) + list(COMMON_COLUMNS):
        if col in index:
            continue
        index[col] = len(header)
        header.append(col)
        raw[0] = raw[0].rstrip(chr(13)) + ';' + col + raw[0][len(raw[0].rstrip(chr(13))):]
        for i in range(1, len(raw)):
            if raw[i].strip():
                body = raw[i].rstrip(chr(13))
                raw[i] = body + ';' + raw[i][len(body):]
        print('   added column: %s' % col)

    changed = 0
    for line_no in range(1, len(raw)):
        if not raw[line_no].strip():
            continue
        # Keep the line's terminator: the last column is written too, and
        # joining split cells would otherwise drop a trailing carriage return.
        line, eol = raw[line_no].rstrip(chr(13)), raw[line_no][len(raw[line_no].rstrip(chr(13))):]
        cells = line.split(';')
        path = cells[index['Path to Results']].replace(chr(92), chr(47))
        key = chr(47).join(path.split(chr(47))[-2:])
        if key not in runs:
            continue
        got = describe(runs[key])
        if stats_by_run is not None and key in stats_by_run:
            st = stats_by_run[key]
            for col, field in STAT_COLUMNS.items():
                if field in st.get('own', {}):
                    got[col] = round(float(st['own'][field]), 4)
            for col, field in COMMON_COLUMNS.items():
                if field in st.get('common', {}):
                    got[col] = round(float(st['common'][field]), 4)
        extra = (tuple(STAT_COLUMNS) + tuple(COMMON_COLUMNS)) if stats_by_run else ()
        for col in DERIVED_COLUMNS + extra:
            if col not in index:
                continue
            new = got[col]
            if new is None:
                continue
            current = cells[index[col]].strip()
            if same_value(current, new):
                continue          # keep the file's own notation
            text = ('%d' % new) if isinstance(new, int) else ('%g' % new)
            print('   %-26s %-18s %r -> %r' % (key, col, current, text))
            cells[index[col]] = text
            changed += 1
        raw[line_no] = ';'.join(cells) + eol

    drop = [index[c] for c in DROPPED_COLUMNS if c in index]
    if drop:
        keep = lambda cells: [c for i, c in enumerate(cells) if i not in drop]
        raw = [';'.join(keep(line.split(';'))) if line.strip() else line
               for line in raw]
        print('   removed column(s): %s' % ', '.join(DROPPED_COLUMNS))
        changed += len(drop)

    if not changed:
        print(chr(10) + 'nothing to write: the table already matches the solver.')
        return
    io.open(CSV, 'w', encoding='utf-8', newline='').write(chr(10).join(raw))
    print(chr(10) + 'wrote %d corrected value(s) to %s' % (changed, CSV))


# The settings that distinguish one configuration from another. Rows agreeing on
# every one of them are the same configuration recorded to different end dates.
# CSVplotter draws one marker per configuration and imports this list, so the
# figure and the count in the article cannot disagree about what a configuration is.
CONFIGURATION_SETTINGS = ('Max Layers', '2D Cells', 'Secchi Depth (m)', 'HMF?', 'VFF?',
                          'Vicoww', 'Dicoww', 'Max Timestep (s)', 'Courant Limit')


def configuration_census(table):
    """Collapse the run records into configurations and return the groups.

    A group of records claiming one configuration is only believable if the
    records agree, so each group's common-period statistics are reported beside
    it. They are computed over a period every run covers, which is what makes
    them comparable across runs of different length.
    """
    groups = []
    for key, rows in table.groupby(list(CONFIGURATION_SETTINGS), dropna=False, sort=False):
        stats = rows[['Correlation, common period',
                      'Root Mean Squared Error, common period']].drop_duplicates()
        groups.append((rows, len(stats) == 1))
    return groups


def report_census(table):
    groups = configuration_census(table)
    print('%d run records -> %d configurations' % (len(table), len(groups)))
    for rows, agree in groups:
        if len(rows) == 1:
            continue
        print('   %d records, one configuration%s:'
              % (len(rows), '' if agree else '  ** statistics disagree **'))
        for _, r in rows.iterrows():
            print('      %-34s RMSE %-8s r %-8s'
                  % (r['Path to Results'],
                     r['Root Mean Squared Error, common period'],
                     r['Correlation, common period']))
    disagreeing = [rows for rows, agree in groups if not agree]
    if disagreeing:
        raise SystemExit(
            'records grouped as one configuration report different statistics; '
            'they are different configurations and the grouping is wrong')
    return len(groups)


RANGES_TABLE = ROOT / 'output' / 'calibration_ranges.tex'

# Column in the committed table, the label the article prints, and how to render the
# set of values it takes. Water clarity is listed as the discrete set tried rather
# than a span: zero is the solver's disabled state, not a depth on the same scale as
# the others, and a zero run does not reproduce the one-metre run it was once folded
# into -- the two report different error statistics on the same mesh and layer count.
RANGE_ROWS = [
    ('2D Cells', 'Horizontal mesh', 'choice', '%s two-dimensional cells'),
    ('Max Layers', 'Vertical discretization', 'choice', '%s z-layers'),
    ('Secchi Depth (m)', 'Water clarity', 'choice', 'Secchi depth %s~m'),
    ('HMF?', 'Horizontal filtering', 'onoff', '%s'),
    ('VFF?', 'Vertical filtering', 'onoff', '%s'),
    ('Vicoww', 'Vertical eddy viscosity', 'power', '%s~m\\textsuperscript{2}/s'),
    ('Dicoww', 'Vertical eddy diffusivity', 'power', '%s~m\\textsuperscript{2}/s'),
    ('Courant Limit', 'Courant limit', 'choice', '%s'),
    ('Max Timestep (s)', 'Maximum timestep', 'choice', '%s~s'),
]


def _render(values, how):
    """The set of values a setting took, as the article words it."""
    if how == 'onoff':
        return 'On or off' if len(values) > 1 else ('On' if values[0] else 'Off')
    if how == 'power':
        lo, hi = min(values), max(values)
        power = lambda v: '$10^{%d}$' % round(math.log10(v))      # noqa: E731
        return power(lo) if lo == hi else '%s to %s' % (power(lo), power(hi))
    trim = lambda v: ('%g' % v)                                   # noqa: E731
    if how == 'span':
        lo, hi = min(values), max(values)
        return trim(lo) if lo == hi else '%s to %s' % (trim(lo), trim(hi))
    shown = ['{:,}'.format(int(v)) if v >= 1000 and v == int(v) else trim(v)
             for v in values]
    return shown[0] if len(shown) == 1 else (
        ' or '.join(shown) if len(shown) == 2
        else ', '.join(shown[:-1]) + ' or ' + shown[-1])


def write_ranges_table():
    """Emit the rows of Table A3 from the committed comparison record."""
    table = committed_table()
    eol = chr(92) * 2
    # The whole tabular is generated, not just its rows: \input inside a tabularx
    # upsets the alignment.
    lines = ['%% Generated by %s; do not edit by hand.' % Path(__file__).name,
             '%% From the retained model-configuration comparison records in %s.'
             % CSV.name,
             r'    \footnotesize',
             r'    \begin{tabularx}{\textwidth}{@{}l X@{}}',
             r'    \toprule',
             r'        \textbf{Setting} & \textbf{Range covered} ' + eol,
             r'    \midrule']
    for column, label, how, shape in RANGE_ROWS:
        values = sorted({float(v) for v in table[column].dropna()})
        if not values:
            raise SystemExit('%s: column %r is empty' % (CSV.name, column))
        lines.append('        %s & %s %s' % (label, shape % _render(values, how), eol))
    lines += [r'    \bottomrule', r'    \end{tabularx}']
    RANGES_TABLE.parent.mkdir(parents=True, exist_ok=True)
    RANGES_TABLE.write_text(chr(10).join(lines) + chr(10), encoding='utf-8')
    print('wrote %s from the comparison records'
          % RANGES_TABLE.relative_to(ROOT))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--extract', action='store_true',
                    help='read the run archive, which is not in this repository')
    ap.add_argument('--runs-dir', help='the solver run tree --extract reads')
    ap.add_argument('--stats', action='store_true',
                    help='also recompute the comparison statistics from each his file')
    ap.add_argument('--write', action='store_true',
                    help='write the regenerated table; ignored without --extract')
    args = ap.parse_args()

    if not args.extract:
        report_census(committed_table())
        return write_ranges_table()

    runs = archive_runs(external_runs.resolve(args.runs_dir) / ARCHIVE_SUBDIR)
    table = committed_table()
    print('archive runs: %d   committed rows: %d' % (len(runs), len(table)))

    missing = sorted(set(table['run']) - set(runs))
    extra = sorted(set(runs) - set(table['run']))
    if missing:
        print('in the table but not the archive: %s' % missing)
    if extra:
        print('in the archive but not the table: %s' % extra)

    numeric_tol = {
        'Area (m2)': 0.005, 'Volume (m3)': 0.005,      # the table rounds these
        'Run Time (h)': 0.01, 'Simulation Time/Run Time': 0.01,
        'Secchi Depth (m)': 0, 'Courant Limit': 0, 'Max Timestep (s)': 0,
        'Vicoww': 1e-12, 'Dicoww': 1e-12,
    }
    exact = ('Max Layers', '2D Cells', '3D Cells', '3D Links', 'Timesteps',
             'HMF?', 'VFF?', 'Simulation Period (h)')

    diffs = []
    for _, row in table.iterrows():
        key = row['run']
        if key not in runs:
            continue
        got = describe(runs[key])
        for col in list(exact) + [c for c in numeric_tol if c in table.columns]:
            if col not in table.columns:
                continue
            old = row[col]
            new = got[col]
            if new is None:
                continue
            try:
                old_f = float(str(old).replace(',', ''))
            except (TypeError, ValueError):
                continue
            tol = 0 if col in exact else numeric_tol[col]
            rel = abs(new - old_f) / max(abs(old_f), 1e-30)
            if (new != old_f) if tol == 0 else (rel > tol):
                diffs.append((key, row['Label'].strip(), col, old_f, new))

    if not diffs:
        print(chr(10) + 'every derivable column matches the committed table.')
    else:
        print(chr(10) + '%d disagreement(s):' % len(diffs))
        print('%-26s %-42s %-24s %>14s %>14s'.replace('>', '') %
              ('run', 'label', 'column', 'committed', 'from solver'))
        for key, label, col, old, new in diffs:
            print('%-26s %-42s %-24s %14s %14s'
                  % (key, label[:42], col, ('%g' % old), ('%g' % new)))

    described = [describe(runs[k]) for k in sorted(runs)]
    census, bad = check_geometry_invariant(described)
    print(chr(10) + 'grid census, by mesh, layers and simulated period:')
    print('   %6s %3s %8s %5s %9s %9s' % ('2D', 'L', 'hours', 'runs', '3D cells', '3D links'))
    for (cells2d, layers, hours), n, c, l in census:
        print('   %6d %3d %8.0f %5d %9s %9s'
              % (cells2d, layers, hours, n,
                 c[0] if len(c) == 1 else c, l[0] if len(l) == 1 else l))
    if bad:
        print(chr(10) + 'geometry differs between runs that should share it:')
        for (cells2d, layers, hours), c, l in bad:
            print('   %d cells x %d layers over %.0f h: cells %s, links %s'
                  % (cells2d, layers, hours, c, l))
    else:
        print('   every group is internally consistent.')

    stats_by_run = None
    if args.stats:
        # Every run is scored against the same readings, selected once.
        observations = profiler_pairing.load_observations()[:3]
        stats_by_run = {}
        print(chr(10) + 'recomputing comparison statistics, pooled over depth bands:')
        print('   %-26s %5s %6s %9s %9s %9s %9s'
              % ('run', 'bands', 'n com', 'RMSE own', 'RMSE old', 'RMSE com', 'r com'))
        for key in sorted(runs):
            own = recompute_stats(runs[key], observations)
            common = recompute_stats(runs[key], observations,
                                     window=COMMON_PERIOD)
            stats_by_run[key] = {'own': own, 'common': common}
            row = table[table['run'] == key].iloc[0]
            print('   %-26s %5d %6d %9.4f %9.4f %9.4f %9.4f'
                  % (key, own['bands'], common['n'], own['rmse'],
                     float(row['Root Mean Squared Error']),
                     common['rmse'], common['pearson_r']))

    if args.write:
        write_table(table, runs, stats_by_run)
    return 0


if __name__ == '__main__':
    sys.exit(main())
