"""Regenerate every schematic figure in the manuscript.

    .venv/Scripts/python src/figures/make_all.py [--no-png] [--dpi N]

Figures 3 and 4 are schematics with no data behind them, drawn by the scripts in
this directory. Figure 1 is the author's own drawing and is not generated here.
The remaining figures are plots of model output or map data and are produced
elsewhere in `src/`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import svgkit as k
import make_fig3
import make_fig4

FIGURES = (make_fig3, make_fig4)
REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-png", action="store_true", help="write only the SVG sources")
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    for module in FIGURES:
        size = module.build().write(module.OUT_SVG)
        print(f"wrote {module.OUT_SVG.relative_to(REPO)}  "
              f"({size[0]:.0f} x {size[1]:.0f} pt)")
        if args.no_png:
            continue
        px = k.rasterise(module.OUT_SVG, module.OUT_PNG, size, args.dpi)
        print(f"wrote {module.OUT_PNG.relative_to(REPO)}  "
              f"({px[0]} x {px[1]} px at {args.dpi} dpi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
