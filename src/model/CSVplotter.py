"""
CSVplotter.py

Figure 6: accuracy against computational cost across the configuration search.

    python src/model/CSVplotter.py

Reads  data/configuration_comparison/calibration.csv
Writes output/Fig6.png

Two comparisons are drawn. Simulations of different length cannot be compared
on accumulated error, so the left panel scores every configuration over the
period they all cover, and the right panel scores those that ran to the end of
the observation record over that longer period. Within a panel the comparison
is like for like; between panels the values are not interchangeable.

One marker per distinct configuration. Several rows record the same
configuration run to different end dates; plotting every row would draw markers
on top of one another and overstate the search. Rows are collapsed only when
they agree in every setting, which the statistics confirm: each collapsed group
shares its common-period RMSE and correlation to four decimals.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'figures'))
from figure_style import (use, open_frame, check_font, WIDTH, TICK, LABEL,
                          TITLE)  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from BuildCalibrationTable import CONFIGURATION_SETTINGS     # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'data/configuration_comparison/calibration.csv'
PNG = ROOT / 'output' / 'Fig6.png'

# 5.42 in is 0.99 linewidth in main.tex, so the figure is placed at the size it
# is drawn and the type reaches the page unscaled.
HEIGHT, DPI = 3.3, 600

X_COLUMN = 'Simulation Time/Run Time'
COMMON_COLUMN = 'Root Mean Squared Error, common period'
COMMON_LOWER = 'RMSE 95% lower, common period'
COMMON_UPPER = 'RMSE 95% upper, common period'
SEASON_LOWER = 'RMSE 95% lower'
SEASON_UPPER = 'RMSE 95% upper'
SEASON_COLUMN = 'Root Mean Squared Error'
SEASON_END = '20.11.2024 00:00'

# What makes two rows the same configuration is defined once, beside the census
# that counts them, so the figure and the count in the article cannot disagree.
SETTINGS = list(CONFIGURATION_SETTINGS)

LAYER_COLOUR = {10: cm.viridis(0.86), 20: cm.viridis(0.55), 40: cm.viridis(0.12)}
MESH_MARKER = {2603: 'o', 4935: 's'}
MESH_LABEL = {2603: 'coarser mesh', 4935: 'finer mesh'}


def load():
    data = pd.read_csv(CSV, sep=';', header=0)
    data.columns = [c.strip() for c in data.columns]
    numeric = [X_COLUMN, COMMON_COLUMN, SEASON_COLUMN, COMMON_LOWER, COMMON_UPPER,
               SEASON_LOWER, SEASON_UPPER, 'Max Layers', '2D Cells',
               'Secchi Depth (m)', 'HMF?', 'VFF?', 'Vicoww', 'Dicoww',
               'Max Timestep (s)', 'Courant Limit']
    for column in numeric:
        data[column] = pd.to_numeric(data[column].astype(str).str.replace(',', ''),
                                     errors='coerce')
    return data


def configurations(data, column):
    """One row per distinct configuration, keeping the longest run of each."""
    kept = data[data[column].notna()].copy()
    kept = kept.sort_values('Simulation Period (h)', ascending=False)
    return kept.drop_duplicates(SETTINGS)


def panel(ax, data, column, lower, upper, label, ticks):
    # Each RMSE is estimated from a finite set of paired observations, so it
    # carries sampling uncertainty. The bars are 95% intervals obtained by
    # resampling whole days, which is what tells a reader whether two
    # configurations differ by more than the comparison can resolve.
    ax.errorbar(data[X_COLUMN], data[column],
                yerr=[data[column] - data[lower], data[upper] - data[column]],
                fmt='none', ecolor='0.62', elinewidth=0.8, capsize=1.5,
                capthick=0.8, zorder=2)

    for mesh, sub in data.groupby('2D Cells'):
        ax.scatter(sub[X_COLUMN], sub[column], marker=MESH_MARKER[mesh], s=34,
                   c=[LAYER_COLOUR[v] for v in sub['Max Layers']],
                   edgecolors='white', linewidths=0.5, zorder=3)

    ax.set_xscale('log')
    ax.set_xticks(list(ticks))
    ax.set_xticklabels([('%g' % t) for t in ticks])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_title(label, loc='left', fontsize=TITLE, pad=4)
    ax.tick_params(labelsize=TICK)
    ax.grid()
    open_frame(ax)


def build():
    use()
    data = load()
    common = configurations(data, COMMON_COLUMN)
    season = configurations(data[data['End'].str.strip() == SEASON_END], SEASON_COLUMN)
    if common.empty or season.empty:
        raise ValueError('%s: no configurations to plot; check the score columns.' % CSV)

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT), layout='constrained',
                             sharey=True)
    panel(axes[0], common, COMMON_COLUMN, COMMON_LOWER, COMMON_UPPER,
          '(a)', (200, 400, 800, 1600))
    panel(axes[1], season, SEASON_COLUMN, SEASON_LOWER, SEASON_UPPER,
          '(b)', (200, 400, 800))
    axes[0].set_ylim(0.55, 3.15)
    axes[0].set_ylabel('RMSE ($^{\\circ}$C)', fontsize=LABEL)

    handles = [plt.Line2D([], [], ls='', marker='o', color=LAYER_COLOUR[k],
                          markeredgecolor='white', markersize=5.5,
                          label='%d layers' % k) for k in (10, 20, 40)]
    handles += [plt.Line2D([], [], ls='', marker=MESH_MARKER[k], color='0.45',
                           markeredgecolor='white', markersize=5.5,
                           label=MESH_LABEL[k]) for k in (2603, 4935)]
    fig.legend(handles=handles, loc='outside upper center', ncol=5, fontsize=TICK,
               frameon=False, handletextpad=0.35, columnspacing=1.3)
    fig.supxlabel('Simulated time per unit run time (dimensionless)', fontsize=LABEL)

    PNG.parent.mkdir(parents=True, exist_ok=True)
    check_font()
    fig.savefig(PNG, dpi=DPI)
    plt.close(fig)
    print('%d configurations over the common period, %d over the season -> %s'
          % (len(common), len(season), PNG))


if __name__ == '__main__':
    build()
