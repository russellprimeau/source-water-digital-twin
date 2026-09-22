"""Draw the plume figure from the scenario simulation's full-domain field.

Three views of modelled ammonium a day and a half after the release: the surface layer over
the whole lake, the layer holding the plume over the western basin, and a vertical
section along the plume's own axis.

The field is the one src/model/VerifyScenarioProvenance.py checks the published time
series against, so both scenario figures come from the same identified simulation. That
record is a full-domain history running to tens of gigabytes and is not published. What is published
is the single output time this figure draws, half a megabyte of it, which --extract
rebuilds from the full record and the default mode reads.

Two choices are worth stating.

All three panels share one colour scale. The figure exists to show that the release does
not stay at the surface, and that comparison only reads if the panels are on the same
scale; per-panel scales would make a dilute layer look like a concentrated one.

The section runs eastwards along the plume rather than across it. A section at a fixed
longitude cuts the dilute tail and shows little; running along the plume shows the
release at the western end and the depth it occupies as it travels. Its cells are drawn
between the true sigma-layer interfaces, which follow the bed, so the section is not a
stack of equal blocks. choose_section() explains how its latitude is arrived at.

Usage:
    .venv/Scripts/python src/figures/make_fig7.py
    .venv/Scripts/python src/figures/make_fig7.py --extract --runs-dir PATH
"""

import sys
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.path import Path as MplPath
from netCDF4 import Dataset, num2date

REPO = Path(__file__).resolve().parents[2]
# The published precursor: the one timestep this figure draws, with the mesh it is
# drawn on, reduced from the full-domain record it came from.
FIELD = REPO / 'data' / 'scenario_simulation' / 'fields' / 'nh4_36h.nc'
# Where the full-domain record sits inside the solver run tree. Read only by
# --extract; the tree itself is named on the command line, not here.
EXTERNAL_MAP = Path('Nitrogen') / 'OneHourEUTROPH.dsproj_data' / 'Water_Quality' \
    / 'output' / 'deltashell_map.nc'
OUT = REPO / 'output' / 'Fig7.png'
OUTLINE = REPO / 'data' / 'sampling_plan' / 'lake_outline_segments.csv'

KEEP = ('mesh2d_face_x', 'mesh2d_face_y', 'mesh2d_node_x', 'mesh2d_node_y',
        'mesh2d_face_nodes')

SPECIES = 'mesh2d_NH4'
RELEASE_INDEX = 4          # 04:00 on 1 August, when the release begins
HOURS_AFTER = 36
# Panel (b) extent, cropped east of the plume: beyond about 900 m the field is
# uniformly near zero and only costs the plume its share of the frame.
WEST = (6.3855, 6.4190, 62.4640, 62.4745)
# The section is a straight line at one latitude, chosen by choose_section() from a
# window either side of the plume's maximum. It must cross this much water unbroken.
MIN_RUN_M = 1200.0
SECTION_SEARCH_DEG = 0.0020
SECTION_SEARCH_STEP = 0.00025
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure_style import (use, open_frame, check_font, WIDTH, TICK, LABEL,
                          TITLE, LEGEND)  # noqa: E402
sys.path.insert(0, str(REPO / 'src'))
import external_runs                                                     # noqa: E402

DPI = 600
LAT0 = 62.47
KMLON = 111320 * np.cos(np.deg2rad(LAT0))


def choose_section(polys, column_max, plume_lat):
    """Pick the latitude the section is taken at, and the cells along it.

    The section has to be a straight line at one latitude, because that is the only
    thing panel (b) can honestly mark: a line drawn at a fixed latitude and a section
    that wandered away from it would be two different objects. The line therefore has
    to lie in open water over its whole drawn length, which not every latitude does --
    the western basin narrows, and a line through the plume's own maximum runs onto
    the southern shore after a few hundred metres.

    So the latitude is chosen rather than assumed, by a stated rule: of those crossing
    the basin without interruption for at least MIN_RUN_M, take the one whose water
    holds the highest concentration. That puts the section as near the plume as an
    unbroken line can be. Returns the latitude, the cell the line passes through at
    each step, and those steps' longitudes.
    """
    boxes = np.array([[p[:, 0].min(), p[:, 0].max(), p[:, 1].min(), p[:, 1].max()]
                      for p in polys])
    paths = [MplPath(p) for p in polys]

    def cell_at(lon, lat):
        for i in np.flatnonzero((boxes[:, 0] <= lon) & (boxes[:, 1] >= lon)
                                & (boxes[:, 2] <= lat) & (boxes[:, 3] >= lat)):
            if paths[i].contains_point((lon, lat)):
                return int(i)
        return -1

    xs = np.arange(WEST[0], WEST[1], 40.0 / KMLON)
    best = None
    for lat in np.arange(plume_lat - SECTION_SEARCH_DEG, plume_lat + SECTION_SEARCH_DEG,
                         SECTION_SEARCH_STEP):
        found = [cell_at(x, lat) for x in xs]
        run, longest = [], []
        for i, c in enumerate(found):
            run = run + [i] if c >= 0 else []
            if len(run) > len(longest):
                longest = run
        if len(longest) < 2:
            continue
        span = (xs[longest[-1]] - xs[longest[0]]) * KMLON
        if span < MIN_RUN_M:
            continue
        peak = column_max[[found[i] for i in longest]].max()
        if best is None or peak > best[0]:
            best = (peak, float(lat), [found[i] for i in longest], xs[longest])
    if best is None:
        raise SystemExit('no latitude crosses the basin unbroken over '
                         f'{MIN_RUN_M:.0f} m; widen the search or lower MIN_RUN_M')
    print(f'  section at {best[1]:.5f} N, {len(best[2])} columns over '
          f'{(best[3][-1] - best[3][0]) * KMLON:.0f} m of unbroken water')
    return best[1], np.array(best[2]), best[3]


