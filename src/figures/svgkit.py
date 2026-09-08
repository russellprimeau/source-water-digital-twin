"""Shared drawing toolkit for the manuscript's schematic figures.

Figures 1, 3 and 4 were raster PNGs whose source files were lost. They are
re-derived here as SVG, from which the 300 dpi PNGs that ``main.tex`` includes
are rasterised. The three figures share this module so that one palette, one set
of type sizes and one box style apply across all of them.

Two conventions matter.

**Colour carries meaning.** The palette is sampled from the original figures, but
each colour is now tied to one role and used for nothing else, so that a reader
who learns the key from Figure 1 can carry it into Figures 3 and 4. See
``SEMANTICS``.

**The canvas is drawn at printed size.** ``main.tex`` sets ``textwidth`` to
394.36 pt and includes each figure at 0.99\\linewidth, so a 390 pt wide canvas is
placed 1:1 and the point sizes below are the sizes that reach the page. Nothing
is scaled down, which is what made the original Figure 4 illegible: it was
authored 12 in wide and squeezed into 5.5 in, taking its type with it.

Text is measured against the real font metrics as it is placed, so a line that
would overflow its box raises rather than being silently clipped.
"""

from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# ---------------------------------------------------------------------------
# Palette, sampled from the original Fig3.png and Fig4.png
# ---------------------------------------------------------------------------
PHYSICAL = "#00B050"  # the real object and the instruments on it
DATA = "#F59D56"      # measured data, and the conditions derived from it
COMPUTE = "#0070C0"   # numerical solvers and the analysis around them
OUTPUT = "#C05046"    # what the model produces
PRODUCT = "#BF9000"   # what a decision-maker uses
INK = "#000000"
PAPER = "#FFFFFF"

SEMANTICS = {
    PHYSICAL: "real object and instruments",
    DATA: "measured data and derived conditions",
    COMPUTE: "solvers and analysis",
    OUTPUT: "model output",
    PRODUCT: "decision products",
}

SERIF = "'Latin Modern Roman','CMU Serif','STIX Two Text',STIXGeneral,'Times New Roman',serif"

# ---------------------------------------------------------------------------
# Type, in points
# ---------------------------------------------------------------------------
FS_PANEL = 9.0      # panel titles
FS_SUB = 6.4        # panel subtitles
FS_TITLE = 7.0      # box headings
FS_BODY = 6.6       # box body
FS_NOTE = 6.2       # arrow labels and footnotes

LH = 7.8            # body line height
LH_TITLE = 8.4      # gap below a box heading
PAD_V = 2.6         # padding above the first ascender and below the last descender
ASC = 0.75          # fraction of the type size taken by the ascent
DESC = 0.24         # and by the descent
RADIUS = 3.0

W = 390.0           # canvas width: 0.99\linewidth at 1:1
MARGIN = 3.0

# ---------------------------------------------------------------------------
# Text metrics: measure with the real font so overflow is caught, not clipped
# ---------------------------------------------------------------------------
_FONT_FILES = {
    ("normal", "normal"): "times.ttf",
    ("bold", "normal"): "timesbd.ttf",
    ("normal", "italic"): "timesi.ttf",
    ("bold", "italic"): "timesbi.ttf",
}


@lru_cache(maxsize=None)
def _font(weight: str, style: str, size_px: int):
    from PIL import ImageFont

    name = _FONT_FILES[(weight, style)]
    for root in (Path(r"C:\Windows\Fonts"), Path(r"C:\Windows\SysWOW64")):
        candidate = root / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size_px)
    return None


def text_width(text: str, size: float, weight: str = "normal", style: str = "normal") -> float:
    """Width of `text` in points at `size`, measured from the font itself.

    Measured at 20x and divided back down, because ImageFont only accepts an
    integer pixel size and these figures use fractional point sizes.
    """
    font = _font(weight, style, max(1, round(size * 20)))
    if font is None:                      # no Times available: fall back to an estimate
        return 0.5 * size * len(text)
    return font.getlength(text) / 20.0


class Overflow(ValueError):
    """A line of text is wider than the box it was placed in."""


