"""Figure 3: what goes into the hydrodynamic water quality model and what comes out.

The original was a raster with no source file. This redraw keeps its content and
its left-to-right reading — conditions, then solvers, then output — and adds the
one thing Reviewer 2 (R2-7) said it omitted: the decision about profiler data.
The first profile of the season sets the initial temperature field; every later
profile is held back for validation and model selection and never forces the
model. That is drawn here as a taken path and a blocked one, so the separation
is visible rather than only stated in Section 2.2.

Colour denotes role, as stated in this figure's caption: green for instruments,
orange for data and the conditions derived from it, blue for solvers and
analysis, brick for output. Figure 1 is the author's own drawing and is plain
black on white, so the key is introduced here.

Equation numbers refer to the manuscript: Eq. 1 is the advection-diffusion-
reaction equation, Eqs. 2-6 the hydrodynamic system.

Usage
-----
    .venv/Scripts/python src/figures/make_fig3.py [--no-png] [--dpi N]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import svgkit as k

REPO = Path(__file__).resolve().parents[2]
OUT_SVG = REPO / "docs" / "manuscript" / "Fig3.svg"
OUT_PNG = REPO / "docs" / "manuscript" / "Fig3.png"

# -- layout: two columns, then the observation path along the bottom --------
COL_W = 186.0
LEFT_X = k.MARGIN
RIGHT_X = k.W - k.MARGIN - COL_W
TOP_Y = 4.0
VGAP = 6.0


def build() -> k.Canvas:
    c = k.Canvas("Inputs, solvers and outputs of the hydrodynamic water quality "
                 "model, showing which observations force it and which validate it")

    # ---- left column: everything that must be specified before a run ------
    # Initial conditions sit at the foot of the column, next to the observations
    # that set them, so the profile path need not cross anything.
    y = TOP_Y
    h_bc = c.panel(LEFT_X, y, COL_W, k.DATA, "BOUNDARY CONDITIONS", None, boxes=[
        ("Atmospheric conditions", ["Wind speed and direction",
                                    "Shortwave radiation",
                                    "Precipitation, humidity",
                                    "Air pressure"]),
        ("Point sources", ["Eight tributary inflows",
                           "Abstraction and outlet",
                           "Contaminant sources and sinks"]),
    ])
    bc_mid = y + h_bc / 2
    y += h_bc + VGAP
    ex_mid = y
    h_ex = c.panel(LEFT_X, y, COL_W, k.DATA, "MODEL EXTENTS", None, boxes=[
        (None, ["Bathymetry, mesh, vertical layers"]),
    ])
    ex_mid = y + h_ex / 2
    y += h_ex + VGAP
    ic_y = y
    h_ic = c.panel(LEFT_X, y, COL_W, k.DATA, "INITIAL CONDITIONS", None, boxes=[
        ("State variables", ["Temperature, velocity,",
                             "contaminant concentration"]),
    ])
    ic_mid = y + h_ic / 2
    left_bottom = y + h_ic

    # ---- right column: the solvers, and what they produce -----------------
    y = TOP_Y
    h_pm = c.panel(RIGHT_X, y, COL_W, k.COMPUTE, "PROCESS MODELS", "numerical solvers",
                   boxes=[
                       (None, ["Hydrodynamics, Eqs. 2–6"]),
                       (None, ["Heat transport, Eq. 1"]),
                       (None, ["Mass transport, Eq. 1"]),
                   ])
    solver_top, solver_bottom = y, y + h_pm
    y += h_pm + VGAP
    out_y = y
    h_out = c.panel(RIGHT_X, y, COL_W, k.OUTPUT, "MODEL OUTPUT", None, boxes=[
        ("State variables", ["Temperature, velocity,",
                             "contaminant concentration"]),
        ("Trans-boundary variables", ["Outgoing radiation, evaporation,",
                                      "outflows"]),
    ])
    right_bottom = y + h_out

    # conditions feed the solvers: one bus collecting all three, into the stack
    bus_x = LEFT_X + COL_W + 6.0
    mid = solver_top + h_pm / 2
    c.add(f'<path d="M {LEFT_X + COL_W:.1f} {bc_mid:.1f} L {bus_x:.1f} {bc_mid:.1f} '
          f'L {bus_x:.1f} {ic_mid:.1f} L {LEFT_X + COL_W:.1f} {ic_mid:.1f}" fill="none" '
          f'stroke="{k.INK}" stroke-width="1.6"/>')
    c.add(f'<line x1="{bus_x:.1f}" y1="{ex_mid:.1f}" x2="{LEFT_X + COL_W:.1f}" '
          f'y2="{ex_mid:.1f}" stroke="{k.INK}" stroke-width="1.6"/>')
    c.arrow(bus_x, mid, RIGHT_X - 1, mid)

    # solvers advance into the output
    c.arrow(RIGHT_X + COL_W / 2, solver_bottom + 1, RIGHT_X + COL_W / 2, out_y - 1)

    # ---- bottom: the observations, and the two things done with them ------
    y = max(left_bottom, right_bottom) + 27.0
    obs_w = 150.0
    h_obs = c.panel(LEFT_X, y, obs_w, k.PHYSICAL, "PROFILER OBSERVATIONS", None, boxes=[
        (None, ["Vertical profiles, every 12 h"]),
    ])
    val_x = RIGHT_X
    h_val = c.panel(val_x, y, COL_W, k.COMPUTE, "VALIDATION AND MODEL SELECTION",
                    None, boxes=[
                        (None, ["Error norms against withheld data"]),
                    ])
    bottom = y + max(h_obs, h_val)
    obs_mid = y + h_obs / 2

    # the taken path: the first profile of the season, straight up into the
    # initial conditions immediately above
    up_x = LEFT_X + 40.0
    c.arrow(up_x, y - 1, up_x, left_bottom + 1)
    c.label(up_x + 5, y - 20.0, ["First profile of the season"], style="italic",
            max_w=LEFT_X + obs_w - 18.0 - (up_x + 5))

    # the taken path: every later profile, into validation
    c.arrow(LEFT_X + obs_w + 1, obs_mid, val_x - 1, obs_mid)
    c.label((LEFT_X + obs_w + val_x) / 2, obs_mid - 4.5, ["All later"],
            anchor="middle", style="italic")

    # model output is what the withheld profiles are compared against
    c.arrow(RIGHT_X + COL_W - 24.0, right_bottom + 1, RIGHT_X + COL_W - 24.0, y - 1)

    # the path deliberately not taken: the profiles never join the forcing bus
    c.blocked(LEFT_X + obs_w - 13.0, y - 2, bus_x, left_bottom + 2.0)
    c.label(bus_x - 2, y - 5.0, ["Never forcing"], anchor="end", style="italic",
            max_w=60.0)

    c.label(LEFT_X + 2, bottom + 10.0,
            ["No profiler observation used to evaluate the model also drives it."],
            style="italic", max_w=k.W - 2 * k.MARGIN - 4)
    return c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    size = build().write(OUT_SVG)
    print(f"wrote {OUT_SVG.relative_to(REPO)}  ({size[0]:.0f} x {size[1]:.0f} pt)")
    if args.no_png:
        return 0
    px = k.rasterise(OUT_SVG, OUT_PNG, size, args.dpi)
    print(f"wrote {OUT_PNG.relative_to(REPO)}  ({px[0]} x {px[1]} px at {args.dpi} dpi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
