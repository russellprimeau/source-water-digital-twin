"""
make_diff.py

Build a marked-up copy of the manuscript showing what changed since an earlier
version, for a revised submission.

    .venv/Scripts/python docs/revision/make_diff.py

Reads  docs/manuscript/old.tex   (the earlier version)
       docs/manuscript/main.tex  (the current version)
Writes docs/manuscript/main-diff.tex   compile this, on Overleaf or locally

Markup:
    new text          green
    deleted text      red, struck through, shown in place
    changed float     red [changed] prefixed to its caption

The diff runs over sentences, so a paragraph in which one clause moved is
marked at that clause and not wholly repainted.

Why not latexdiff: it marks up word by word, which means writing markup inside
tabular cells, and that is what breaks tables. Here a float, an equation or a
list is one opaque unit that is never opened; only running prose is entered,
and only at sentence boundaries.

Deleted text is sanitised before it is re-inserted: \\label keys are stripped so
they cannot collide with the live ones, and math is boxed so \\sout can break
lines around it.
"""
from difflib import SequenceMatcher
from pathlib import Path
import io
import re
import sys

BS = chr(92)
NL = chr(10)

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'docs/manuscript/old.tex'
NEW = ROOT / 'docs/manuscript/main.tex'
OUT = ROOT / 'docs/manuscript/main-diff.tex'

MACROS = NL.join([
    '',
    '%% ---- revision markup, added by docs/revision/make_diff.py ----',
    BS + 'usepackage[normalem]{ulem}',
    BS + 'definecolor{diffadd}{rgb}{0,0.45,0}',
    BS + 'providecommand{' + BS + 'DIFadd}[1]{{' + BS + 'color{diffadd}#1}}',
    BS + 'providecommand{' + BS + 'DIFdel}[1]{{' + BS + 'color{red}' + BS +
    'sout{#1}}}',
    BS + 'providecommand{' + BS + 'DIFchanged}{%',
    '  ' + BS + 'par' + BS + 'noindent{' + BS + 'color{red}' + BS +
    'rule[-0.15ex]{1.1ex}{1.1ex}~' + BS + 'textbf{[changed]}}' + BS + 'par' + BS +
    'nobreak}',
    '%% ---------------------------------------------------------------',
    '',
])

# Words whose trailing period does not end a sentence.
ABBREV = {
    'e.g.', 'i.e.', 'cf.', 'al.', 'etc.', 'vs.', 'approx.', 'ca.',
    'Fig.', 'Figs.', 'Eq.', 'Eqs.', 'Sec.', 'Secs.', 'Ref.', 'Refs.',
    'No.', 'Nos.', 'Dr.', 'Prof.', 'Mr.', 'Ms.', 'Mrs.', 'St.', 'Inc.', 'Ltd.',
}

STRUCTURAL = re.compile(
    re.escape(BS) + r'(?:section|subsection|subsubsection|paragraph|appendix|'
    r'begin|end|bibliography|dataavailability|authorcontributions|funding|'
    r'institutionalreview|informedconsent|acknowledgments|conflictsofinterest|'
    r'abstract|keyword|Title|Author|address|corres|firstnote|reftitle|'
    r'PublishersNote|externalbibliography|isPreprints|documentclass|usepackage|'
    r'newcommand|providecommand|Copyright|history|item|input|include)')


def split_sentences(text):
    """Split running prose into sentences, ignoring periods inside braces,
    inside math, in decimals and in common abbreviations."""
    out, start, depth, math = [], 0, 0, False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == BS and i + 1 < n:          # escaped char, skip the pair
            i += 2
            continue
        if c == '$':
            math = not math
        elif c == '{':
            depth += 1
        elif c == '}':
            depth = max(0, depth - 1)
        elif c in '.!?' and depth == 0 and not math:
            nxt = text[i + 1:i + 2]
            after = text[i + 2:i + 3]
            digit_run = (text[i - 1:i].isdigit() and nxt.isdigit())
            word = text[max(start, text.rfind(' ', 0, i) + 1):i + 1]
            initial = len(word) == 2 and word[0].isupper()
            if (not digit_run and word not in ABBREV and not initial
                    and nxt in ' ' and after
                    and (after.isupper() or after in (BS, '$', '[', '(')
                         or after.isdigit())):
                out.append(text[start:i + 1].strip())
                start = i + 2
                i += 2
                continue
        i += 1
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return out or [text.strip()]


