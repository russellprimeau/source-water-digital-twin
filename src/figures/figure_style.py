"""
figure_style.py

One house style for the data-driven figures, so that no two of them can disagree
about type size, line weight or typeface.

    from figure_style import use, WIDTH
    use()

Why this exists. Each figure is drawn on its own canvas and then scaled to the
text block by \\includegraphics, so a size set in a script reaches the page
multiplied by that scale. Figures drawn wide and shrunk hard therefore printed
much smaller type than figures drawn at the width they are placed at, even where
both asked for the same number. Drawing every figure at WIDTH removes the scale
factor, after which a point set here is a point on the page.

The manuscript is set in Palatino: the MDPI class loads mathpazo, and the
compiled PDF embeds URW Palladio L. The figures follow it rather than sitting in
matplotlib's sans-serif default beside a serif page. FONT_STACK is tried in
order and ends in DejaVu Serif, which ships with matplotlib, so a machine with no
Palatino installed still gets a serif rather than silently reverting to sans.
"""
from pathlib import Path
import warnings

import matplotlib
from matplotlib import font_manager

# 0.99 of \textwidth, which main.log reports as 394.36 pt. Every data figure is
# placed at that width, so drawing at it makes the scale factor one.
WIDTH = 5.42

# Point sizes as they reach the page.
TICK, LABEL, TITLE, LEGEND = 7, 8, 9, 7

# Line weights, chosen mid-range of what the figures used before so that none of
# them changes much.
GRID_LW, GRID_ALPHA = 0.4, 0.2
SPINE_LW = 0.6
TRACE_LW = 0.6
PROXY_LW = 0.9          # the legend's sample line, drawn a little heavier to read

GAP_GREY = '0.85'       # shading over intervals without observations
TRACE = '#26343f'       # single-series traces, where colour carries nothing

FONT_STACK = ['Palatino Linotype', 'Book Antiqua', 'P052', 'URW Palladio L',
              'TeX Gyre Pagella', 'DejaVu Serif']


def resolved_font():
    """The first family in the stack that this machine actually has.

    Resolved once here rather than left to matplotlib, which otherwise retries
    the whole stack for every text object and warns on each miss.
    """
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in FONT_STACK:
        if name in installed:
            path = font_manager.findfont(font_manager.FontProperties(family=name))
            return name, Path(path).name
    raise SystemExit('none of %s is installed, and DejaVu Serif ships with '
                     'matplotlib, so something is wrong with the font cache'
                     % (FONT_STACK,))


def use(report=True):
    """Apply the house style. Call once, before anything is drawn."""
    family, filename = resolved_font()
    matplotlib.rcParams.update({
        'font.family': family,
        # Mathtext follows the same family, so a degree sign or an exponent in an
        # axis label is set in the label's own face.
        'mathtext.fontset': 'custom',
        'mathtext.rm': family,
        'mathtext.it': family + ':italic',
        'mathtext.bf': family + ':bold',
        'font.size': LABEL,
        'axes.labelsize': LABEL,
        'axes.titlesize': TITLE,
        'xtick.labelsize': TICK,
        'ytick.labelsize': TICK,
        'legend.fontsize': LEGEND,
        'figure.titlesize': TITLE,
        'axes.linewidth': SPINE_LW,
        'xtick.major.width': SPINE_LW,
        'ytick.major.width': SPINE_LW,
        'xtick.minor.width': SPINE_LW,
        'ytick.minor.width': SPINE_LW,
        'grid.linewidth': GRID_LW,
        'grid.alpha': GRID_ALPHA,
        'lines.linewidth': TRACE_LW,
    })
    if report:
        print('figure style: %s (%s), %g in wide, %g pt ticks'
              % (family, filename, WIDTH, TICK))


def open_frame(ax):
    """Drop the top and right spines, which enclose nothing."""
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)


def check_font():
    """Fail if the figure was not drawn in the family use() selected.

    A missing font is not an error in matplotlib: it warns and substitutes, so a
    figure can come back set in the wrong face with nothing in the output to say
    so. Called by each script after drawing.
    """
    wanted = matplotlib.rcParams['font.family']
    wanted = wanted[0] if isinstance(wanted, list) else wanted
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        path = font_manager.findfont(font_manager.FontProperties(family=wanted))
        missed = [str(w.message) for w in caught if 'findfont' in str(w.message)]
    got = font_manager.FontProperties(fname=path).get_name()
    if missed or got != wanted:
        raise SystemExit('figure set in %r, not the requested %r %s'
                         % (got, wanted, missed))