def tint(colour: str, strength: float = 0.18) -> str:
    """Blend a role colour toward white, for a wash that keeps black text legible."""
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda v: round(255 - (255 - v) * strength)
    return "#%02X%02X%02X" % (mix(r), mix(g), mix(b))


@dataclass(frozen=True)
class Oval:
    """An ellipse, with the geometry needed to fit text in it and join it to others."""

    cx: float
    cy: float
    rx: float
    ry: float

    def chord(self, dy: float) -> float:
        """Full width of the ellipse at `dy` above or below its centre."""
        frac = 1.0 - (dy / self.ry) ** 2
        return 2.0 * self.rx * math.sqrt(frac) if frac > 0 else 0.0

    def toward(self, other: "Oval", trim: float = 0.0) -> tuple[float, float]:
        """The point on this boundary facing `other`, pushed out by `trim`."""
        dx, dy = other.cx - self.cx, other.cy - self.cy
        norm = math.hypot(dx, dy) or 1.0
        t = 1.0 / math.sqrt((dx / self.rx) ** 2 + (dy / self.ry) ** 2)
        return (self.cx + dx * t + dx / norm * trim,
                self.cy + dy * t + dy / norm * trim)

    def at_angle(self, deg: float) -> tuple[float, float]:
        """Boundary point at `deg`, measured clockwise from east in screen axes.

        Needed because a connector along the line joining two centres is very
        short when the ovals are large and close; routing it through the open
        wedge between their curves, as the original figure does, needs explicit
        anchors.
        """
        t = math.radians(deg)
        return (self.cx + self.rx * math.cos(t), self.cy + self.ry * math.sin(t))

    def contains(self, x: float, y: float, margin: float = 0.0) -> bool:
        """Is (x, y) inside this oval, shrunk by `margin`?"""
        rx, ry = max(self.rx - margin, 0.1), max(self.ry - margin, 0.1)
        return ((x - self.cx) / rx) ** 2 + ((y - self.cy) / ry) ** 2 <= 1.0

    def encloses(self, other: "Oval", margin: float = 2.0) -> bool:
        """Does this oval contain all of `other`, with `margin` to spare?"""
        return all(self.contains(*other.at_angle(d), margin=-margin)
                   for d in range(0, 360, 10))

    def shift(self, dx: float, dy: float) -> "Oval":
        return Oval(self.cx + dx, self.cy + dy, self.rx, self.ry)


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
class Canvas:
    """Collects SVG markup, tracking the drawn extent so height need not be guessed."""

    def __init__(self, title: str, width: float = W):
        self.title = title
        self.width = width
        self.parts: list[str] = []
        self.bottom = 0.0

    # -- primitives --------------------------------------------------------
    def add(self, markup: str) -> None:
        self.parts.append("  " + markup)

    @staticmethod
    def esc(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _note_extent(self, y: float) -> None:
        self.bottom = max(self.bottom, y)

    def rect(self, x, y, w, h, fill, stroke=INK, sw=1.0, r=RADIUS) -> None:
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self._note_extent(y + h)

    def text(self, x, y, s, size=FS_BODY, weight="normal", style="normal",
             fill=INK, anchor="middle", max_w=None, where="") -> None:
        if max_w is not None:
            got = text_width(s, size, weight, style)
            if got > max_w:
                raise Overflow(f"{where or 'text'}: {s!r} is {got:.1f} pt wide, "
                               f"{max_w:.1f} pt available")
        extra = ' font-style="italic"' if style == "italic" else ""
        extra += ' font-weight="bold"' if weight == "bold" else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}"{extra}>{self.esc(s)}</text>')
        self._note_extent(y + size * 0.3)

    def arrow(self, x1, y1, x2, y2, width=2.0, both=False, head="head") -> None:
        start = f' marker-start="url(#{head})"' if both else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{INK}" stroke-width="{width}"{start} '
                 f'marker-end="url(#{head})"/>')
        self._note_extent(max(y1, y2))

    def elbow(self, points, width=2.0) -> None:
        """Orthogonal multi-segment arrow through `points`, head on the last leg."""
        d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
                     for i, (x, y) in enumerate(points))
        self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width}" '
                 f'marker-end="url(#head)"/>')
        self._note_extent(max(y for _, y in points))

    def blocked(self, x1, y1, x2, y2, width=1.4) -> None:
        """Dashed connector struck through with a cross: a path that is *not* taken."""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{INK}" stroke-width="{width}" stroke-dasharray="3 2"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        for dx, dy in ((-1, -1, ), (-1, 1)):
            self.add(f'<line x1="{mx + dx * 3.4:.1f}" y1="{my + dy * 3.4:.1f}" '
                     f'x2="{mx - dx * 3.4:.1f}" y2="{my - dy * 3.4:.1f}" '
                     f'stroke="{INK}" stroke-width="1.6"/>')
        self._note_extent(max(y1, y2) + 4)

    # -- ellipses, for the Grieves-style framework figure -------------------
    def oval(self, e, title=None, lines=(), fill=PAPER, title_size=FS_PANEL,
             size=FS_BODY, title_dy=None, sw=1.1) -> "Oval":
        """Outlined ellipse with an optional bold title and centred text.

        Each line is checked against the ellipse's chord at its own baseline, not
        against the bounding box, so text cannot escape the curve.
        """
        self.add(f'<ellipse cx="{e.cx:.1f}" cy="{e.cy:.1f}" rx="{e.rx:.1f}" '
                 f'ry="{e.ry:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>')
        self._note_extent(e.cy + e.ry)

        if title is not None:
            ty = e.cy - e.ry + (title_size + 5.0 if title_dy is None else title_dy)
            self.text(e.cx, ty, title, size=title_size, weight="bold",
                      max_w=e.chord(ty - e.cy) * 0.92, where=f"oval title {title!r}")
        if not lines:
            return e
        # centre the block on the ellipse's centre, or below the title if there is one
        centre = e.cy + (title_size * 0.55 if title is not None else 0.0)
        lh = size * 1.2
        first = centre - (len(lines) - 1) * lh / 2 + size * 0.35
        for i, line in enumerate(lines):
            y = first + i * lh
            self.text(e.cx, y, line, size=size,
                      max_w=e.chord(y - e.cy - size * 0.35) * 0.92,
                      where=f"oval {title or lines[0]!r} line")
        return e

    def connect(self, a, b, width=2.4, both=False, trim=(1.5, 1.5), head="head") -> None:
        """Arrow between two ellipse boundaries, along the line joining centres."""
        (x1, y1), (x2, y2) = a.toward(b, trim[0]), b.toward(a, trim[1])
        self.arrow(x1, y1, x2, y2, width=width, both=both, head=head)

    def sweep(self, a, angle_a, b, angle_b, width=2.0, head="bighead",
              clear=(), min_len=20.0) -> None:
        """Arrow from a point on `a` to a point on `b`, routed through open space.

        `clear` names ovals the arrow's middle must not cross; a short or
        colliding arrow raises rather than being drawn badly.
        """
        (x1, y1), (x2, y2) = a.at_angle(angle_a), b.at_angle(angle_b)
        length = math.hypot(x2 - x1, y2 - y1)
        if length < min_len:
            raise Overflow(f"sweep is only {length:.1f} pt long, wanted {min_len:.0f}")
        for f in (0.2, 0.35, 0.5, 0.65, 0.8):
            px, py = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
            for name, oval in clear:
                if oval.contains(px, py):
                    raise Overflow(f"sweep crosses {name} at {f:.0%} along it")
        self.arrow(x1, y1, x2, y2, width=width, head=head)

    # -- composites --------------------------------------------------------
    def label(self, x, y, lines, size=FS_NOTE, anchor="start", style="normal",
              fill=INK, max_w=None) -> float:
        for i, line in enumerate(lines):
            self.text(x, y + i * (size + 1.4), line, size=size, style=style,
                      fill=fill, anchor=anchor, max_w=max_w, where="label")
        return y + (len(lines) - 1) * (size + 1.4)

    def vlabel(self, x, y, line, size=FS_NOTE, style="italic", max_w=None) -> None:
        """Label rotated to read bottom-to-top, for text set in a narrow lane."""
        if max_w is not None:
            got = text_width(line, size, "normal", style)
            if got > max_w:
                raise Overflow(f"vlabel: {line!r} is {got:.1f} pt long, "
                               f"{max_w:.1f} pt available")
        extra = ' font-style="italic"' if style == "italic" else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{INK}" '
                 f'text-anchor="middle" transform="rotate(-90 {x:.1f} {y:.1f})"'
                 f'{extra}>{self.esc(line)}</text>')

    @staticmethod
    def box_height(lines, title=None) -> float:
        """Tight to the type: padding, the first ascent, the lines, the last descent."""
        n = max(1, len(lines))
        first = (FS_TITLE if title else FS_BODY) * ASC
        body = (LH_TITLE if title else 0.0) + LH * (n - 1)
        return PAD_V + first + body + FS_BODY * DESC + PAD_V

    def box(self, x, y, w, title, lines, fill=PAPER, title_fill=INK,
            align="middle", h=None, body_fill=INK) -> float:
        """White (by default) box with an optional bold heading. Returns its height."""
        h = self.box_height(lines, title) if h is None else h
        self.rect(x, y, w, h, fill, sw=0.8, r=max(0.0, RADIUS - 1))
        tx = x + w / 2 if align == "middle" else x + 4
        avail = w - 8
        baseline = y + PAD_V + (FS_TITLE if title else FS_BODY) * ASC
        if title:
            self.text(tx, baseline, title, size=FS_TITLE, weight="bold", fill=title_fill,
                      anchor=align, max_w=avail, where=f"box title {title!r}")
            baseline += LH_TITLE
        for line in lines:
            self.text(tx, baseline, line, size=FS_BODY, anchor=align, fill=body_fill,
                      max_w=avail, where=f"box {title!r} line")
            baseline += LH
        return h

    def panel(self, x, y, w, fill, title, subtitle=None, boxes=(), gap=4.0,
              h=None) -> float:
        """Coloured region with a white title and a stack of boxes. Returns its height."""
        head = 12.6 + (7.4 if subtitle else 0.0)
        inner = sum(self.box_height(b[1], b[0]) for b in boxes) + gap * max(0, len(boxes) - 1)
        h = head + inner + 4.0 if h is None else h
        self.rect(x, y, w, h, fill)
        self.text(x + w / 2, y + 10.4, title, size=FS_PANEL, weight="bold", fill=PAPER,
                  max_w=w - 8, where=f"panel title {title!r}")
        if subtitle:
            self.text(x + w / 2, y + 18.4, subtitle, size=FS_SUB, fill=PAPER,
                      max_w=w - 8, where=f"panel subtitle {subtitle!r}")
        by = y + head
        for btitle, blines in boxes:
            by += self.box(x + 4, by, w - 8, btitle, blines) + gap
        return h

    def chip(self, x, y, w, text, fill=PAPER, size=FS_BODY, h=15.0) -> float:
        """One-line labelled box: a named component, nothing more."""
        self.rect(x, y, w, h, fill, sw=0.8, r=max(0.0, RADIUS - 1))
        self.text(x + w / 2, y + h / 2 + size * 0.36, text, size=size,
                  max_w=w - 6, where=f"chip {text!r}")
        return h

    def table(self, x, y, w, headers, rows, col_x, size=FS_NOTE) -> float:
        """Left-aligned mini table inside a white box. `col_x` are offsets from x."""
        h = 8.2 + 8.6 * len(rows) + 6.0
        self.rect(x, y, w, h, PAPER, sw=0.8, r=max(0.0, RADIUS - 1))
        base = y + 8.2
        limits = [(col_x[i + 1] - col_x[i] - 3) if i + 1 < len(col_x)
                  else (w - col_x[i] - 4) for i in range(len(col_x))]
        for cx, head, lim in zip(col_x, headers, limits):
            self.text(x + cx, base, head, size=size, weight="bold", anchor="start",
                      max_w=lim, where="table header")
        self.add(f'<line x1="{x + 3:.1f}" y1="{base + 2.2:.1f}" x2="{x + w - 3:.1f}" '
                 f'y2="{base + 2.2:.1f}" stroke="{INK}" stroke-width="0.5"/>')
        for i, row in enumerate(rows):
            ry = base + 8.6 * (i + 1) + 0.8
            for cx, cell, lim in zip(col_x, row, limits):
                self.text(x + cx, ry, cell, size=size, anchor="start",
                          max_w=lim, where="table cell")
        return h

    # -- output ------------------------------------------------------------
    def render(self, height: float | None = None) -> str:
        h = self.bottom + MARGIN if height is None else height
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width:.0f}pt" '
                f'height="{h:.0f}pt" viewBox="0 0 {self.width:.0f} {h:.0f}" '
                f'font-family={SERIF!r}>\n'
                f'  <title>{self.esc(self.title)}</title>\n'
                f'  <defs>\n'
                f'    <marker id="head" viewBox="0 0 10 10" refX="8.6" refY="5" '
                f'markerWidth="4.6" markerHeight="4.6" orient="auto-start-reverse">\n'
                f'      <path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/>\n'
                f'    </marker>\n'
                # sized in user units, so a hairline shaft can still carry a big head
                f'    <marker id="bighead" viewBox="0 0 10 10" refX="9.2" refY="5" '
                f'markerWidth="9.5" markerHeight="7.5" markerUnits="userSpaceOnUse" '
                f'orient="auto-start-reverse">\n'
                f'      <path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/>\n'
                f'    </marker>\n'
                f'  </defs>\n'
                f'{body}\n'
                f'</svg>\n')

    def write(self, path: Path, height: float | None = None) -> tuple[float, float]:
        svg = self.render(height)
        path.write_text(svg, encoding="utf-8")
        h = float(svg.split('height="', 1)[1].split('pt"', 1)[0])
        return self.width, h