def blocks(lines):
    out, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].strip():
            j = i
            while j < n and lines[j].strip():
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def is_prose(text):
    """True when the block is running prose that may be entered and split."""
    if (BS + 'begin{') in text or (BS + 'end{') in text:
        return False
    if re.search(r'(?<!' + re.escape(BS) + r')%', text):   # a real comment
        return False
    return not STRUCTURAL.match(text.lstrip())


def units_of(lines, spans):
    """Flatten a document into comparable units: one per sentence of prose,
    one per opaque block."""
    units = []
    for b, (start, end) in enumerate(spans):
        text = NL.join(lines[start:end])
        if is_prose(text):
            for s in split_sentences(' '.join(text.split())):
                units.append((b, 'sent', s))
        else:
            units.append((b, 'opaque', text))
    return units


def norm(unit):
    return ' '.join(unit[2].split())


def sanitise_deleted(text):
    """Make old text safe to re-insert: no duplicate labels, boxed math."""
    text = re.sub(re.escape(BS) + r'label\{[^}]*\}', '', text)
    text = re.sub(r'(\$[^$]*\$)', lambda m: BS + 'mbox{' + m.group(1) + '}', text)
    return text.strip()


def tag_caption(text):
    at = text.find(BS + 'caption{')
    if at < 0:
        return None
    cut = at + len(BS + 'caption{')
    return text[:cut] + BS + 'DIFadd{[changed]}~' + text[cut:]


def main():
    for path in (OLD, NEW):
        if not path.exists():
            sys.exit('missing: %s' % path)

    old_lines = io.open(OLD, encoding='utf-8', errors='replace').read().split(NL)
    new_lines = io.open(NEW, encoding='utf-8', errors='replace').read().split(NL)
    old_spans, new_spans = blocks(old_lines), blocks(new_lines)
    old_units, new_units = units_of(old_lines, old_spans), units_of(new_lines, new_spans)

    # Everything before \begin{document} is preamble and is never marked.
    body_from = 0
    for k, u in enumerate(new_units):
        if (BS + 'begin{document}') in u[2]:
            body_from = k
            break

    matcher = SequenceMatcher(None, [norm(u) for u in old_units],
                              [norm(u) for u in new_units], autojunk=False)

    # marked[k] is the rendering of new unit k; pending[k] holds deleted old
    # text to emit immediately before it.
    marked = {}
    pending = {}
    stats = {'add': 0, 'del': 0, 'same': 0, 'opaque': 0}

    def add_pending(j, text):
        pending.setdefault(min(j, len(new_units) - 1), []).append(text)

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            for k in range(j1, j2):
                marked[k] = new_units[k][2]
                stats['same'] += 1
            continue
        if op in ('delete', 'replace'):
            for k in range(i1, i2):
                if k < 0 or old_units[k][1] != 'sent':
                    continue                      # never re-insert an environment
                body = sanitise_deleted(old_units[k][2])
                if body:
                    add_pending(j1, BS + 'DIFdel{' + body + '}')
                    stats['del'] += 1
        if op in ('insert', 'replace'):
            for k in range(j1, j2):
                b, kind, text = new_units[k]
                if k < body_from:
                    marked[k] = text
                elif kind == 'sent':
                    marked[k] = BS + 'DIFadd{' + text + '}'
                    stats['add'] += 1
                else:
                    tagged = tag_caption(text)
                    marked[k] = tagged if tagged is not None else (
                        BS + 'DIFchanged' + NL + text)
                    stats['opaque'] += 1

    # Reassemble, block by block, in the order of the new document.
    per_block = {}
    for k, (b, kind, text) in enumerate(new_units):
        chunks = per_block.setdefault(b, [])
        if k in pending and k >= body_from:
            chunks.extend(pending[k])
        chunks.append(marked.get(k, text))

    out, cursor = [], 0
    for b, (start, end) in enumerate(new_spans):
        out.extend(new_lines[cursor:start])
        cursor = end
        chunks = per_block.get(b)
        if not chunks:
            out.append(NL.join(new_lines[start:end]))
            continue
        joined = NL.join(chunks) if any(
            c.startswith(BS + 'DIFchanged') or (BS + 'begin{') in c
            for c in chunks) else ' '.join(chunks)
        out.append(joined)
    out.extend(new_lines[cursor:])

    body = NL.join(out)
    anchor = BS + 'begin{document}'
    at = body.index(anchor)
    io.open(OUT, 'w', encoding='utf-8').write(body[:at] + MACROS + body[at:])

    print('units: %d old, %d new' % (len(old_units), len(new_units)))
    print('unchanged %d | added %d | deleted %d | changed blocks %d'
          % (stats['same'], stats['add'], stats['del'], stats['opaque']))
    print('written: %s' % OUT)


if __name__ == '__main__':
    main()
