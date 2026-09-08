# Change List for Red Highlighting

Line numbers refer to `docs/manuscript/main.tex` as compiled on 2026-09-08 (34 pages).
Regenerated after the full revision; supersedes the earlier Phase 0 and 1 version, whose line numbers are obsolete.

Wrap the indicated passages in `\textcolor{red}{...}` in Overleaf. Sorted by position in the manuscript.

| `main.tex` line | Section | What changed | Action |
|---|---|---|---|
| 54 | Abstract | Validation scope, plus measured RMSE 1.7 C and r 0.96 | HIGHLIGHT |
| 71 | 1. Introduction | Contribution relative to the earlier paper | HIGHLIGHT |
| 73 | 1. Introduction | SSRN preprint declaration | HIGHLIGHT |
| 107 | 1.2 Digital Twins | Novelty claim qualified, new citations | HIGHLIGHT |
| 115 | Figure 2 caption | Projection, centre point and base imagery added | HIGHLIGHT |
| 137 | 2.1 Sensing Systems | Pointer to merged instrument table | HIGHLIGHT |
| 147 | 2.1 Sensing Systems | Battery claim replaced by endurance specification | HIGHLIGHT |
| 159 | 2.2 HWQM | Two-stage calibration, objective and search described | HIGHLIGHT |
| 207 | 2.2 HWQM | Turbulence closure named and cross-referenced | HIGHLIGHT |
| 226 | 2.2 HWQM | Withheld-data decision promoted to its own paragraph | HIGHLIGHT |
| 228 | 2.2 HWQM | Latency reattributed, measured run timings | HIGHLIGHT |
| 260 | 2.3 Path planning | Battery wording removed | HIGHLIGHT |
| 271 | 2.3 Path planning | Eq. 8 normalisation applied consistently | HIGHLIGHT |
| 285 | 2.3 Path planning | Dmax justified by mission duration | HIGHLIGHT |
| 315 | 2.4 Case Study | Hydrological reconstruction and non-independence caveat | HIGHLIGHT |
| 343 | 3.1 Nowcast | Fig 6 axis defined, scaling corrected, error bars | HIGHLIGHT |
| 347 | 3.1 Nowcast | Criteria referenced to a published benchmark | HIGHLIGHT |
| 349 | 3.1 Nowcast | Full-season results and new performance table | HIGHLIGHT |
| 375 | 3.2 Hazard | Scope of chemical validation stated | HIGHLIGHT |
| 387 | 3.2 Hazard | Denitrification stoichiometry corrected | HIGHLIGHT |
| 399 | 3.2 Hazard | Reaction rate formulation and citation | HIGHLIGHT |
| 401 | 3.2 Hazard | Weather gap-filling described | HIGHLIGHT |
| 405 | 3.2 Hazard | Boom claim reframed as an inference | HIGHLIGHT |
| 409 | 3.2 Hazard | Background comparison and intake conclusion | HIGHLIGHT |
| 411 | 3.2 Hazard | Mass balance pointer | HIGHLIGHT |
| 427 | 3.3 Data Collection | 100 m clustering threshold justified | HIGHLIGHT |
| 427 | 3.3 Data Collection | Terminology, 51 cells, what sigma measures | HIGHLIGHT |
| 428 | 3.3 Data Collection | 6 km constraint justified | HIGHLIGHT |
| 430 | 3.3 Data Collection | Stability pointer | HIGHLIGHT |
| 432 | 3.3 Data Collection | Route was not flown | HIGHLIGHT |
| 446 | 4. Discussion | Measured gap fractions | HIGHLIGHT |
| 448 | 4. Discussion | Equifinality limitation | HIGHLIGHT |
| 457 | 5. Conclusions | Prototype-maturity qualifier | HIGHLIGHT |
| 459 | 5. Conclusions | Transferability softened | HIGHLIGHT |
| 476 | Data Availability | Rewritten: restricted data and third-party software | HIGHLIGHT |
| 516 | Appendix A | Merged instrument table and turbidity discussion | HIGHLIGHT |
| 549 | Appendix B | NEW table: model configuration | NEW, highlight whole table |
| 615 | Appendix B | NEW table: tuned parameters, bounds, selected values | NEW, highlight whole table |
| 636 | Appendix C | NEW appendix: per-depth validation, Figures 11 to 13 | NEW, highlight whole appendix |
| 681 | Appendix D | NEW appendix: whole-domain mass balance | NEW, highlight whole appendix |
| 714 | Appendix E | NEW appendix: automation, coverage, latency | NEW, highlight whole appendix |
| 785 | Appendix F | NEW appendix: leave-one-out, bootstrap, co-association | NEW, highlight whole appendix |

## Not listed

Mechanical fixes with no rendered effect: added labels, the Section prefix on a cross-reference, the Fig./Figure wording, removal of the dead abstract and adjustwidth comments, and deletion of four dummy bibliography entries plus one duplicate.

`sources.bib`: 79 entries had a doubled DOI prefix, all normalised. A correction, not a revision, so do not highlight.

New bibliography entries: `kwon2025hybrid`, `primeau2025preprint`.

Regenerated figures: Figure 6 (full-season runs only, error bars, defined axis) and Figures 11 to 13 (new).

## Outstanding, not yet in the manuscript

| Item | Source | Status |
|---|---|---|
| Figure 1 annotation with update rates | R2-7 | Raster image, no source file in any repo |
| Figure 3 redraw showing the withheld-data path | R2-7 | Raster image, no source file; substance handled in prose |
| Calibration/validation period split | R1-4, R3-2 | Open by choice; the letter offers to add it |
| Transport-specific mesh convergence | R2-10 | Declined as out of scope, stated as future work |
| Resampling over model configurations | R2-3 | Per-configuration fields not retained, stated as future work |
| Commit the 5.45 MB model configuration | R3-5 | Files un-ignored but not committed; the DAS is false until they are |

## TODO comments remaining in `main.tex`

These are comments and do not render.

- L73: TODO(author): state in one sentence what is new here relative to the preprint. Claude could not verify the preprint's contents and has deliberately le
- L383: TODO(author): state explicitly whether 3.5 kg is the total mass of the compounds or the mass of nitrogen, and give the resulting source loading in gN.
- L402: TODO(author): the previous draft described this gap-filling as 'seasonally appropriate historical weather data from the digital twin's database of sen
- L427: TODO(Phase 2/5): state the mesh spacing explicitly once the mesh used for the nitrogen runs is confirmed.
- L476: TODO(author): if a DataverseNO deposit is created, add its DOI here. The DOI 10.18710/6CD1B5 previously drafted for this statement is not registered a
- L478: TODO(before submission): this statement asserts that the model configuration is in the repository. The 35 files (5.45 MB: mesh, .mdu, .ext, boundary a
- L521: TODO(author): Reviewer 2 also asked for manufacturer accuracy and resolution columns here.
