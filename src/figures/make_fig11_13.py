"""Draw the per-depth temperature comparisons of the validation appendix.

Figure 5 plots all fifty depth groups at once, which shows the seasonal envelope but
buries the behaviour of any single depth. These three panels isolate 1, 20 and 50 m
from the same paired records: the surface mixed layer, the transitional layer where
temperature falls sharply with depth, and the cold deep water beneath it.

They are drawn from the same CSV as Figure 5, so a trace here is the trace of that
depth there. The pairing is done once, during the extraction that writes the CSV;
this script only selects and draws. There is no --extract here because
src/model/ExportThermalProfiles.py owns that extraction, and two routes to one
artefact are what the convention prevents.

Usage:
    .venv/Scripts/python src/figures/make_fig11_13.py
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_style import (use, open_frame, check_font, WIDTH, LABEL,
                          PROXY_LW, GAP_GREY, TRACE)  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / 'output'
CSV = ROOT / 'data/thermal_simulation/validation/temperature_profiles_2024.csv'
GAPS = ROOT / 'data/thermal_simulation/validation/temperature_profile_gaps_2024.csv'

# Depth, and the figure it becomes. The caption labels them (a), (b) and (c).
PANELS = ((1, 'Fig11.png'), (20, 'Fig12.png'), (50, 'Fig13.png'))
# Three of these stack to the height of the residual figure of Appendix C, which
# plots the same three depths over the same period, so the pair reads as one.
PANEL_H = 1.6
# The trace colour is shared with the residual figure through figure_style. The depth
# colouring Figure 5 uses does not carry over: with fifty overlapping traces its pale
# end reads in context, but a single pale trace on white does not.


def draw(frame, gaps, depth, out, legend):
    d = frame[frame.depth_m == depth].sort_values('time')
    if d.empty:
        raise SystemExit(f'no paired records at {depth} m in {CSV.name}')

    fig, ax = plt.subplots(figsize=(WIDTH, PANEL_H), layout='constrained')
    if gaps is not None:
        for _, g in gaps.iterrows():
            ax.axvspan(g.start, g.end, color=GAP_GREY, lw=0, zorder=0)

    ax.plot(d.time, d.observed_degC, color=TRACE, zorder=2)
    ax.plot(d.time, d.model_degC, color=TRACE, ls='--', zorder=2)
    ax.annotate(f'{depth} m', xy=(0.012, 0.9), xycoords='axes fraction',
                fontsize=LABEL, va='top')

    if legend:
        ax.plot([], [], color=TRACE, lw=PROXY_LW, label='Observed')
        ax.plot([], [], color=TRACE, lw=PROXY_LW, ls='--', label='Modelled')
        handles, _ = ax.get_legend_handles_labels()
        if gaps is not None:
            handles.append(mpatches.Patch(color=GAP_GREY, label='No observations'))
        ax.legend(handles=handles, loc='upper right', frameon=False)

    ax.set_ylabel(r'Temperature ($^\circ$C)')
    ax.set_xlabel('2024')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid()
    open_frame(ax)
    check_font()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTDIR / out, dpi=600)
    plt.close(fig)

    r = d.observed_degC.corr(d.model_degC)
    bias = (d.model_degC - d.observed_degC).mean()
    print(f'  {depth:2d} m  {len(d):4d} pairs  Pearson {r:.4f}  '
          f'mean model-minus-observation {bias:+.2f} degC  -> {out}')


def main() -> int:
    use()
    if not CSV.exists():
        raise SystemExit(f'missing {CSV.relative_to(ROOT)}; run '
                         'src/model/ExportThermalProfiles.py --extract to rebuild it')
    frame = pd.read_csv(CSV, parse_dates=['time'])
    gaps = (pd.read_csv(GAPS, parse_dates=['start', 'end'])
            if GAPS.exists() else None)
    if gaps is not None and gaps.empty:
        gaps = None
    for i, (depth, out) in enumerate(PANELS):
        draw(frame, gaps, depth, out, legend=(i == 0))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
