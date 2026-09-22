"""Pair modelled temperature with profiler observations.

Every temperature comparison the article reports rests on one question: which model
value corresponds to a measurement taken at a given depth and time? This module holds
the answer, so that the figures, the residuals and the error statistics cannot disagree
about it.

It reads only what `data/thermal_simulation/profiler/` publishes: the profiler's
instrument log as it was logged, and the modelled temperature reduced from the
solver history file. The comparison can therefore be re-derived and checked here,
with the selection and quality filtering applied in front of the reader rather
than baked into a stored extract.

Three choices decide the result.

**Depth bands.** Observations are grouped into one-metre bands by the rounded magnitude
of their depth, and each band is reported at its nominal depth. The profiler samples
continuously as it winches, so without banding every measurement would sit at its own
depth and no series would have more than a handful of points.

**Which layers bracket an observation.** Only the layers spanning the observed depth
range take part in the interpolation, plus one extra above and below. The padding
matters because the preselection uses each layer's nominal depth while the
interpolation uses its true depth, and a sigma layer can move far enough between the
two for the nominal bracket to be a layer short.

**Nominal against true depth.** A layer's nominal depth is its average over the run;
its true depth is where it actually sits at each output time. For sigma layers these
differ — the shallowest layer here is nominally 0.9 m deep but ranges from 1.09 m to
1.48 m as the water level moves. Wherever a layer's true depth varies by more than a
centimetre, the true depth is used. Treating a sigma layer as fixed would attribute a
model value to the wrong depth by more than the spacing between layers near the surface.
"""

from __future__ import annotations

import csv
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from netCDF4 import Dataset, num2date

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / 'data' / 'thermal_simulation' / 'profiler'
MODEL_FILE = RECORD / 'model_profile.nc'
OBSERVATIONS_FILE = RECORD / 'Profiler_Step.csv'

# Columns of the instrument log this comparison reads. The log carries nine other
# sonde parameters, which the temperature comparison does not use.
OBS_TIME_COL = 'TIMESTAMP'
OBS_VALUE_COL = 'sensorParms(1)'      # water temperature, degC
OBS_DEPTH_COL = 'sensorParms(9)'      # vertical position, metres below surface

# Plausible ranges for those two columns, both open intervals. A winched sonde on
# a lake that freezes cannot read 0 degC or below in open water, nor 25 degC or
# above at this latitude, and a reading outside the range is the instrument
# faulting rather than the water changing. The same holds for a position at or
# above the surface, or below any sounding in the lake.
VALUE_RANGE = (0.0, 25.0)             # degC
DEPTH_RANGE = (0.0, 100.0)            # m

# The station and variable every temperature comparison in the article uses.
STATION = 'Profiler'
VARIABLE = 'temperature'

# The solver writes this where a layer lies below the bed at a station, and
# netCDF fill values arrive at around this magnitude.
DRY_SENTINEL = -998.0
FILL_LIMIT = 9.0e36

# Observations are grouped into bands this wide, by the magnitude of their depth.
DEPTH_BAND_M = 1.0

# A layer whose true depth moves less than this over the run is treated as fixed at
# its nominal depth. Below a centimetre the distinction cannot matter to a comparison
# against a winched sonde.
SIGMA_TOLERANCE_M = 0.01

# Extra layers taken above and below the bracketing pair. See the module docstring.
BRACKET_PADDING = 1

# The profiler takes a profile over roughly an hour and a half; readings closer
# together than this belong to the same descent.
PROFILE_WINDOW = timedelta(minutes=100)
# Longer than this between profiles is an outage rather than the normal cadence,
# and the figures draw it as a break instead of joining across it.
GAP_THRESHOLD = timedelta(hours=13)


class ModelProfile:
    """Modelled temperature at the profiler, with each layer's depth over time.

    Layers are held shallowest first. `nominal_depth` and `true_depth` are both
    negative below the surface, matching the solver's convention.
    """

    def __init__(self, times, nominal_depth, true_depth, temperature):
        self.times = times
        self.nominal_depth = np.asarray(nominal_depth, dtype=float)
        self.true_depth = np.asarray(true_depth, dtype=float)
        self.temperature = np.asarray(temperature, dtype=float)
        self.seconds = np.array([(t - times[0]).total_seconds() for t in times],
                                dtype=float)

    @property
    def n_layers(self):
        return len(self.nominal_depth)


