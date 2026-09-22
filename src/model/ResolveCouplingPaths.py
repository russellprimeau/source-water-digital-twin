"""Make the published DELWAQ input readable here and runnable elsewhere.

A DELWAQ run is forced from the hydrodynamic coupling the flow solver writes:
volumes, areas, flows, pointers, segment lengths and the vertical diffusivity, as
binary files, gigabytes apiece, so they are not published. They do not have to be: a
coupling is output of the hydrodynamic simulation, and the configuration and forcing
that produce it are published, so running D-Flow FM writes it again.

The DELWAQ input files are small text and are published as they stand: the
substance list, the numerical options, the release definition and the output
timers. One thing in them could not be published as written. Each set names its
coupling by an absolute path on the machine that produced it -- for the scenario
run, a drive belonging to a different user that no longer exists -- so those lines
describe a directory layout that is nowhere.

Every such path is therefore replaced by the token <COUPLING>, and the coupling
manifest FlowFM.hyd is published beside the input. The manifest records the
segment and exchange counts, the layer count and the time base, which is what a
regenerated coupling has to match. --resolve rewrites the token to a coupling once
one exists.

    --parameterise   rewrite absolute paths to <COUPLING>; run once at publication
    --resolve DIR    write a runnable copy of the input against a real coupling
    --check          assert no absolute path survives anywhere under data/

Usage:
    .venv/Scripts/python src/model/ResolveCouplingPaths.py --check
    .venv/Scripts/python src/model/ResolveCouplingPaths.py --resolve /path/to/DFM_DELWAQ_FlowFM \\
        --input data/scenario_simulation/waq/input --out /tmp/runnable
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
TOKEN = "<COUPLING>"

# An absolute Windows path ending in a coupling file. The directory part is what
# varies between machines; the file name is what the run actually needs.
COUPLING_PATH = re.compile(r"[A-Za-z]:[\\/][^'\"\s]*?[\\/](FlowFM\.[A-Za-z]+|FlowFM_waqgeom\.nc)")
# The generator configs record the invocation that produced each input set, which
# names the local Delft3D installation. A reader supplies their own kernel, so the
# location here is noise at best and misleading at worst.
KERNEL_PATH = re.compile(r"(--delft\s+)[A-Za-z]:[\\/][^'\"\s]*")
KERNEL_TOKEN = "<DELFT3D>"
# Any absolute path at all, for --check. The lookbehind keeps the drive-letter
# pattern from matching the "s:/" inside a URL such as https://svn.example/... ,
# which the solver writes into every .mdu as its own version identifier.
ABSOLUTE = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/home/|/Users/)[^'\"\s]*")

INPUTS = (DATA / "scenario_simulation" / "waq" / "input",
          DATA / "transport_ensemble" / "input")
CONFIGS = DATA / "transport_ensemble" / "config"


def input_files(roots=INPUTS):
    for root in roots:
        if root.exists():
            for path in sorted(root.rglob("*")):
                if path.is_file() and path.suffix.lower() in {".inc", ".inp", ".fil", ".ini"}:
                    yield path


def parameterise() -> int:
    changed = 0
    for path in input_files():
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        new = COUPLING_PATH.sub(lambda m: f"{TOKEN}/{m.group(1)}", text)
        if new != text:
            path.write_text(new, encoding="utf-8", errors="surrogateescape")
            changed += 1
    for path in sorted(CONFIGS.glob("*.json")) if CONFIGS.exists() else ():
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        new = KERNEL_PATH.sub(lambda m: m.group(1) + KERNEL_TOKEN, text)
        if new != text:
            path.write_text(new, encoding="utf-8", errors="surrogateescape")
            changed += 1
    print(f"parameterised {changed} file(s)")
    return 0


def resolve(source: Path, coupling: Path, out: Path) -> int:
    if not coupling.is_dir():
        raise SystemExit(f"not a directory: {coupling}")
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    shutil.copytree(source, out)
    target = str(coupling).replace("\\", "/").rstrip("/")
    missing, filled = set(), 0
    for path in input_files((out,)):
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        if TOKEN not in text:
            continue
        for name in re.findall(re.escape(TOKEN) + r"/([^'\"\s]+)", text):
            if not (coupling / name).exists():
                missing.add(name)
        path.write_text(text.replace(TOKEN, target), encoding="utf-8",
                        errors="surrogateescape")
        filled += 1
    print(f"wrote {out} with {filled} file(s) pointed at {target}")
    if missing:
        print("  the coupling is missing: " + ", ".join(sorted(missing)))
        print("  the run will not start until the flow solver has written them")
    return 0


def check() -> int:
    """No published file may name a path on somebody's machine."""
    offenders = []
    for path in sorted(DATA.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {
                ".inc", ".inp", ".fil", ".ini", ".json", ".ext", ".mdu", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        hits = [h for h in ABSOLUTE.findall(text)
                if TOKEN not in h and KERNEL_TOKEN not in h]
        if hits:
            offenders.append((path.relative_to(REPO), sorted(set(hits))[:3]))
    for rel, hits in offenders:
        print(f"{rel}: {hits}")
    print(f"{len(offenders)} published file(s) carry an absolute path")
    return 1 if offenders else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--parameterise", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--resolve", type=Path, metavar="COUPLING_DIR")
    ap.add_argument("--input", type=Path,
                    default=DATA / "scenario_simulation" / "waq" / "input")
    ap.add_argument("--out", type=Path, default=Path("runnable_input"))
    args = ap.parse_args()

    if args.parameterise:
        return parameterise()
    if args.resolve is not None:
        return resolve(args.input, args.resolve, args.out)
    if args.check:
        return check()
    ap.error("give one of --parameterise, --resolve or --check")


if __name__ == "__main__":
    raise SystemExit(main())
