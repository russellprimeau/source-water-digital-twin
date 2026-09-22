"""Modelled minus observed water temperature at three depths.

Default mode draws the residual panels from the published series. With --extract it
first re-derives them from the reduced profiler record, using the same pairing rules
as every other temperature comparison; src/model/profiler_pairing.py holds them.
Nothing outside this repository is needed either way.

    .venv/Scripts/python src/model/ExportThermalResiduals.py
    .venv/Scripts/python src/model/ExportThermalResiduals.py --extract
"""
from pathlib import Path
import argparse
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'data/thermal_simulation/validation/temperature_residuals_2024.csv'

sys.path.insert(0, str(ROOT / 'src' / 'figures'))
from figure_style import use, open_frame, check_font, WIDTH, TRACE  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import profiler_pairing                                            # noqa: E402

# The depths the panels report, in metres below the surface.
DEPTHS = (1, 20, 50)

# The three panels match the per-panel height of the comparison figure of
# Appendix C, which plots the same three depths over the same period.
PANEL_H = 1.6

def extract():
    """Re-derive the residual series from the reduced profiler record."""
    rows, _stats, _gaps = profiler_pairing.pair_all()
    frames = []
    for depth in DEPTHS:
        band = [(t, m - o) for t, d, o, m in rows
                if d == depth and np.isfinite(m) and np.isfinite(o)]
        band.sort(key=lambda r: r[0])
        frames.append(pd.DataFrame({
            'time': [t.strftime('%Y-%m-%d %H:%M:%S') for t, _ in band],
            'depth_m': depth,
            'model_minus_observation_degC': [v for _, v in band]}))
        print(f'  {depth:2d} m  {len(band)} residual(s)')
    CSV.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(CSV, index=False)
    print(f'wrote {CSV.relative_to(ROOT)}')


def plot():
    frame = pd.read_csv(CSV, parse_dates=['time'])
    use()
    fig, axes = plt.subplots(3, 1, figsize=(WIDTH, 3 * PANEL_H), sharex=True,
                             sharey=True, layout='constrained')
    for ax, depth in zip(axes,(1,20,50)):
        d = frame[frame.depth_m == depth]
        ax.axhline(0, color='0.45', lw=0.6)
        ax.scatter(d.time, d.model_minus_observation_degC, s=2, color=TRACE,
                   linewidths=0, rasterized=True)
        ax.text(.012, .88, f'{depth} m', transform=ax.transAxes, va='top')
        ax.grid()
        open_frame(ax)
    axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    axes[-1].set_xlabel('2024')
    fig.supylabel('Model − observation (°C)')
    check_font()
    out = ROOT / 'output' / 'Fig14.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=600)
    plt.close(fig)

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--extract', action='store_true',
                   help='re-derive the residuals from the reduced profiler record')
    args = p.parse_args()
    if args.extract:
        extract()
    plot()
