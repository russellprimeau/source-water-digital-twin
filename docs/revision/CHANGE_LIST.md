# Change List for Red Highlighting

**Status: superseded, and deliberately not regenerated.**

Earlier versions of this file listed individual passages to highlight, each located by
matching an anchor phrase in `main.tex`. That approach assumed the revision was a set of
discrete edits to an otherwise stable draft. It no longer is: of the 52 anchors tracked
before the manual revision of 8 September, **16 still match and 36 do not**, because the
affected sections were rewritten rather than amended.

A passage-level list built from the 16 survivors would imply that everything unlisted is
unchanged. That is false, and it would mislead a reviewer checking the highlighting
against the previous submission.

## Recommended alternative

Highlight whole sections. Substantially rewritten since submission:

- Abstract
- Section 1.2 (digital twins, novelty claim) and Section 1.3 (modelling approach)
- Section 2.2 (HWQM, calibration scope)
- Sections 3.1, 3.2 and 3.3 (all results)
- Section 4 (Discussion) and Section 5 (Conclusions)
- Data Availability Statement
- Appendices A through F, of which B, C, D, E and F are new

New or redrawn figures: 1, 3, 4, 6 and 14.

## On latexdiff

A mechanical diff would be preferable to any hand-maintained list, and `latexdiff` ships
with the MiKTeX installation on this machine. **It does not currently run:** it aborts
with `Can't locate Algorithm/Diff.pm in @INC`, so the Perl module it depends on is not
installed. If that module is installed, a marked-up PDF can be produced directly from the
submitted version held in the manuscript repository history:

    latexdiff OLD.tex main.tex > diff.tex
    latexmk -pdf diff.tex

This marks every insertion and deletion mechanically, so nothing depends on a list being
kept current by hand.

## Outstanding, not in the manuscript

| Item | Source | Status |
|---|---|---|
| Calibration/validation period split | R1-4, R3-2 | Open by choice; the letter states this |
| Transport-specific mesh convergence | R2-10 | Declined as out of scope, stated as future work |
| Resampling over model configurations | R2-3 | Per-alternative fields not retained, stated as future work |
| Figure payload | submission | `main.pdf` is 25.5 MB; Figure 2 alone is 19 MB. Likely over the journal limit |
| Repository consolidation | R3-5 | Shared helper modules and one-command figure regeneration not implemented |
| Figure 4 latency annotation | consistency | The figure still shows a nowcast "under 2 h old" while the text now states the full interval was never measured |

## TODO comment remaining in `main.tex`

This is a comment and does not render.

- L493: `TODO(author): Reviewer 2 also asked for manufacturer accuracy and resolution
  columns here.`