def load_model(path=MODEL_FILE):
    """The published model record."""
    if not Path(path).is_file():
        raise SystemExit(
            'missing %s; run src/model/ExportProfilerRecord.py --extract to rebuild '
            'it from the solver output, which is not published'
            % Path(path).relative_to(ROOT))
    with Dataset(path) as ds:
        timer = ds.variables['time']
        times = [datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
                 for t in num2date(timer[:], timer.units)]
        return ModelProfile(
            times=times,
            nominal_depth=np.asarray(ds.variables['nominal_depth'][:], dtype=float),
            true_depth=np.asarray(ds.variables['true_depth'][:], dtype=float),
            temperature=np.asarray(ds.variables['temperature'][:], dtype=float),
        )


def model_from_his(path, station=STATION, variable=VARIABLE):
    """A ModelProfile read straight from a solver history file.

    The reduced record this module normally reads is written from exactly this, so
    the two paths cannot diverge. Returns (profile, layers_below_the_bed).
    """
    with Dataset(path) as ds:
        raw = ds.variables['station_name'][:]
        # Station names are fixed-width and NUL-padded in the history file.
        names = [b''.join(row).decode('utf-8', 'replace').strip(chr(0)).strip()
                 for row in raw]
        if station not in names:
            raise SystemExit('station %r not in %s' % (station, names))
        loc = names.index(station)

        z = np.asarray(ds.variables['zcoordinate_c'][:], dtype=float)
        z[np.abs(z) > FILL_LIMIT] = np.nan
        usable = np.where(z <= DRY_SENTINEL, np.nan, z)
        flat = usable.reshape(-1, usable.shape[-1])
        with warnings.catch_warnings():
            # A layer dry at every station averages over nothing; the NaN that
            # produces is what marks it absent, so the warning is noise.
            warnings.simplefilter('ignore', RuntimeWarning)
            nominal = np.round(np.nanmean(flat, axis=0), 1)

        temperature = np.asarray(ds.variables[variable][:, loc, :], dtype=float)
        true_depth = usable[:, loc, :]

        present = [i for i in range(true_depth.shape[1])
                   if np.any(np.isfinite(true_depth[:, i]))]
        order = sorted(present, key=lambda i: nominal[i], reverse=True)

        timer = ds.variables['time']
        times = [datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
                 for t in num2date(timer[:], timer.units)]

    profile = ModelProfile(times=times, nominal_depth=nominal[order],
                           true_depth=true_depth[:, order],
                           temperature=temperature[:, order])
    return profile, temperature.shape[1] - len(order)


def load_observations(path=OBSERVATIONS_FILE, period=None):
    """The profiler readings this comparison uses, as (times, depths, values, rejected).

    Read from the instrument log as it was logged. Three things are applied here
    rather than to a stored extract, so that what the comparison rests on is visible
    in front of the reader instead of baked into a file:

      - only the temperature and vertical-position columns are taken;
      - readings outside the plausible ranges above are dropped as instrument faults;
      - `period`, when given as (first, last), restricts to the simulated window.

    Depths are returned negative below the surface, matching the model. The log
    records them positive, as metres below the surface.
    """
    path = Path(path)
    if not path.is_file():
        raise SystemExit('missing %s' % path.relative_to(ROOT))

    times, depths, values = [], [], []
    rejected = 0
    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in (OBS_TIME_COL, OBS_VALUE_COL, OBS_DEPTH_COL)
                   if c not in (reader.fieldnames or ())]
        if missing:
            raise SystemExit('%s has no column(s) %s'
                             % (path.relative_to(ROOT), missing))
        for row in reader:
            stamp = (row.get(OBS_TIME_COL) or '').strip()
            if not stamp:
                continue
            try:
                # The log stamps ISO 8601 with a T; accept a space too.
                when = datetime.fromisoformat(stamp.replace('T', ' '))
            except ValueError:
                continue                   # header repeats and units rows
            if period is not None and not period[0] <= when <= period[1]:
                continue
            try:
                value = float(row[OBS_VALUE_COL])
                depth = float(row[OBS_DEPTH_COL])
            except (TypeError, ValueError):
                continue
            if not (np.isfinite(value) and np.isfinite(depth)):
                continue
            if not (VALUE_RANGE[0] < value < VALUE_RANGE[1]
                    and DEPTH_RANGE[0] < depth < DEPTH_RANGE[1]):
                rejected += 1
                continue
            times.append(when)
            depths.append(-abs(depth))
            values.append(value)

    order = sorted(range(len(times)), key=lambda i: times[i])
    return ([times[i] for i in order],
            np.array([depths[i] for i in order], dtype=float),
            np.array([values[i] for i in order], dtype=float),
            rejected)


