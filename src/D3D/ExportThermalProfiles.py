"""
ExportThermalProfiles.py

Observed and modelled water temperature at every profiler depth group, from the
same history file and the same pairing definitions that produce the per-depth
comparison in the temperature validation appendix.

Default (public plot regeneration): python src/D3D/ExportThermalProfiles.py
Local extraction: use the D3DFMRunner Python environment and append --extract.
No model execution or forcing generation is performed.

Output: data/validation/temperature_profiles_ThermalTune_2024.csv
        docs/manuscript/Fig5.png
"""
from pathlib import Path
import argparse
import importlib.util
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'data/validation/temperature_profiles_ThermalTune_2024.csv'
GAPS = ROOT / 'data/validation/temperature_profile_gaps_ThermalTune_2024.csv'
PNG = ROOT / 'docs/manuscript/Fig5.png'
HIS = ROOT / 'data/d3d/ThermalTune/FlowFM2026/output/FlowFMnew_his.nc'
PAIRING_LABEL = 'Temperature vs. Depth Profiles_All'


def extract():
    runner = ROOT.parent / 'D3DFMRunner'
    sys.path.insert(0, str(runner / 'src'))
    spec = importlib.util.spec_from_file_location(
        'thermal_post', runner / 'src/hydro/d_hydro_post.py')
    post = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = post
    spec.loader.exec_module(post)

    his, warnings = post.hydro_output.load_his(str(HIS))
    if his is None:
        raise RuntimeError(warnings)
    post._his_ds = his
    dates = [t.replace(tzinfo=None)
             for t in post.hydro_output.his_times_as_datetimes(his)]
    series = list(his.iter_series())

    pairs_path = runner / 'data/sources/config/hydro/Pairings.csv'
    pairs = post.validation.load_pairings(str(pairs_path))
    if isinstance(pairs, tuple):          # shared reader returns (pairings, messages)
        pairs = pairs[0]
    sources = post.validation.observation_sources_dir(str(pairs_path))

    pairing = next(p for p in pairs if p['label'] == PAIRING_LABEL)
    result = post._process_pairing(pairing, Path(sources), dates, series,
                                   {}, {}, [], include_error_trace=True)
    if not result.depth_group_results:
        raise RuntimeError(f'{PAIRING_LABEL}: no depth groups returned ({result.kind})')

    frames = []
    for group in result.depth_group_results:
        nominal, labels, obs, model = group[0], group[1], group[2], group[3]
        frames.append(pd.DataFrame({'time': labels, 'depth_m': nominal,
                                    'observed_degC': obs, 'model_degC': model}))
    frame = pd.concat(frames)
    CSV.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(CSV, index=False)
    print(f'{len(frame)} paired records across '
          f'{frame.depth_m.nunique()} depth groups -> {CSV}')

    # The intervals in which the profiler returned nothing, so that the figure can
    # distinguish a flat line from an absent one. Same source as the appendix panels.
    windows = result.profile_gap_windows or []
    pd.DataFrame({'start': [w[0] for w in windows],
                  'end': [w[1] for w in windows]}).to_csv(GAPS, index=False)
    print(f'{len(windows)} observation gap(s) -> {GAPS}')


def plot():
    frame = pd.read_csv(CSV, parse_dates=['time'])
    depths = sorted(frame.depth_m.unique())
    norm = mcolors.Normalize(vmin=min(depths), vmax=max(depths))
    cmap = cm.viridis_r

    fig, ax = plt.subplots(figsize=(9.0, 4.6), layout='constrained')

    gaps = pd.read_csv(GAPS, parse_dates=['start', 'end']) if GAPS.exists() else None
    if gaps is not None and len(gaps):
        for _, g in gaps.iterrows():
            ax.axvspan(g.start, g.end, color='0.85', lw=0, zorder=0)

    for depth in depths:
        d = frame[frame.depth_m == depth].sort_values('time')
        colour = cmap(norm(depth))
        ax.plot(d.time, d.observed_degC, color=colour, lw=0.8, zorder=2)
        ax.plot(d.time, d.model_degC, color=colour, lw=0.8, ls='--', zorder=2)

    ax.plot([], [], color='0.25', lw=1.1, label='Observed')
    ax.plot([], [], color='0.25', lw=1.1, ls='--', label='Modelled')
    handles, _ = ax.get_legend_handles_labels()
    if gaps is not None and len(gaps):
        handles.append(mpatches.Patch(color='0.85', label='No observations'))
    ax.legend(handles=handles, loc='upper right', frameon=False)
    ax.set_ylabel('Temperature ($^\\circ$C)')
    ax.set_xlabel('2024')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(alpha=0.25)

    bar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, pad=0.01)
    bar.set_label('Depth (m)')
    bar.ax.invert_yaxis()

    fig.savefig(PNG, dpi=300)
    plt.close(fig)
    print(f'{len(depths)} depth groups plotted -> {PNG}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extract', action='store_true')
    args = p.parse_args()
    if args.extract:
        extract()
    plot()
