"""Draw the sampling-plan figure from the retained cells, clusters and route.

Panel (a) shows where the model alternatives disagree; panel (b) shows the clusters
those cells fall into and the route selected within the mission's distance budget.

The two panels are placed in one gridspec column with the colour bar in a column of
its own, so that both maps keep identical widths and their axes line up. Letting a
colour bar take its space from one panel alone would shrink that panel's box, and
because the maps carry a fixed geographic aspect ratio it would shrink in height too,
leaving the two maps aligned on neither axis.
"""
import os
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from geopy.distance import geodesic

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'sampling_plan'
OUT = ROOT / 'output' / 'Fig9.png'
# The manuscript is not part of this repository, so the caption check below runs
# only when a copy is named. The length it checks is printed either way.
MANUSCRIPT_ENV = 'MANUSCRIPT_TEX'
MANUSCRIPT_FLAG = '--manuscript'

# Sized for the journal's text width, matching the other figures in the article.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_style import (use, open_frame, check_font, WIDTH, TICK, LABEL,
                          TITLE, LEGEND)  # noqa: E402

DPI = 600

# Clear of the latitude tick labels and their axis label, so the letter sits
# outside the panel rather than over it.
LABEL_PAD = 30

# The foot of the figure, in inches, stacked upward: a margin, the line naming what
# the legend lists, the entries, then clear space before panel (b). The line is set
# close to the entries and the entries well clear of the panel, so the line groups
# with the legend rather than with the axis label above it.
FOOT, HEADER_H, HEADER_GAP, ROW_H, AXES_GAP = 0.04, 0.10, 0.04, 0.10, 0.06
SCORE = 'Model-spread score'
LAT0 = 62.47


def place(ax, xy, taken, pad=11.0):
    """Choose an offset for a label at xy that does not land on an existing one.

    Clusters that sit close together would otherwise take the same offset and print
    over each other. Candidates are tried in order of preference and the first one
    clear of everything already placed is used; if none is clear, the least bad is.
    Positions are compared in display points, because the map is far wider than it
    is tall and a separation that looks ample in degrees of longitude is not. The
    offsets are returned in points, which is what annotate wants, but the comparison
    happens in pixels: transData gives pixels, and at the resolution these figures are
    rendered at a point is several of them, so mixing the two collapses every
    separation and the labels print on top of one another anyway.
    """
    candidates = []
    for radius in (11, 17, 24, 32, 41):
        for angle in (-90, 90, -140, -40, 140, 40, 180, 0):
            rad = np.deg2rad(angle)
            candidates.append((radius * np.cos(rad), radius * np.sin(rad)))
    scale = ax.figure.dpi / 72.0                     # points to pixels
    px, py = ax.transData.transform(xy)
    best, best_clear = candidates[0], -np.inf
    for dx, dy in candidates:
        spot = (px + dx * scale, py + dy * scale)
        clear = min((np.hypot(spot[0] - tx, spot[1] - ty) for tx, ty in taken),
                    default=np.inf)
        if clear >= pad * scale:
            taken.append(spot)
            return (dx, dy)
        if clear > best_clear:
            best, best_clear = (dx, dy), clear
    taken.append((px + best[0] * scale, py + best[1] * scale))
    return best


def manuscript_path():
    """The main.tex to check the caption against, if one has been named."""
    for i, arg in enumerate(sys.argv):
        if arg == MANUSCRIPT_FLAG:
            if i + 1 >= len(sys.argv):
                raise SystemExit('%s needs a path' % MANUSCRIPT_FLAG)
            return Path(sys.argv[i + 1])
        if arg.startswith(MANUSCRIPT_FLAG + '='):
            return Path(arg.split('=', 1)[1])
    named = os.environ.get(MANUSCRIPT_ENV)
    return Path(named) if named else None


