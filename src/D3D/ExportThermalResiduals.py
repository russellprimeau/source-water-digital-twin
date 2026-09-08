"""Plot retained paired temperature residuals; optionally extract with existing tools.

Default (public plot regeneration): python src/D3D/ExportThermalResiduals.py
Local extraction: use the D3DFMRunner Python environment and append --extract.
No model execution or forcing generation is performed.
"""
from pathlib import Path
import argparse
import importlib.util
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'data/validation/temperature_residuals_ThermalTune_2024.csv'

def extract():
    runner = ROOT.parent / 'D3DFMRunner'
    sys.path.insert(0, str(runner / 'src'))
    spec = importlib.util.spec_from_file_location('thermal_post', runner / 'src/hydro/d_hydro_post.py')
    post = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = post
    spec.loader.exec_module(post)
    his, warnings = post.hydro_output.load_his(str(ROOT / 'data/d3d/ThermalTune/FlowFM2026/output/FlowFMnew_his.nc'))
    if his is None:
        raise RuntimeError(warnings)
    post._his_ds = his
    dates = [t.replace(tzinfo=None) for t in post.hydro_output.his_times_as_datetimes(his)]
    series = list(his.iter_series())
    pairs_path = runner / 'data/sources/config/hydro/Pairings.csv'
    pairs = post.validation.load_pairings(str(pairs_path))
    # Shared reader returns (pairings, messages) in supported versions.
    if isinstance(pairs, tuple):
        pairs = pairs[0]
    sources = post.validation.observation_sources_dir(str(pairs_path))
    frames = []
    for depth in (1,20,50):
        pairing = next(p for p in pairs if p['label'] == f'Temperature vs. Depth Profiles_{depth}m')
        result = post._process_pairing(pairing, Path(sources), dates, series, {}, {}, [], include_error_trace=True)
        residual = result.correlation_series[0]
        frame = pd.DataFrame({'time': residual.time_labels, 'depth_m': depth,
                              'model_minus_observation_degC': residual.values})
        frames.append(frame.dropna())
        print(depth, result.stats)
    CSV.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(CSV, index=False)

def plot():
    frame = pd.read_csv(CSV, parse_dates=['time'])
    fig, axes = plt.subplots(3,1,figsize=(7.2,5.4),sharex=True,sharey=True,layout='constrained')
    for ax, depth in zip(axes,(1,20,50)):
        d = frame[frame.depth_m == depth]
        ax.axhline(0,color='0.35',lw=.7)
        ax.scatter(d.time,d.model_minus_observation_degC,s=3,color='#176c9c',rasterized=True)
        ax.text(.015,.85,f'{depth} m',transform=ax.transAxes)
        ax.grid(alpha=.2)
    axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    axes[-1].set_xlabel('2024')
    fig.supylabel('Model − observation (°C)')
    fig.savefig(ROOT/'docs/manuscript/Fig14.png',dpi=300)
    plt.close(fig)

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extract',action='store_true')
    args=p.parse_args()
    if args.extract:
        extract()
    plot()