def extract(runs):
    """Reduce the full-domain record to the single timestep this figure draws."""
    source = runs / EXTERNAL_MAP
    if not source.exists():
        raise SystemExit(f'scenario field not found: {source}')
    src = Dataset(source)
    index = RELEASE_INDEX + HOURS_AFTER
    timer = src.variables['nTimesDlwq']
    FIELD.parent.mkdir(parents=True, exist_ok=True)
    with Dataset(FIELD, 'w', format='NETCDF4') as ds:
        ds.title = 'Scenario simulation: modelled ammonium at one output time'
        ds.source = source.name
        ds.time = str(num2date(timer[index], timer.units))
        ds.hours_after_release = HOURS_AFTER
        layer = src.variables[SPECIES].shape[1]
        ds.createDimension('layer', layer)
        ds.createDimension('face', len(src.dimensions['mesh2d_nFaces']))
        ds.createDimension('node', len(src.variables['mesh2d_node_x']))
        ds.createDimension('vertex', src.variables['mesh2d_face_nodes'].shape[1])
        for name, dims in ((SPECIES, ('layer', 'face')),
                           ('mesh2d_volume', ('layer', 'face'))):
            v = ds.createVariable(name, 'f8', dims, zlib=True, complevel=4)
            v[:] = np.asarray(src.variables[name][index], dtype=float)
        v = ds.createVariable('mesh2d_layer_dlwq', 'f8', ('layer',))
        v[:] = np.asarray(src.variables['mesh2d_layer_dlwq'][:], dtype=float)
        for name in KEEP:
            arr = src.variables[name][:]
            dims = ('face',) if name.endswith(('face_x', 'face_y')) else \
                   ('node',) if name.endswith(('node_x', 'node_y')) else ('face', 'vertex')
            kind = 'i4' if name == 'mesh2d_face_nodes' else 'f8'
            v = ds.createVariable(name, kind, dims, zlib=True, complevel=4,
                                  fill_value=-1 if kind == 'i4' else None)
            v[:] = np.ma.filled(np.ma.asarray(arr), -1) if kind == 'i4' else \
                np.asarray(arr, dtype=float)
    src.close()
    print(f'wrote {FIELD.relative_to(REPO)}  ({FIELD.stat().st_size / 1e6:.2f} MB)')