def select_bracketing_layers(nominal_depth, obs_depths, padding=BRACKET_PADDING):
    """Indices of the layers needed to bracket an observed depth range.

    `nominal_depth` is shallowest first. Returns the deepest layer still shallower
    than the shallowest observation, the shallowest layer still deeper than the
    deepest observation, anything between them, and `padding` layers either side.
    Always at least two layers, so there is a genuine bracket to interpolate across.
    """
    n = len(nominal_depth)
    if n <= 2 or obs_depths is None or len(obs_depths) == 0:
        return list(range(n))

    finite = [d for d in np.asarray(obs_depths, dtype=float) if np.isfinite(d)]
    if not finite:
        return [0]

    shallowest_obs = max(finite)      # least negative
    deepest_obs = min(finite)

    upper = 0
    for i in range(n):
        if nominal_depth[i] >= shallowest_obs:
            upper = i
        else:
            break

    lower = n - 1
    for i in range(n):
        if nominal_depth[i] <= deepest_obs:
            lower = i
            break

    if upper == lower:
        lower = min(upper + 1, n - 1)
    if lower < upper:
        upper = max(lower - 1, 0)

    pad = max(0, int(padding))
    return list(range(max(0, upper - pad), min(n - 1, lower + pad) + 1))


def interpolate_to_observations(model, layer_indices, obs_times, obs_depths):
    """Model temperature at each observation's time and depth.

    Interpolated linearly in time to the observation, then linearly in depth between
    the bracketing layers, using each layer's true depth wherever that varies.
    Observations outside the model's own time window return NaN.
    """
    obs_seconds = np.array([(t - model.times[0]).total_seconds() for t in obs_times],
                           dtype=float)
    outside = (obs_seconds < model.seconds[0]) | (obs_seconds > model.seconds[-1])

    def to_obs_times(values):
        result = np.interp(obs_seconds, model.seconds,
                           np.asarray(values, dtype=float))
        result[outside] = np.nan
        return result

    order = sorted(layer_indices, key=lambda i: model.nominal_depth[i], reverse=True)
    if len(order) == 1:
        return to_obs_times(model.temperature[:, order[0]])

    n_obs = len(obs_times)
    values_at_obs = [to_obs_times(model.temperature[:, i]) for i in order]
    depth_at_obs = np.tile(model.nominal_depth[order][:, None], (1, n_obs))

    for row, i in enumerate(order):
        true_depth = model.true_depth[:, i]
        finite = true_depth[np.isfinite(true_depth)]
        if finite.size == 0 or (finite.max() - finite.min()) <= SIGMA_TOLERANCE_M:
            continue                       # a fixed layer; its nominal depth is exact
        depth_at_obs[row, :] = to_obs_times(true_depth)

    obs_depths = np.asarray(obs_depths, dtype=float)
    result = np.full(n_obs, np.nan, dtype=float)
    for k in range(n_obs):
        target = obs_depths[k]
        if not np.isfinite(target):
            result[k] = values_at_obs[0][k]
            continue
        # Reversed so depth ascends, which is what np.interp requires.
        column = np.array([v[k] for v in values_at_obs[::-1]], dtype=float)
        depths = depth_at_obs[::-1, k]
        usable = np.isfinite(depths) & np.isfinite(column)
        if not np.any(usable):
            continue
        result[k] = float(np.interp(target, depths[usable], column[usable]))
    return result