def check_caption(length):
    """Report the route length drawn, and check the caption when one is at hand.

    A number typed into a caption goes stale the first time the chain is rerun on
    different inputs, and nothing in a LaTeX build would notice. The panel title
    that used to carry it was generated, so this keeps the guarantee.

    The manuscript is not distributed with this repository. Where a copy is named,
    the check runs exactly as before; where none is, the length is still printed,
    so the value the caption has to state is never left unreported.
    """
    drawn = '%s~m' % format(round(length), ',')
    print('  route length drawn: %s' % drawn)
    manuscript = manuscript_path()
    if manuscript is None:
        print('  caption not checked: no manuscript named. Pass %s PATH or set %s'
              % (MANUSCRIPT_FLAG, MANUSCRIPT_ENV))
        return
    if not manuscript.is_file():
        raise SystemExit('%s names no such file: %s' % (MANUSCRIPT_FLAG, manuscript))
    line = next((l for l in manuscript.read_text(encoding='utf-8').splitlines()
                 if 'label{fig:planner}' in l), None)
    if line is None:
        raise SystemExit('no caption labelled fig:planner in %s' % manuscript)
    if drawn not in line:
        raise SystemExit(
            'the Figure 9 caption does not state the route length that was drawn '
            '(%s); update it in %s' % (drawn, manuscript))
    print('  caption states %s' % drawn)


def panel_label(ax, text):
    """The panel letter, to the left of the axes.

    What the panel shows belongs in the caption, which a reader has in front of
    them; the letter is only there to point at one of the two maps.
    """
    ax.annotate(text, xy=(0, 1), xycoords='axes fraction',
                xytext=(-LABEL_PAD, 0), textcoords='offset points',
                ha='right', va='top', fontsize=TITLE)


def _frame(ax, outline):
    if outline is not None:
        ax.add_collection(LineCollection(outline, color='0.6', lw=.6, zorder=1))
    ax.set_ylabel('Latitude (°N)', fontsize=LABEL)
    ax.tick_params(labelsize=TICK)
    ax.grid()
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)


