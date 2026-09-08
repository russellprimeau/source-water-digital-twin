"""Figure 4: the operational model update loop, with the rates it actually runs at.

The original was a raster with no source file, authored about 12 in wide and then
included at 5.5 in, which reduced its type to roughly 3 pt on the page. This
redraw keeps its content and its loop structure but is laid out portrait at the
printed size, so nothing is scaled down.

This is the figure that carries the update rates Reviewer 2 (R2-7) asked for,
because this is the figure about the loop: retrieval cadence per platform, the
hourly model run and what it costs, the latency of the published nowcast, and
the two feedback paths — model output becoming the next update's initial
condition, and a planned mission returning to the USV by hand.

Colour denotes role, as in Figure 3 and stated in its caption: green for
instruments, orange for data and derived conditions, blue for solvers and
analysis, brick for output, gold for products.

Sources: cadences and coverage from Section 2.1 and Tables A6 and A7; run cost
and latency from Appendix E; solver configuration from Table A2.

Usage
-----
    .venv/Scripts/python src/figures/make_fig4.py [--no-png] [--dpi N]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import svgkit as k

REPO = Path(__file__).resolve().parents[2]
OUT_SVG = REPO / "docs" / "manuscript" / "Fig4.svg"
OUT_PNG = REPO / "docs" / "manuscript" / "Fig4.png"

# -- layout -----------------------------------------------------------------
FEED = 13.0                       # lane down each side for the feedback paths
LEFT_X = k.MARGIN + FEED
FULL_W = k.W - 2 * (k.MARGIN + FEED)
COL_W = (FULL_W - 12.0) / 2
RIGHT_X = LEFT_X + COL_W + 12.0
TOP_Y = 4.0
VGAP = 15.0                       # gaps carry the arrows and their labels


def build() -> k.Canvas:
    c = k.Canvas("Operational update loop of the water quality digital twin, "
                 "annotated with the rate at which each step runs")

    # ---- the platforms, and how often each publishes ----------------------
    y = TOP_Y
    h_sense = c.panel(LEFT_X, y, FULL_W, k.PHYSICAL, "SENSING PLATFORMS", None, h=47.0)
    chip_w = (FULL_W - 8 - 2 * 5) / 3
    cx = LEFT_X + 4
    for title, cadence in (("Weather station", "1 h"),
                           ("Profiler station", "1 h surface, 12 h profile"),
                           ("USV", "per mission")):
        c.box(cx, y + 13.0, chip_w, title, [cadence])
        cx += chip_w + 5.0
    c.label(LEFT_X + FULL_W / 2, y + 42.0,
            ["Automated retrieval at each platform's publication rate; "
             "range checks and provenance tagging on ingestion"],
            anchor="middle", style="italic", fill=k.PAPER, max_w=FULL_W - 8)
    sense_bottom = y + h_sense
    usv_x = cx - chip_w / 2 - 5.0

    # ---- forcing, assembled from what has been retrieved ------------------
    y = sense_bottom + VGAP
    forcing_y = y
    h_force = c.panel(LEFT_X, y, COL_W, k.DATA, "FORCING DATA", None, boxes=[
        ("Boundary conditions", ["Reassembled each update,", "gaps backfilled and tagged"]),
        ("Initial conditions", ["From the previous update"]),
    ])
    # ---- and the observations held back to judge the result ---------------
    h_truth = c.panel(RIGHT_X, y, COL_W, k.DATA, "GROUND TRUTH", None, boxes=[
        ("Withheld profiler data", ["Profiles every 12 h"]),
        ("USV survey data", ["Per mission, by hand"]),
    ])
    c.arrow(LEFT_X + COL_W / 2, sense_bottom + 1, LEFT_X + COL_W / 2, y - 1)
    c.arrow(RIGHT_X + COL_W / 2, sense_bottom + 1, RIGHT_X + COL_W / 2, y - 1)

    # ---- the run itself ---------------------------------------------------
    y += max(h_force, h_truth) + VGAP
    truth_bottom = forcing_y + h_truth
    h_solve = c.panel(LEFT_X, y, COL_W, k.COMPUTE, "MODEL SOLVERS", None, boxes=[
        ("Hourly model run", ["D-Flow FM, 12 MPI partitions", "≈ 1 s per simulated hour"]),
    ])
    c.arrow(LEFT_X + COL_W / 2, forcing_y + h_force + 1, LEFT_X + COL_W / 2, y - 1)

    # ---- what it produces -------------------------------------------------
    y2 = y + h_solve + VGAP
    h_out = c.panel(LEFT_X, y2, COL_W, k.OUTPUT, "MODEL OUTPUT", None, boxes=[
        ("3D state estimate", ["Temperature and constituent", "fields, one set per update"]),
    ])
    c.arrow(LEFT_X + COL_W / 2, y + h_solve + 1, LEFT_X + COL_W / 2, y2 - 1)
    out_mid = y2 + h_out / 2
    out_bottom = y2 + h_out

    # ---- and how it is judged --------------------------------------------
    eval_y = y2
    h_eval = c.panel(RIGHT_X, eval_y, COL_W, k.COMPUTE, "MODEL EVALUATION", None, boxes=[
        ("Error norms", ["RMSE and correlation against", "withheld observations"]),
        ("Model spread", ["Across M alternative", "configurations"]),
    ])
    c.arrow(RIGHT_X + COL_W / 2, truth_bottom + 1, RIGHT_X + COL_W / 2, eval_y - 1)
    c.arrow(LEFT_X + COL_W + 1, out_mid, RIGHT_X - 1, out_mid)
    eval_bottom = eval_y + h_eval

    # ---- the products a manager sees --------------------------------------
    y3 = max(out_bottom, eval_bottom) + VGAP
    h_prod = c.panel(LEFT_X, y3, FULL_W, k.PRODUCT, "APPLICATION OUTPUTS", None, h=46.0)
    cx = LEFT_X + 4
    for title, lines in (("Water quality nowcast", ["Published each update,", "under 2 h old"]),
                         ("Contamination analysis", ["Offline scenario runs"]),
                         ("Data collection plan", ["USV waypoints ranked", "by model spread"])):
        c.box(cx, y3 + 13.0, chip_w, title, lines)
        cx += chip_w + 5.0
    plan_x = cx - chip_w / 2 - 5.0
    c.arrow(RIGHT_X + COL_W / 2, eval_bottom + 1, RIGHT_X + COL_W / 2, y3 - 1)
    c.label(RIGHT_X + COL_W / 2 - 6.0, eval_bottom + 12.0, ["Selected configuration"],
            anchor="end", style="italic", max_w=COL_W / 2 - 8)

    # ---- the two loops ----------------------------------------------------
    # model output becomes the next update's initial condition
    lane = k.MARGIN + FEED / 2
    c.elbow([(LEFT_X - 1, out_mid), (lane, out_mid), (lane, forcing_y + h_force * 0.72),
             (LEFT_X - 1, forcing_y + h_force * 0.72)])
    c.vlabel(lane - 1.0, (out_mid + forcing_y + h_force * 0.72) / 2,
             "Initial conditions, next update", max_w=out_mid - forcing_y - 20)

    # a planned mission returns to the vessel, carried there by a person
    lane_r = k.W - k.MARGIN - FEED / 2
    c.elbow([(plan_x + chip_w / 2 + 1, y3 + h_prod * 0.62), (lane_r, y3 + h_prod * 0.62),
             (lane_r, sense_bottom - h_sense * 0.42), (usv_x + chip_w / 2 + 1,
                                                       sense_bottom - h_sense * 0.42)])
    c.vlabel(lane_r - 1.0, (y3 + h_prod * 0.62 + sense_bottom - h_sense * 0.42) / 2,
             "Mission file, uploaded by hand",
             max_w=y3 - sense_bottom + h_prod * 0.62 - 20)
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