def main():
    use()
    if '--extract' in sys.argv:
        extract(external_runs.resolve(external_runs.argv_option(sys.argv)))
    if not FIELD.exists():
        raise SystemExit(
            f'missing {FIELD.relative_to(REPO)}; run with --extract to rebuild it '
            'from the scenario output, which is not published')
    ds = Dataset(FIELD)
    stamp = pd.Timestamp(ds.time)
    field = np.asarray(ds.variables[SPECIES][:], dtype=float)          # (layer, face)
    volume = np.asarray(ds.variables['mesh2d_volume'][:], dtype=float)
    sigma = np.asarray(ds.variables['mesh2d_layer_dlwq'][:], dtype=float)
    fx = np.asarray(ds.variables['mesh2d_face_x'][:], dtype=float)
    fy = np.asarray(ds.variables['mesh2d_face_y'][:], dtype=float)

    nx = np.asarray(ds.variables['mesh2d_node_x'][:], dtype=float)
    ny = np.asarray(ds.variables['mesh2d_node_y'][:], dtype=float)
    nodes = np.ma.filled(np.ma.asarray(ds.variables['mesh2d_face_nodes'][:]), -1).astype(int)
    nodes = np.where(nodes >= 0, nodes - nodes[nodes >= 0].min(), -1)
    polys = [np.column_stack([nx[r[r >= 0]], ny[r[r >= 0]]]) for r in nodes]

    areas = np.array([0.5 * abs(np.dot(p[:, 0] * KMLON, np.roll(p[:, 1] * 111320, -1))
                                - np.dot(p[:, 1] * 111320, np.roll(p[:, 0] * KMLON, -1)))
                      for p in polys])
    depth = np.where(areas > 0, volume.sum(axis=0) / np.maximum(areas, 1e-9), 0.0)

    peak_layer, peak_cell = np.unravel_index(field.argmax(), field.shape)
    axis_lat, cells, lons = choose_section(polys, field.max(axis=0), float(fy[peak_cell]))
    vmax = float(field.max())
    print(f'{stamp:%Y-%m-%d %H:%M}, {HOURS_AFTER} h after the release begins')
    print(f'  maximum {vmax:.5f} gN/m3 in layer {peak_layer + 1} of {len(sigma)}')
    print(f'  surface maximum {field[0].max():.5f}; section axis {axis_lat:.5f} N')

    outline = pd.read_csv(OUTLINE).to_numpy().reshape(-1, 2, 2) if OUTLINE.exists() else None

    # ── layout: one wide panel above, two narrower ones below ────────────────
    full = ((outline[:, :, 0].min(), outline[:, :, 0].max(),
             outline[:, :, 1].min(), outline[:, :, 1].max()) if outline is not None
            else (fx.min(), fx.max(), fy.min(), fy.max()))
    scale = 1 / np.cos(np.deg2rad(LAT0))
    span_a = ((full[1] - full[0]), (full[3] - full[2])) if outline is not None else (1, 1)
    aspect_a = scale * span_a[1] / span_a[0]                 # height per unit width
    aspect_b = scale * (WEST[3] - WEST[2]) / (WEST[1] - WEST[0])
    # Panel (a) spans the drawing width; (b) and (c) each span about half of it. The
    # colour bar takes roughly a tenth. Sizing the figure to what the aspect-locked
    # panels actually need keeps the leftover height from opening a band between the
    # rows, which is where constrained layout puts it otherwise.
    row_a, row_b = aspect_a * 0.88, aspect_b * 0.44
    fig = plt.figure(figsize=(WIDTH, WIDTH * (row_a + row_b) + 0.75),
                     dpi=DPI, layout='constrained')
    fig.get_layout_engine().set(h_pad=.01, hspace=.01)
    gs = fig.add_gridspec(2, 2, height_ratios=[row_a, row_b])
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    def plan(ax, values, extent, title):
        keep = [i for i in range(len(polys))
                if extent[0] <= fx[i] <= extent[1] and extent[2] <= fy[i] <= extent[3]]
        coll = PolyCollection([polys[i] for i in keep], array=values[keep], cmap='turbo',
                              edgecolors='face', linewidths=0, antialiased=False, zorder=2)
        coll.set_clim(0, vmax)
        ax.add_collection(coll)
        if outline is not None:
            ax.add_collection(LineCollection(outline, color='0.45', lw=.5, zorder=3))
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.set_aspect(1 / np.cos(np.deg2rad(LAT0)))
        ax.set_title(title, loc='center', fontsize=TITLE)
        ax.tick_params(labelsize=TICK)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        return coll

    coll = plan(ax_a, field[0], full, '(a)')
    ax_a.set_ylabel('Latitude (°N)', fontsize=LABEL)
    ax_a.set_xlabel('Longitude (°E)', fontsize=LABEL)
    plan(ax_b, field[peak_layer], WEST, '(b)')
    ax_b.set_ylabel('Latitude (°N)', fontsize=LABEL)
    ax_b.set_xlabel('Longitude (°E)', fontsize=LABEL)
    # The line in (b) is exactly the line sectioned in (c): it is drawn only over
    # the stretch that is sampled, and every column of (c) is the cell the line
    # passes through at that longitude.
    ax_b.plot([lons[0], lons[-1]], [axis_lat, axis_lat],
              color='crimson', lw=.9, zorder=4)

    # ── (c) section along that line, cells between true interfaces ───────────
    # Distance is measured along the line itself, at the evenly spaced points the
    # line was sampled at, not between the cell centres those points fell in. The
    # column that panel (c) draws at a given distance is then the cell panel (b)
    # shows the line crossing at that distance.
    east = (lons - lons[0]) * KMLON
    half_step = 0.5 * (east[1] - east[0])
    x_edge = np.concatenate([east - half_step, [east[-1] + half_step]])
    d_edge = np.interp(x_edge, east, depth[cells])
    iface = np.linspace(1.0, 0.0, len(sigma) + 1)          # sigma at layer interfaces
    y_edge = -np.outer(1 - iface, d_edge)                  # (nlayer+1, ncol+1)
    ax_c.pcolormesh(np.tile(x_edge, (len(sigma) + 1, 1)), y_edge, field[:, cells],
                    cmap='turbo', vmin=0, vmax=vmax, shading='flat', rasterized=True)
    ax_c.plot(x_edge, -d_edge, color='0.35', lw=.6)
    ax_c.set_xlabel(f'Metres east along {axis_lat:.4f}°N', fontsize=LABEL)
    ax_c.set_ylabel('Depth (m)', fontsize=LABEL)
    ax_c.set_box_aspect(aspect_b)
    ax_c.set_title('(c)', loc='center', fontsize=TITLE)
    ax_c.tick_params(labelsize=TICK)
    for side in ('top', 'right'):
        ax_c.spines[side].set_visible(False)

    bar = fig.colorbar(coll, ax=[ax_a, ax_b, ax_c], location='right',
                       fraction=.035, pad=.015)
    bar.set_label('Ammonium (gN/m$^3$)', fontsize=LABEL)
    bar.ax.tick_params(labelsize=TICK)

    check_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI)
    plt.close(fig)
    print(f'wrote {OUT}  ({len(cells)} columns in the section)')


if __name__ == '__main__':
    main()