# ---------------------------------------------------------------------------
# Rasterisation, via whichever Chromium-based browser is installed
# ---------------------------------------------------------------------------
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_browser() -> str:
    for candidate in BROWSERS:
        if Path(candidate).exists():
            return candidate
    for name in ("chrome", "msedge", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError(
        "No Chrome or Edge found for rasterisation. Re-run with --no-png and convert "
        "the SVG with Inkscape, rsvg-convert or another renderer."
    )


def rasterise(svg_path: Path, png_path: Path, size_pt: tuple[float, float],
              dpi: int = 300) -> tuple[int, int]:
    """Screenshot the SVG at `dpi` and stamp the resolution into the PNG."""
    w_pt, h_pt = size_pt
    # Chrome sizes its window in CSS pixels at 96 per inch; the canvas is in points
    # at 72 per inch, so the window and the device scale factor differ by 96/72.
    css_w, css_h = w_pt * 96.0 / 72.0, h_pt * 96.0 / 72.0
    scale = dpi / 96.0
    px_w, px_h = round(w_pt * dpi / 72.0), round(h_pt * dpi / 72.0)
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmp:
        wrapper = Path(tmp) / "wrap.html"
        wrapper.write_text(
            "<!doctype html><meta charset='utf-8'>"
            "<style>html,body{margin:0;padding:0;background:transparent}"
            f"svg{{display:block;width:{w_pt:.0f}pt;height:{h_pt:.0f}pt}}</style>"
            + svg_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = subprocess.run(
            [browser, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--default-background-color=00000000",
             f"--force-device-scale-factor={scale:.6f}",
             f"--window-size={round(css_w)},{round(css_h)}",
             f"--screenshot={png_path}",
             f"--user-data-dir={Path(tmp) / 'profile'}",
             wrapper.as_uri()],
            capture_output=True, text=True, timeout=180,
        )
    if not png_path.exists():
        raise RuntimeError(f"headless render produced no file:\n{result.stderr[-2000:]}")

    from PIL import Image

    with Image.open(png_path) as im:
        im.load()
        im = im.crop((0, 0, min(px_w, im.width), min(px_h, im.height)))
        im.save(png_path, dpi=(dpi, dpi))
        return im.size
