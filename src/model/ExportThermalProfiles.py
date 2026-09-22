"""Observed and modelled water temperature at every profiler depth band.

Default mode draws Figure 5 from the published comparison. With --extract it first
re-derives that comparison from the reduced profiler record, pairing each observation
with the model by depth and time; src/model/profiler_pairing.py holds the rules and
explains them. Nothing outside this repository is needed either way.

    .venv/Scripts/python src/model/ExportThermalProfiles.py
    .venv/Scripts/python src/model/ExportThermalProfiles.py --extract

Output: data/thermal_simulation/validation/temperature_profiles_2024.csv
        data/thermal_simulation/validation/temperature_profile_gaps_2024.csv
        data/thermal_simulation/validation/temperature_by_depth_2024.csv
        output/Fig5.png
"""
from pathlib import Path
import argparse
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'figures'))
from figure_style import (use, open_frame, check_font, WIDTH, PROXY_LW,
                          GAP_GREY, TRACE)  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import profiler_pairing                                                  # noqa: E402
VALIDATION = ROOT / 'data' / 'thermal_simulation' / 'validation'
CSV = VALIDATION / 'temperature_profiles_2024.csv'
GAPS = VALIDATION / 'temperature_profile_gaps_2024.csv'
BY_DEPTH = VALIDATION / 'temperature_by_depth_2024.csv'
PNG = ROOT / 'output' / 'Fig5.png'


def extract():
    """Re-derive the published comparison from the published profiler record."""
    model = profiler_pairing.load_model()
    period = (model.times[0], model.times[-1])
    times, depths, values, rejected = profiler_pairing.load_observations(
        period=period)
    print(f'{len(times)} reading(s) in the simulated period, '
          f'{rejected} dropped as instrument faults')
    rows, stats, gaps = profiler_pairing.pair_all(
        model=model, observations=(times, depths, values))

    VALIDATION.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(
        [(t.strftime('%Y-%m-%d %H:%M:%S'), int(d), o, m) for t, d, o, m in rows],
        columns=['time', 'depth_m', 'observed_degC', 'model_degC'])
    frame.to_csv(CSV, index=False)
    print(f'{len(frame)} paired records across '
          f'{frame.depth_m.nunique()} depth bands -> {CSV.relative_to(ROOT)}')

    pd.DataFrame({'start': [g[0].strftime('%Y-%m-%d %H:%M:%S') for g in gaps],
                  'end': [g[1].strftime('%Y-%m-%d %H:%M:%S') for g in gaps]}
                 ).to_csv(GAPS, index=False)
    print(f'{len(gaps)} observation gap(s) -> {GAPS.relative_to(ROOT)}')

    # The per-band error statistics the validation appendix tabulates. Generated
    # here rather than transcribed, so the table and the paired records cannot
    # disagree about what the model achieved at a given depth.
    pd.DataFrame(
        [{'depth_m': int(d), 'n': s['n'], 'r2': round(s['r2'], 3),
          'pearson_r': round(s['pearson_r'], 3), 'rmse_degC': round(s['rmse'], 3),
          'mae_degC': round(s['mae'], 3),
          'final_error_degC': round(s['final_error'], 3)}
         for d, s in sorted(stats.items())]
    ).to_csv(BY_DEPTH, index=False)
    print(f'{len(stats)} depth band(s) -> {BY_DEPTH.relative_to(ROOT)}')


def plot():
    use()
    frame = pd.read_csv(CSV, parse_dates=['time'])
    depths = sorted(frame.depth_m.unique())
    norm = mcolors.Normalize(vmin=min(depths), vmax=max(depths))
    cmap = cm.viridis_r

    fig, ax = plt.subplots(figsize=(WIDTH, 2.9), layout='constrained')

    gaps = pd.read_csv(GAPS, parse_dates=['start', 'end']) if GAPS.exists() else None
    if gaps is not None and len(gaps):
        for _, g in gaps.iterrows():
            ax.axvspan(g.start, g.end, color=GAP_GREY, lw=0, zorder=0)

    for depth in depths:
        d = frame[frame.depth_m == depth].sort_values('time')
        colour = cmap(norm(depth))
        ax.plot(d.time, d.observed_degC, color=colour, zorder=2)
        ax.plot(d.time, d.model_degC, color=colour, ls='--', zorder=2)

    ax.plot([], [], color=TRACE, lw=PROXY_LW, label='Observed')
    ax.plot([], [], color=TRACE, lw=PROXY_LW, ls='--', label='Modelled')
    handles, _ = ax.get_legend_handles_labels()
    if gaps is not None and len(gaps):
        handles.append(mpatches.Patch(color=GAP_GREY, label='No observations'))
    ax.legend(handles=handles, loc='upper right', frameon=False)
    ax.set_ylabel('Temperature ($^\\circ$C)')
    ax.set_xlabel('2024')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid()
    open_frame(ax)

    bar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, pad=0.01)
    bar.set_label('Depth (m)')
    bar.ax.invert_yaxis()

    check_font()
    PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG, dpi=600)
    plt.close(fig)
    print(f'{len(depths)} depth groups plotted -> {PNG}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--extract', action='store_true',
                   help='re-derive the comparison from the reduced profiler record')
    args = p.parse_args()
    if args.extract:
        extract()
    plot()
