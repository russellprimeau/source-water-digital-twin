"""Draw the scenario time-series figure from the committed scenario output.

Ammonium and nitrate at the five sites of interest, against time since the release.
The figure reads only files published with the repository, so the figure a reader sees
and the data they can download are the same thing.

The vertical scale is logarithmic because the quantity spans about ten decades: the
release cell peaks near 1 gN/m3 within the hour, while the far-field site is at 1e-11
for the first week. On a linear scale every site but the release would sit on the axis.

Usage:
    .venv/Scripts/python src/figures/make_fig8.py
"""

from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_style import use, open_frame, check_font, WIDTH  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'scenario_simulation' / 'series'
OUT = ROOT / 'output' / 'Fig8.png'

# Ten series and a ten-entry legend above the axes; the height leaves the axes
# about the depth they had before, with the type now at its page size.
HEIGHT, DPI = 3.5, 600

# The release, which sets the origin of the horizontal axis.
RELEASE = pd.Timestamp('2024-08-01 00:00:00')

SPECIES = [('NO3', '-'), ('NH4', '--')]
# File stem, and the name used in the article. Both species at a site share a colour
# and are separated by line style, so the eye groups by place first.
SITES = [
    ('Source', 'Blast Site'),
    ('Spjelkavikelva', 'Spjelkavikelva'),
    ('Vasstrandlia', 'Vasstrandlia Pump Intake'),
    ('Profiler', 'Profiler'),
    ('FarField', 'Nørebotnen'),
]


def series(species, site):
    frame = pd.read_csv(DATA / f'{species}{site}.csv')
    time = pd.to_datetime(frame.iloc[:, 0], format='%Y.%m.%d %H:%M:%S')
    return (time - RELEASE).dt.total_seconds() / 86400.0, frame.iloc[:, 1]


def main():
    missing = [f'{s}{site}.csv' for s, _ in SPECIES for site, _ in SITES
               if not (DATA / f'{s}{site}.csv').exists()]
    if missing:
        raise SystemExit(f'missing committed series: {", ".join(missing)}')

    use()
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT), layout='constrained')
    palette = plt.get_cmap('jet')
    # Species-major, so the two legend columns separate nitrate from ammonium while
    # colour still carries the site.
    for species, style in SPECIES:
        for index, (site, label) in enumerate(SITES):
            days, values = series(species, site)
            ax.semilogy(days, values, style, color=palette(index / len(SITES)),
                        label=f'{label}, {species}')

    ax.set_xlabel('Days post-incident')
    ax.set_ylabel('Concentration (gN/m$^3$)')
    ax.grid(True)
    open_frame(ax)
    # Two columns, so nitrate and ammonium line up as a pair for each site.
    ax.legend(ncol=2, loc='lower center', bbox_to_anchor=(.5, 1.02), frameon=True)
    check_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI)
    plt.close(fig)

    print(f'wrote {OUT}')
    print(f'  {len(SITES)} sites, {len(SPECIES)} species, '
          f'{len(series("NO3", "Source")[0])} timesteps')


if __name__ == '__main__':
    main()
