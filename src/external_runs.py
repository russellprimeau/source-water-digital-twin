"""Locate the solver run tree that --extract reads.

The repository publishes the small precursor files every default run needs, so
nothing here is required to regenerate a result in the article.  --extract
rebuilds those precursors from the solver's own output instead, which runs to
tens of gigabytes and is not published.

Where that output sits is a property of a machine, not of the work, so it is
named on the command line or in the environment rather than written into a
script.  Nothing is assumed: if the tree has not been named, --extract stops
and says so rather than guessing at a path or quietly producing nothing.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_VAR = "D3DFM_RUNS"
FLAG = "--runs-dir"

_UNSET = (
    "--extract needs the {what}, which is outside this repository and is not\n"
    "published.  Name it with {flag} PATH, or set {env}.\n"
    "Default runs read the committed precursors and need none of this."
)

_MISSING = "{flag} names a directory that does not exist: {path}"


def _tree(value, env, flag, what):
    """A named directory, from `value` if given, else from the environment.

    Raises SystemExit naming both ways of setting it when neither is present,
    and again when the directory named does not exist.
    """
    named = value or os.environ.get(env)
    if not named:
        raise SystemExit(_UNSET.format(what=what, flag=flag, env=env))
    path = Path(named).expanduser()
    if not path.is_dir():
        raise SystemExit(_MISSING.format(flag=flag, path=path))
    return path


def resolve(value: str | os.PathLike[str] | None = None) -> Path:
    """The solver run tree: the directory holding one subdirectory per run."""
    return _tree(value, ENV_VAR, FLAG, "solver run tree")


def argv_option(argv, flag: str = FLAG) -> str | None:
    """Pull `--runs-dir VALUE` or `--runs-dir=VALUE` out of a plain argv scan.

    For the scripts that test for --extract in sys.argv directly rather than
    building an argparse parser.
    """
    for i, arg in enumerate(argv):
        if arg == flag:
            if i + 1 >= len(argv):
                raise SystemExit("%s needs a path" % flag)
            return argv[i + 1]
        if arg.startswith(flag + "="):
            return arg.split("=", 1)[1]
    return None