def main():
    use()
    cells = pd.read_csv(DATA / '2.clustered_coordinates.csv')
    clusters = pd.read_csv(DATA / '3.cluster_info.csv').sort_values('cluster')
    route = pd.read_csv(DATA / '4.highscore_path.csv')

    outline = None
    path = DATA / 'lake_outline_segments.csv'
    if path.exists():
        outline = pd.read_csv(path).to_numpy().reshape(-1, 2, 2)

    # Extent from the lake itself, with a small margin, so the maps are not framed
    # by whatever the retained cells happen to span this time.
    if outline is not None:
        x0, x1 = outline[:, :, 0].min(), outline[:, :, 0].max()
        y0, y1 = outline[:, :, 1].min(), outline[:, :, 1].max()
    else:
        x0, x1 = cells.Longitude.min(), cells.Longitude.max()
        y0, y1 = cells.Latitude.min(), cells.Latitude.max()
    mx, my = (x1 - x0) * .04, (y1 - y0) * .12

    # Entries are short ("A: 3.96"), so lay them out across the full width rather than
    # stacking them in a narrow block: seven fit on a line at this text width.
    ncol = min(len(clusters), 7)
    legend_rows = int(np.ceil(len(clusters) / ncol))

    # The maps carry a geographic aspect, so their boxes are wide and short. Setting
    # that as a box aspect rather than a data aspect lets the layout engine pack the
    # rows against the boxes themselves; a data aspect leaves each row at whatever
    # height the grid gave it and the map floating in the middle of it.
    lon_span = (x1 - x0) + 2 * mx
    lat_span = (y1 - y0) + 2 * my
    box_aspect = (lat_span / lon_span) / np.cos(np.deg2rad(LAT0))
    # A band at the foot of the figure for the line that says what the legend
    # lists. It sits below the entries rather than above them: above, it reads as a
    # second line of the axis label belonging to panel (b).
    foot = FOOT + HEADER_H + HEADER_GAP + ROW_H * legend_rows + AXES_GAP
    height = 2 * (WIDTH * .78 * box_aspect) + 1.0 + foot

    fig = plt.figure(figsize=(WIDTH, height), dpi=DPI, layout='constrained')
    # The legend and its line sit in a band the layout engine is kept out of, so
    # that both are positioned here rather than competing with the axes for room.
    band = foot / height
    fig.get_layout_engine().set(hspace=.02, wspace=.02, h_pad=.02, w_pad=.02,
                                rect=(0, band, 1, 1 - band))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, .025])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[1, 0], sharex=ax_a, sharey=ax_a)
    cax = fig.add_subplot(gs[0, 1])
    for ax in (ax_a, ax_b):
        ax.set_box_aspect(box_aspect)

    # ── (a) where the alternatives disagree ──────────────────────────────────
    # The retained cells are the highest-scoring ones, so their normalized scores sit
    # at the top of the range; spanning the scale from zero would render them all the
    # same shade and hide the ranking the panel exists to show.
    lo = np.floor(cells[SCORE].min() * 20) / 20
    sc = ax_a.scatter(cells.Longitude, cells.Latitude, c=cells[SCORE], s=11,
                      cmap='viridis', vmin=lo, vmax=1, zorder=3, linewidths=0)
    cb = fig.colorbar(sc, cax=cax)
    cb.set_label('Normalized model spread', fontsize=LABEL)
    cb.ax.tick_params(labelsize=TICK)
    cb.outline.set_visible(False)
    panel_label(ax_a, '(a)')

    # ── (b) clusters and the selected route ──────────────────────────────────
    # tab20 rather than tab10, which would repeat once past ten clusters. Each cluster
    # also carries its letter on the map and in the legend, so identity never rests on
    # colour alone, but a repeated colour would still read as a grouping.
    palette = plt.get_cmap('tab20')
    for row in clusters.itertuples():
        d = cells[cells.cluster == row.cluster]
        ax_b.scatter(d.Longitude, d.Latitude, s=10, color=palette(row.cluster % 20),
                     label=f'{chr(65 + row.cluster)}: {row.Weight:.2f}', zorder=3,
                     linewidths=0)
    ax_b.plot(route.longitude, route.latitude, '-', color='0.15', lw=1, zorder=4)
    ax_b.plot(route.longitude, route.latitude, '.', color='0.15', ms=4, zorder=4)

    # Length from the route itself, rather than a number that goes stale whenever the
    # input changes.
    length = sum(geodesic((a.latitude, a.longitude), (b.latitude, b.longitude)).meters
                 for a, b in zip(route.itertuples(), route.iloc[1:].itertuples()))
    panel_label(ax_b, '(b)')
    check_caption(length)
    # A legend on the axes would sit under the x-axis label; one on the figure is
    # placed by the layout engine, which reserves room for it.
    handles, labels = ax_b.get_legend_handles_labels()
    fig.legend(handles, labels, ncol=ncol, fontsize=LEGEND,
               loc='lower center',
               bbox_to_anchor=(.5, (FOOT + HEADER_H + HEADER_GAP) / height),
               bbox_transform=fig.transFigure, frameon=False, handletextpad=.3,
               columnspacing=1.0, labelspacing=.35, borderpad=0, borderaxespad=0)
    fig.text(.5, FOOT / height, 'Cluster: summed normalized score',
             ha='center', va='bottom', fontsize=LEGEND)

    for ax in (ax_a, ax_b):
        _frame(ax, outline)
        ax.set_xlim(x0 - mx, x1 + mx)
        ax.set_ylim(y0 - my, y1 + my)
    ax_a.tick_params(labelbottom=False)
    ax_a.set_xlabel('')
    ax_b.set_xlabel('Longitude (°E)', fontsize=LABEL)

    # Labels are placed last, because the offsets are chosen in display coordinates
    # and those are only settled once the limits and the box aspect are.
    fig.canvas.draw()
    # The markers occupy space too. Seeding them means a label is never placed on top
    # of a cluster centroid or a route vertex, only clear of one.
    taken = [tuple(ax_b.transData.transform((lon, lat)))
             for lon, lat in zip(clusters['Longitude'], clusters['Latitude'])]
    taken += [tuple(ax_b.transData.transform((lon, lat)))
              for lon, lat in zip(route['longitude'], route['latitude'])]

    def label(text, xy, **kw):
        dx, dy = place(ax_b, xy, taken)
        # A label pushed well clear of its marker needs a line back to it, or the
        # reader has to guess which cluster it belongs to.
        arrow = (dict(arrowprops=dict(arrowstyle='-', lw=.4, color='0.45',
                                      shrinkA=1, shrinkB=2))
                 if np.hypot(dx, dy) > 16 else {})
        ax_b.annotate(text, xy, xytext=(dx, dy), textcoords='offset points',
                      ha='center', va='center', fontsize=LEGEND, **arrow, **kw)

    # Waypoint numbers go first: they carry the route, so they get the best positions.
    for row in route.iloc[:-1].itertuples():
        label(str(int(row.label)), (row.longitude, row.latitude),
              fontweight='bold', zorder=6)
    for row in clusters.itertuples():
        label(chr(65 + row.cluster), (row.Longitude, row.Latitude), zorder=5)

    check_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI)
    plt.close(fig)
    print(f'wrote {OUT}')
    print(f'  {len(cells)} cells, {len(clusters)} clusters, route {length:,.0f} m')


if __name__ == '__main__':
    main()