def group_by_depth(obs_times, obs_depths, obs_values, band=DEPTH_BAND_M):
    """Observations gathered into depth bands, shallowest band first.

    Yields (nominal_depth_m, times, depths, values) with the nominal depth positive,
    as the published comparison reports it.
    """
    bands = {}
    for i, depth in enumerate(obs_depths):
        value = float(obs_values[i])
        if not np.isfinite(depth) or not np.isfinite(value):
            continue
        nominal = round(abs(depth) / band) * band
        bands.setdefault(nominal, ([], [], []))
        bands[nominal][0].append(obs_times[i])
        bands[nominal][1].append(depth)
        bands[nominal][2].append(value)
    for nominal in sorted(bands):
        times, depths, values = bands[nominal]
        yield (nominal, times, np.array(depths, dtype=float),
               np.array(values, dtype=float))


def profile_windows(obs_times, obs_depths, obs_values, window=PROFILE_WINDOW):
    """The (start, end) of each individual profile the instrument recorded."""
    rows = sorted((t, abs(float(d)), float(v))
                  for t, d, v in zip(obs_times, obs_depths, obs_values)
                  if np.isfinite(d) and np.isfinite(v))
    if not rows:
        return []

    profiles, bucket = [], []
    bucket_start = rows[0][0]

    def flush():
        if not bucket:
            return
        depths = np.array([r[1] for r in bucket], dtype=float)
        # A profile needs more than one distinct depth to be a profile at all.
        if len(np.unique(depths)) < 2:
            return
        times = [r[0] for r in bucket]
        profiles.append((min(times), max(times)))

    for row in rows:
        if row[0] >= bucket_start + window and bucket:
            flush()
            bucket = []
            bucket_start = row[0]
        bucket.append(row)
    flush()
    return profiles


def gap_windows(profiles, threshold=GAP_THRESHOLD):
    """Intervals between consecutive profiles that exceed the outage threshold."""
    return [(prev_end, next_start)
            for (_, prev_end), (next_start, _) in zip(profiles, profiles[1:])
            if next_start - prev_end > threshold]


def validation_stats(model_values, observed_values):
    """Comparison statistics over the finite paired subset."""
    model = np.asarray(model_values, dtype=float)
    observed = np.asarray(observed_values, dtype=float)
    usable = np.isfinite(model) & np.isfinite(observed)
    n = int(usable.sum())
    if n < 2:
        return {'n': n}
    m, o = model[usable], observed[usable]
    error = m - o
    ss_res = float(np.sum(error ** 2))
    ss_tot = float(np.sum((o - np.mean(o)) ** 2))
    return {
        'n': n,
        'r2': 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan'),
        'pearson_r': float(np.corrcoef(m, o)[0, 1]),
        'rmse': float(np.sqrt(np.mean(error ** 2))),
        'mae': float(np.mean(np.abs(error))),
        'bias': float(np.mean(error)),
        'final_error': float(error[-1]),
        'max_abs_error': float(np.max(np.abs(error))),
    }


def pair_all(model=None, observations=None, band=DEPTH_BAND_M):
    """Every depth band paired against the model, with its statistics.

    Returns (rows, stats_by_depth, gaps) where rows are
    (time, nominal_depth_m, observed, modelled) in band order.
    """
    model = model if model is not None else load_model()
    if observations is not None:
        times, depths, values = observations[:3]
    else:
        times, depths, values, _rejected = load_observations(
            period=(model.times[0], model.times[-1]))

    gaps = gap_windows(profile_windows(times, depths, values))

    rows, stats = [], {}
    for nominal, band_times, band_depths, band_values in group_by_depth(
            times, depths, values, band=band):
        layers = select_bracketing_layers(model.nominal_depth, band_depths)
        modelled = interpolate_to_observations(model, layers, band_times, band_depths)
        stats[nominal] = validation_stats(modelled, band_values)
        for i, when in enumerate(band_times):
            rows.append((when, nominal, band_values[i], modelled[i]))
    return rows, stats, gaps
