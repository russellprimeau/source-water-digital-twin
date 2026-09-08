# Revision Tracker — *A Digital Twin Prototype for Protecting Surface Source Waters*

Point-by-point disposition of all 36 reviewer comments. **This file is the working record and the source for the response letter.** Update the Status column as each item lands.

- Manuscript: `docs/manuscript/main.tex` (git submodule → Overleaf). **This tracker lives in `Postprocess`, not the submodule**, so it is not published to Overleaf.
- Baseline PDF built 2026-09-04: 23 pages. After Phase 0+1: 24 pages. Build clean, zero undefined references or citations.
- Plan: `~/.claude/plans/docs-manuscript-main-tex-and-related-fi-distributed-nautilus.md`

**Disposition key** — `Accept` · `Partial` (accept in substance, decline the requested form or extent) · `Decline` (justify, do not implement) · `Deferred` (agreed, blocked on data or a later phase)

**Status key** — ☐ not started · ◐ in progress · ☑ done · ⏸ blocked

---

## Reviewer line-number → `main.tex` mapping

Reviewer 1 cites line numbers from the submitted PDF. Verified against the baseline build at 20 independent anchors:

| PDF lines | `main.tex` | Content |
|---|---|---|
| 1–19 | 55 | Abstract |
| 58–69 | 74 | Contributions paragraph |
| 176–183 | 108 | Novelty claim |
| 327–346 | 238 | Profiler data withheld from forcing |
| 335–348 | 240–242 | Ensemble / update loop |
| 368–377 | 262 | Iterative parameter tuning |
| 475–479 | 325 | Hydrological calibration omitted |
| 490–519 | 341–351 | Temperature validation, criteria |
| 510–516 | 351 | RMSE < 1 °C, r > 0.95 criteria |
| 533–556 | 363–377 | 3.5 kg release, Eqs. 11–12 |
| 557–561 | 379 | Historical + 2024 weather splice |
| 564–589 | 381–385 | Plume interpretation, boom sufficiency |
| 596–603 | 396 | Three alternative predictions |
| 604–617 | 398 | 50 cells, 100 m, 6 km |
| 618–623 | 400 | Mission file export |
| 638–644 | 414 | Missing / unreliable sensor data |
| 645–657 | 416–418 | Limitations |
| 659–665 | 423 | Conclusions |
| 666–675 | 425–427 | Transferability |
| 717–718 | 442 | Data Availability Statement |

---

## Reviewer 1 — minor revision (20 comments)

> *Summary:* "I found the manuscript interesting and generally well prepared… The main methodology is reasonably sound for a prototype study, and the manuscript already discusses several of its limitations in a transparent way. The comments above are mainly intended to improve reproducibility, clarify the level of validation, and avoid a few claims being interpreted more strongly than the available results support."

| ID | Ask (abridged) | Disposition | Plan item | Where | Status |
|---|---|---|---|---|---|
| R1-1 | Add 1–2 quantitative results to the abstract (RMSE, r, or latency) | Accept | 1D + 2A | L54 | ☑ RMSE 1.7 / r 0.96 now in the abstract |
| R1-2 | State novelty vs. the authors' own previous work more explicitly | Accept | 1C | L72 | ☑ |
| R1-3 | "No existing DTs for surface drinking-water reservoirs" is too strong — support or moderate | Accept | 1A | L108 | ☑ |
| R1-4 | Clarify separation of calibration / model selection / independent validation | Accept | 3B | L238, §2.2 | ☐ open by choice; letter offers to add it |
| R1-5 | Ensemble details: how many members, what varied, how ranges chosen | Accept | 2B | §2.2 | ☑ §2.2 two-stage description + Table A3 |
| R1-6 | Iterative parameter tuning: main parameters, ranges, stopping criterion | Accept | 2B | L262 | ☑ §2.2 objective, search, budget; Table A3 |
| R1-7 | Summarize hydrological calibration + performance indicators without disclosing restricted data | Partial | 3G | L325 | ☑ §2.4 procedure + aggregate indicators |
| R1-8 | Give numerical performance of the final configuration in text or a small table (RMSE, r, MAE, computation time) | Accept | 2A | §3.1 | ☑ Table 6, full-season |
| R1-9 | Were RMSE < 1 °C and r > 0.95 set before or after seeing results? | Accept | 1J | L337 | ☑ |
| R1-10 | Is 3.5 kg compound or N mass? Check Eqs. 11–12; add a reference for the reaction expressions | Accept | 1I | L350, L371-383 | ☑ |
| R1-11 | Explain how historical and 2024 weather data were combined; any discontinuity? | Accept | 3H | L379 | ☑ §3.2 gap-filling described |
| R1-12 | Mark intervention statements as simulation-derived, not experimentally demonstrated | Accept | 1D | L387 | ☑ |
| R1-13 | "Uncertainty" is too strong for 3 configurations — prefer "model spread" | Accept | 1E | L405, L392 | ☑ |
| R1-14 | Justify the 50 most sensitive cells, the 100 m clustering threshold, and the 6 km route limit | Accept | 1G | L166, L300, L388 | ☑ |
| R1-15 | Clarify whether the route was actually executed by the USV | Accept | 1H | L408 | ☑ |
| R1-16 | Give a percentage or frequency for missing sensor data | Accept | 3E | L414 | ☑ Appendix E coverage table |
| R1-17 | Keep the temperature-only and path-planning limitations clearly visible | Accept | 1D | L424, L428 | ☑ |
| R1-18 | Keep "prototype" / "proof-of-concept" / "demonstration" wording in the conclusions | Accept | 1D | L432 | ☑ |
| R1-19 | Present as a potentially transferable framework, not a demonstrated general solution | Accept | 1D | L434 | ☑ |
| R1-20 | DAS contradicts the statement that hydrological data cannot be shared | Accept | 1N | L449 | ☑ |

⚠️ **R1-14** — `data/1.Sampling_Priority.csv` contains **29 rows, not 50**. Do not write the justification until this is resolved (Phase 5A provenance work). Either the committed file is a subset or the manuscript number is wrong.

⚠️ **R1-20** — the commented-out alternative DAS at L444 cites DataverseNO DOI `10.18710/6CD1B5`, which **returns 404 from the DataCite API — it is not registered**. Do not uncomment it as-is.

---

## Reviewer 2 — major revision (11 comments)

> *Summary:* "The prototype built and reported in this manuscript overstates what has actually been validated, and several figures don't carry enough information for the reader to verify what's claimed in the text… Overall I consider this to be a good piece of systems-integration work and the framework itself a useful contribution, but the manuscript as it stands gives the impression that more has been validated than actually has been."

| ID | Ask (abridged) | Disposition | Plan item | Where | Status |
|---|---|---|---|---|---|
| R2-1 | Soften/support the novelty claim (cites Qiu et al. 2023, Kwon et al. 2025); declare the SSRN preprint **in the text** | Accept | 1A + 1B | L74, L108 | ☑ |
| R2-2 | Only temperature was validated — make chemical/biological validation explicitly future work from the abstract onward | Accept | 1D | L54, L360, L432 | ☑ |
| R2-3 | M = 3 is too small; show ranking/path stability under a 4th–5th run or resampling | Partial | 2D + Phase 4.2 | §3.3 + appendix | ☑ Appendix F stability; extra members declined |
| R2-4 | Eq. 8 normalizes σ but Eq. 9 sums raw σ — fix or explain | Accept | 1F + 5C | L286, L297 | ☑ |
| R2-5 | Missing mass-balance check on contaminant transport | Accept | 3C | appendix + §3.2 | ☑ Appendix D whole-domain balance |
| R2-6 | Turbulence closure never stated or validated; acknowledge equifinality | Partial | 1K + 3I | L219, §4 | ☑ closure + coefficients in Appendix B; equifinality in §4 |
| R2-7 | Figs. 1–3 and Table 1 don't pull enough weight (annotate Fig. 1; merge Tables 1 + A1; expand Fig. 2 caption; draw the withheld-data decision in Fig. 3) | Accept | 1L | L116, L156, L166, L212, L241, Table A1 | ◐ tables, Fig. 2 caption and the withheld-data path done (Figs. 3 and 4 redrawn); Fig. 1 annotation with the author |
| R2-8 | Fig. 5 doesn't let the reader verify the RMSE/r claims — add per-depth panels, residuals, RMSE heatmap by depth × month | Accept | 3A | new appendix | ☑ Appendix C, Figures 11-13 |
| R2-9 | Fig. 6 needs error bars; the computational-time scaling doesn't add up; define "Simulation Time/Run Time" with units | Accept | 2C | Fig. 6, §3.1 | ☑ Fig. 6 regenerated, full-season only, axis defined |
| R2-10 | Figs. 7/8 need a solute-transport-specific mesh convergence check | Accept | Phase 4.1 | appendix + §3.2 | ⏸ Phase 4 |
| R2-11 | `Dmax` = 6 km is unjustified — cite Otter battery/range specs or field data | Partial | 1G | L166, L300 | ☑ |

✅ **R2-1 verified.** The SSRN preprint exists: `abstract_id=5226067`, *"A Water Quality Digital Twin for Protecting a Drinking Water Source"*, Primeau, Seidu, Zhang, Han, Li — the same five authors. The reviewer is correct and this must be declared in the text.

✅ **R2-4 verified in code.** [`src/PathPlanning/a.PointSelection.py:42`](../../src/PathPlanning/a.PointSelection.py#L42) aggregates `Weight=('Depth-averaged uncertainty', 'sum')` — the **raw** σ. Eq. 9 matches the code; Eq. 8's `σ'ᵢ = σᵢ/max(S)` is never applied. Not a typo in Eq. 9 — an unapplied step in Eq. 8.

⚠️ **R2-9** — the reviewer's arithmetic needs checking before responding. In `data/Calibration.csv` the 9,884-cell run is *40-layer Low-Res* (3.45 h) and the 65,904-cell run is *40-layer High-Res* (6.07 h): 6.67× cells for **1.76×** time, not the 4.75× the reviewer infers. Verify which rows the manuscript actually refers to and correct the manuscript if its numbers are wrong.

⚠️ **R2-11 — partial, and the current justification must be withdrawn.** The manuscript attributes the 6 km limit to battery capacity (L164, L297). The Otter does ~20 h at 2 kn (≈74 km), so endurance is **not** the binding constraint. Replace with the mission-duration justification; cite the `Otter` bib entry. No field trial was run, so field-trial evidence is declined.

---

## Reviewer 3 — revision, reproducibility focus (5 comments)

> *Summary:* "The paper is clearly written and the application is relevant, but several issues need to be addressed before publication."

| ID | Ask (abridged) | Disposition | Plan item | Where | Status |
|---|---|---|---|---|---|
| R3-1 | Model configuration too sparse to reproduce: Delft3D FM version, mesh, layers, timestep, BC/IC, solver settings, calibrated values + ranges | Accept | 2B + 3D | appendix | ☑ Appendix B, two tables |
| R3-2 | Was the same 2024 dataset used for calibration and validation? Discuss overfitting, split the periods, report RMSE/MAE/r | Accept | 2A + 3B | §2.2, §3.1 | ◐ statistics tabulated; season not split temporally |
| R3-3 | Spell out the workflow concretely; which steps are automated vs. manual | Accept | 1L (Fig. 3) + 3F | §2.2, Fig. 3/4 | ☑ Appendix E workflow table |
| R3-4 | Support the <2 h latency claim with actual per-stage timings; discuss robustness to missing data, comms failures, failed runs | Partial | 3F | L240, §4 | ☑ Appendix E latency + robustness ⚠ see 2026-09-08 audit |
| R3-5 | Repository lacks components needed to reproduce the results | Accept | Phase 5 | repo | ☑ pipeline repaired; 51 data files await commit |

⚠️ **R3-4** — the best configuration's run time is **6.07 h**, which exceeds the hourly update interval the latency claim depends on. The operational configuration presumably differs from the calibration configuration; this must be stated explicitly rather than left for a reviewer to notice.

✅ **R3-5 is accurate.** All four scripts in `src/PathPlanning/` currently raise `FileNotFoundError` (data files were renamed with `1.`–`4.` prefixes; no script was updated); four committed CSVs contain unresolved git conflict markers; `data/d3d/` is empty; and `data/2.clustered_coordinates.csv` holds values 1e10× larger than `data/1.Sampling_Priority.csv`, so the committed outputs were not produced by the committed inputs and scripts.

---

## Cross-cutting items (not tied to one comment)

| Item | Rationale | Status |
|---|---|---|
| Two consecutive `\corres{}` at L51–52 — the second overwrites the first | Only Guoyuan Li would render as corresponding author | ☑ |
| Commented-out obsolete abstract at L57 | Dead text | ☑ |
| Missing `\label`s at L110, L169, L394 | Subsections cannot be cross-referenced | ☑ |
| `\ref{ch:waterquality}` at L118 missing `Section~` prefix | Renders as a bare "1.1" | ☑ |
| "Fig. \ref{}" at L463 vs. "Figure~" everywhere else; Fig. 10 `\label` outside `\caption`, no float specifier | Consistency | ☑ |
| Commented-out `adjustwidth` around Fig. 4 (L222/L225) | Decide deliberately | ☑ removed in Phase 0 |
| MDPI dummy bib entries `Smith2012qr`, `Smith2013jd`, `Feynman1963118` | Template leftovers | ☑ |
| Possible duplicate: `xu2024design` (cited L108) vs. staged `w16243668` | Same authors/topic — keep one key | ☑ |
| Citation-as-subject sentences at L98, L106, L108 | Numeric *Sensors* style renders these as "[27] presents…" | ☑ |
| Figure payload ≈ 28 MB (Fig. 2 = 19 MB, Fig. 5 = 5 MB) | Likely over MDPI submission limits; slow Overleaf compiles | ⏸ Phase 6 |
| `Definitions/` is an older MDPI class and lacks `unicode.tex` | Refresh from `supplements/MDPI_template_ACS/Definitions/` | ⏸ Phase 6 |

---

## Reviewer-recommended references

All five supplement PDFs already have BibTeX entries staged in `sources.bib` **but are cited nowhere**. Only the Kwon et al. review needs a new entry.

| Bib key | Reference | Status |
|---|---|---|
| `qiu2023digital` | Qiu et al., *Toxins* **15**(11):665, 2023 — "A Digital Twin Lake Framework for Monitoring and Management of Harmful Algal Blooms" | staged, uncited |
| *(none yet)* | Kwon, Kang, Nam & Kim, *Water Sci. Technol.* **92**(9):1286–1307, 2025, doi `10.2166/wst.2025.145` — "Water quality monitoring using hybrid physical–soft sensors for river digital twins: a comprehensive review" | **must be added** |
| `w16142038` | Li et al., *Water* **16**(14):2038, 2024 — "Digital Twin Smart Water Conservancy: Status, Challenges, and Prospects" | staged, uncited |
| `w16243668` | Xu, Hui & Qu, *Water* **16**(24):3668, 2024 — 3D urban-river water-quality DT platform | staged, uncited |
| `computers13040100` | Hananto et al., *Computers* **13**(4):100, 2024 — "Digital Twin and 3D Digital Twin: Concepts, Applications, and Challenges in Industry 4.0" | staged, uncited |
| `civileng6040059` | Gehring, Brötmann & Rüppel, *CivilEng* **6**(4):59, 2025 — "A Modular, Logistics-Centric Digital Twin Framework for Construction" | staged, uncited |
| `buildings15172984` | Wang et al., *Buildings* **15**(17):2984, 2025 — "Value-Chain-Driven Multi-Level Digital Twin Models for Architectural Heritage" | staged, uncited |
| `hess-29-1183-2025` | Feldbauer, Mesman, Andersen & Ladwig, *HESS* **29**(4), 2025 — "Learning from a large-scale calibration effort of multiple lake temperature models" | staged, uncited — anchors R1-9 |

---

## Declined, with justification

| Comment | Response for the letter |
|---|---|
| R2-3 (full uncertainty characterization) | Reframed as *model spread across structurally distinct configurations*. Adding resampling stability and 1–2 further members; formal UQ (Monte Carlo, Gaussian process) remains future work, as already stated in the Discussion. |
| R2-6 (independent turbulence validation) | No ADCP or drifter velocity data exist for this site. We state the closure and its coefficients, acknowledge the equifinality problem explicitly, and name it as a limitation. |
| R1-7 (full hydrological calibration) | Procedure and aggregate performance indicators only; the underlying outflow and surface-elevation dataset is restricted by ownership and safety. |
| R2-7 (option to drop Fig. 1) | Retained and annotated with this system's actual update rates — the reviewer's own first alternative. The framework is the paper's first stated contribution. |
| R1-14 / R2-11 (field-trial evidence for `Dmax`) | Manufacturer specifications and operational reasoning are cited; no field trial was conducted. The previous battery-capacity justification is withdrawn as unsupported. |


---

## Phase 0 + Phase 1 completion record

Completed 2026-09-04. Build verified clean (24 pages, zero undefined references or citations); 22 automated content assertions pass.

### Phase 0 — latent LaTeX defects fixed
- Merged the two consecutive `\corres{}` commands (the second was silently overwriting the first, so only the second author would have rendered as corresponding).
- Deleted the commented-out obsolete abstract.
- Added `\label`s to the three unlabelled subsections (`ch:framework`, `ch:HWQM`, `ch:pathresults`).
- Fixed the bare `\ref{ch:waterquality}` (missing `Section~` prefix) and the "Fig." / "Figure~" inconsistency; moved Fig. 10's `\label` inside its `\caption` and gave it a float specifier.
- Removed the dead `adjustwidth` comments around Fig. 4.
- Deleted four MDPI template dummy bib entries (`Smith2012qr`, `Smith2013jd`, `Dirac1953888`, `Feynman1963118`) plus a stray byte-order mark inside `sources.bib`.
- Removed the duplicate `w16243668` entry (identical to the already-cited `xu2024design`) and fixed the malformed `doi={https://doi.org/...}` field in `xu2024design`.

### Phase 1 — reviewer comments addressed
- **1A/R2-1, R1-3:** novelty claim qualified. Now cites Qiu et al., Kwon et al., Li et al. and Xu et al., states that such systems are no longer rare, and narrows the claim to what is actually defensible — a process-based 3D hydrodynamic twin of a drinking water source reservoir.
- **1B/R2-1:** SSRN preprint declared in the text with a new bib entry.
- **1C/R1-2:** contribution relative to the earlier paper stated explicitly.
- **1D/R2-2 etc.:** abstract, §3.2 opener and conclusions reframed so temperature-only validation is explicit; transferability softened; boom-insufficiency marked as simulation-derived.
- **1E/R1-13, R2-3:** "uncertainty" replaced by "model spread" where only three configurations were compared, with an added sentence saying what the quantity does and does not measure.
- **1F/R2-4:** Eqs. 8, 9 and 10 now use the normalized sigma consistently, with an explanation that the rescaling is monotone and does not change the selection.
- **1G/R1-14, R2-11:** the battery-capacity justification for `Dmax` is **withdrawn** in all three places it appeared, replaced by a mission-duration argument citing the Otter specification (~20 h at 2 kn, so endurance was never the binding constraint).
- **1H/R1-15:** states plainly that the route is an executable mission that was not flown.
- **1I/R1-10:** Eq. 12 replaced — the previous form showed denitrification producing O2. Now the heterotrophic form with organic carbon as electron donor, with the process formulations cited.
- **1J/R1-9:** thresholds anchored against Feldbauer et al.'s multi-model lake temperature comparison.
- **1K/R2-6:** equifinality acknowledged in the Discussion, citing the paper's own Xia et al. reference; absence of velocity data named as a limitation.
- **1L/R2-7:** Fig. 2 caption extended as requested; Table 1 merged into the Appendix A instrument-characterization table with §2.1 pointing to it; the withheld-profiler-data decision promoted from mid-paragraph into its own paragraph; turbidity's outlying calibration scatter now discussed rather than left unremarked.
- **1M:** citation-as-subject sentences rewritten to name authors, since the numeric *Sensors* style would otherwise render them as "[27] presents...". All author attributions verified against `sources.bib` (one initial error — "Alam and El Saddik" for a three-author paper — was caught and corrected to "Alam et al.").
- **1N/R1-20:** Data Availability Statement rewritten to point at the GitHub repository and to carve out the restricted hydrological dataset explicitly.

### Left open deliberately

Nine `TODO` markers remain in `main.tex`. Each marks something that could not be verified from the repository, and each was left unwritten rather than guessed:

| `main.tex` | Needs |
|---|---|
| L54 | RMSE / r / latency for the abstract (Phase 2, from `Calibration.csv`) |
| L74 | One sentence on what is new relative to the SSRN preprint — **author knowledge**; the preprint's contents could not be verified |
| L116 | Geodetic datum/projection and base-imagery source/resolution for the Fig. 2 caption — **author knowledge** |
| L205 | Turbulence closure name and coefficients (Phase 3, from the `.mdu`) |
| L337 | Whether the RMSE/r thresholds were set a priori or post hoc — **author knowledge** |
| L350 | Whether 3.5 kg is compound mass or nitrogen mass — **author knowledge** |
| L388 | Horizontal mesh spacing, to complete the 100 m clustering justification (Phase 2/5) |
| L435 | DataverseNO DOI, only if a deposit is actually created |
| L475 | Accuracy and resolution columns of the merged instrument table, from the EXO manual |

### Not possible in this pass

**Fig. 1 annotation and Fig. 3 redraw (both R2-7).** Both were raster PNGs with no source files in the repository, so at the time neither could be edited. The Fig. 3 substance was handled in prose meanwhile (the withheld-data decision was given its own paragraph).

**Partly superseded.** Figures 3 and 4 were re-derived from scratch, rather than recovered, as SVG sources generated by `src/figures/make_fig3.py` and `make_fig4.py` on a shared toolkit (`src/figures/svgkit.py`); regenerate with `.venv/Scripts/python src/figures/make_all.py`. Figure 4 was included because it had the same missing-source problem and, having been authored about 12 in wide and placed at 5.5 in, rendered its type at roughly 3 pt. Figure 1 was also redrawn, twice, and both attempts were rejected by the author and reverted; the submitted figure stands and the author is handling that comment. The original was recovered from `cd35a4c` if it is wanted again.


---

## Publication-readiness rule (user directive, 2026-09-07)

**The rendered PDF must contain no placeholders, TODO notes, or empty cells.** Anything unresolved lives as a `%` comment in `main.tex`, never as rendering content.

Audited and enforced. Three defects were found and fixed:

1. **Table A1 rendered em-dash placeholders.** The merged instrument table carried `---` in the Accuracy and Resolution columns on every row, and two rows (Conductivity, Salinity) were entirely dashes. Those two columns were removed until the manufacturer figures are available, and the non-calibrated rows now carry real statements via `\multicolumn` — "Factory calibrated; no field calibration required" for temperature, "Same sensor; traceable to the specific conductivity calibration" for conductivity, "Derived from conductivity and temperature" for salinity. The table now renders complete. Prose in §2.1 and Appendix A that promised accuracy/resolution was corrected to match.
2. **Space before a comma in the abstract.** An inline `%` comment left "water temperature only , the largest" — the space preceding `%` survives while `%` absorbs the newline. Fixed by closing the space up.
3. **Doubled DOI prefixes throughout the bibliography.** 79 entries in `sources.bib` had `doi = {https://doi.org/10....}`, which the MDPI style rendered as `https://doi.org/https://doi.org/10....`. All 79 normalized to bare DOIs.

### Standing check

A TeX-accurate comment simulation is used to confirm nothing unintended renders. Current state: **0** rendering placeholders, **0** space-before-punctuation defects, **0** malformed DOI fields, **0** undefined references or citations, 24 pages.

The 9 remaining `TODO` markers are all verified to sit inside `%` comments. Grep `TODO` in `main.tex` to list them.


---

## Cover letter (draft, 2026-09-07)

`docs/manuscript/Cover_letter.docx` has been rebuilt from the supplied template's own XML (Times New Roman, justified, same heading weights), signed **Russell Primeau on behalf of all authors**, and covers all 36 comments in the template's `Comment` / `Response:` / `Changes in manuscript:` structure. The original template is preserved as `Cover_letter_TEMPLATE_original.docx`.

It carries a **DRAFT banner that must be deleted before sending**, because most "Changes in manuscript" lines describe work that is planned but not yet in the PDF.

### Claims in the letter that are NOT yet true of the manuscript

Verify or complete each before removing the banner:

| Letter says | Actually done? |
|---|---|
| R1-1 abstract reports RMSE / r / latency | **No** — scope sentence added, numbers still a TODO |
| R1-4, R3-2 independent validation period with held-out metrics | **No** |
| R1-5, R1-6, R3-1 configuration matrix + ranges + model config table | **No** — data now available in `D3DFMRunner` |
| R1-7 hydrological calibration summary | **No** |
| R1-8 performance table | **No** — computable from `Calibration.csv` |
| R1-11 weather splicing description | **No** |
| R1-16 measured gap fractions | **No** |
| R2-3 resampling stability | **No** |
| R2-5 mass balance | **No** — `waq_balance.py` + `-bal.his` available |
| R2-6 closure named with coefficients | **No** — values confirmed in the `.mdu`, not yet written in |
| R2-7 Fig. 1 annotated, Fig. 3 redrawn | **Partly** — Figs. 3 and 4 redrawn from SVG sources in `src/figures/`; Fig. 1 unchanged, with the author |
| R2-8 per-depth panels, residuals, error breakdown | **No** — computable from `ThermalTune` his.nc |
| R2-9 Fig. 6 units, corrected scaling, error bars | **No** |
| R3-3 workflow / automated vs manual | **No** |
| R3-4 per-stage latency | **No** |
| R3-5 repository reorganised | **No** — Phase 5 |

Already true: R1-2, R1-3, R1-9 (partially), R1-10, R1-12, R1-13, R1-14 (partially), R1-15, R1-17, R1-18, R1-19, R1-20, R2-1, R2-2, R2-4 (text; code pending), R2-11.

### Correction to an earlier note in this file

An earlier draft of this tracker flagged a conflict between the `tuner_fixed` metrics (RMSE ~2.08 °C, negative r²) and the manuscript's RMSE 0.708 / r 0.9718. That comparison was invalid: `tuner_fixed` is a separate one-at-a-time parameter sweep, not the 2024 long run, and its runs differ in many parameters. The two are not comparable and the flag is withdrawn.

### Authoritative source for the revised results

`FlowFM2026/input/FlowFMnew.mdu` and `ThermalTune/input/FlowFMnew.mdu` are byte-identical in every parameter checked, and both cover 2024-04-22 → 2024-11-20. `FlowFM2026/output` holds only a `.dia` file (it was the tuner's scratch run directory); `ThermalTune/output` holds the completed `FlowFMnew_his.nc` (5 stations × 40 layers × 5089 hourly steps, including `Profiler`), the merged `FlowFMnew_map.nc`, and the WAQ coupling files. **Confirm with the author which output directory is the authoritative 2024 long run before any number is written into the manuscript.**


---

## Findings from D3DFMRunner / BrusdalsvatnetDT (2026-09-08)

`ThermalTune/output` confirmed as the governing results set, per the author.

### Assumption now verified, not assumed

`FlowFM2026/input/FlowFMnew.mdu` and `ThermalTune/input/FlowFMnew.mdu` were compared key by key: **526 keys each, zero differences.** The two projects share one configuration and one period (2024-04-22 to 2024-11-20). `FlowFM2026/output` holds only a `.dia` file because it served as the tuner's scratch run directory. The earlier ambiguity about which project is authoritative is therefore resolved on evidence, not by preference.

### CONTRADICTION FOUND AND CORRECTED — in-situ nitrogen observations do exist

A sentence added during Phase 1 stated that *"No in situ measurements of ammonium or nitrate concentration are available at the site."* **This is false**, and it has been corrected.

`D3DFMRunner/data/sources/timeseries/waq/` contains laboratory grab-sample records spanning the simulation period:

| Dataset | Samples | Period | Stations |
|---|---|---|---|
| `Nitrate_g_l_N_validation` | 38 | 2022-09-12 to 2025-10-22 | Fremmerholen surface, Vasstrandlia intake @32 m, Spjelkavikelva 1 and 2 |
| `Unfiltered_Ammonium_g_l_N_validation` | 39 | 2022-09-12 to 2025-10-22 | same four |
| `Total_nitrogen_g_l_N_validation` | 44 | 2023-05-22 to 2025-12-03 | seven, incl. Bv-east/mid/vest at 12-16 m |
| `Filtered_Ammonium_g_l_N_trib`, `Nitrate_nitrite_g_l_N_trib` | 12 each | 2024 | tributary loads (model *inputs*, not validation) |

The same programme's lake-background values are already committed in this repo as `data/Nitrogen/GroundTruth/{NH4,NO3}.csv` (8-9 samples each, 2022-2024; NH4 0.001-0.011 gN/m3, NO3 0.079-0.12 gN/m3).

The original manuscript wording was subtler and remains correct: it referred to the absence of *sensors*. The error was introduced by Phase 1 in widening "sensors" to "measurements".

**Corrected text now distinguishes two separate limits:** no continuously recording NH4/NO3 sensor is deployed, and the observations that do exist are sparse and often at or below detection limit; and, more fundamentally, the modelled release is a contingency scenario that never occurred, so plume observations cannot exist in principle.

### OPPORTUNITY — Figure 8 could show observations but does not

`src/D3D/NewWAQPlots.py` already loads the nitrogen ground truth via `read_groundtruth()`, but the two lines that plot it are **commented out** (lines 277-278, and again at 325-326). Figure 8 as published therefore shows model output only, which is why a `combined_model_only.png` exists alongside `combined.png`.

Uncommenting these gives a genuine, if limited, model-versus-observation comparison for the modelled background concentrations of NH4 and NO3, at essentially no cost. **This would move Reviewer 2 Comment 2 from "nothing chemical was validated" to "modelled background concentrations are compared against grab samples; transient plume validation is impossible for a hypothetical release."** Author decision required before it goes in, and the abstract wording would need to follow.

### Post-processing tooling to be used (per author instruction)

Results added to the manuscript are to be derived with the existing tools, not reimplemented:

- `src/hydro/d_hydro_post.py` (8,705 lines) — `--plot-validation` writes a model-vs-observation report with N, R2, Pearson r, RMSE and MAE per pairing; `--export-figure LABEL --export-dir` writes publication-ready PNGs with statistics printed to console. Pairings come from `data/sources/config/hydro/Pairings.csv`, which already defines the profiler temperature comparisons at 1, 20, 30, 40 and 50 m plus a `depth_group_round_m=1` variant that produces per-metre bands. That variant is what Reviewer 2 Comment 8 asks for.
- `src/waq/g_waq_post.py` (7,449 lines) — water-quality post-processing.
- `src/utils/waq/waq_balance.py` — mass balance, for Reviewer 2 Comment 5.

All observation inputs referenced by `Pairings.csv` are present under `data/sources/timeseries/hydro/`.


---

## Governing validation results (ThermalTune, 2026-09-08)

Produced with `src/hydro/d_hydro_post.py --plot-validation` against `ThermalTune/output/FlowFMnew_his.nc`, using the project's own `Pairings.csv`. No metric code was written for this; the numbers are the tool's own output.

Period 2024-04-22 to 2024-11-20.

| Comparison | N | R2 | Pearson r | RMSE | MAE | Final error |
|---|---|---|---|---|---|---|
| Hourly water temperature at Profiler | 4,504 | 0.776 | 0.962 | 1.731 °C | 1.399 °C | +0.792 °C |
| Temperature profile @ 1 m | 353 | 0.716 | 0.959 | 1.936 °C | 1.588 °C | +0.323 °C |
| Temperature profile @ 20 m | 389 | -5.718 | 0.819 | 2.954 °C | 2.529 °C | +0.804 °C |
| Temperature profile @ 30 m | 395 | -5.062 | 0.865 | 2.422 °C | 1.995 °C | +0.810 °C |
| Temperature profile @ 40 m | 398 | -4.256 | 0.870 | 1.953 °C | 1.520 °C | +0.833 °C |
| Temperature profile @ 50 m | 398 | -3.381 | 0.875 | 1.565 °C | 1.139 °C | +0.818 °C |
| Water level | 3,180 | 0.949 | 0.987 | 0.027 m | 0.018 m | -0.050 m |

### Reading these numbers

**Negative R2 alongside a respectable Pearson r is not a contradiction.** Deep water is nearly isothermal, so the observed variance is small; R2 penalises the bias against that small variance, while r still registers that the model tracks the seasonal shape. The deep-water rows are a bias problem, not a phase problem.

**There is a consistent warm bias at every depth**, +0.79 to +0.83 °C at the end of the run, and it grows with depth in RMSE terms up to 20 m.

**Neither acceptance criterion in the current manuscript is met by the governing run.** The manuscript states RMSE below 1 °C and Pearson r above 0.95. The full-season run gives RMSE 1.57-2.95 °C, and r above 0.95 only at the surface and 1 m.

The figures currently in the manuscript (RMSE 0.708 °C, r 0.9718, MAE 0.445) come from `data/Calibration.csv`, which holds two-month runs (2024-04-25 to 2024-06-28) that the author has confirmed are superseded.

### Why this may be a finding rather than a problem

The manuscript already argues, in its own words, that calibrating over a short span risks concealing errors: that during spring and early summer there is net heat gain, that inaccuracies in heat-loss processes such as outgoing longwave radiation can be masked by adjustments to incoming flux, and that "such an error only becomes apparent when the simulation includes the fall season."

The full-season result is precisely that prediction coming true: a two-month spring-summer window met the criteria, and extending through autumn cooling exposes a systematic warm bias. Reported that way, the degradation supports the manuscript's existing methodological argument instead of undermining it, and it answers Reviewer 3 Comment 2 on overfitting with direct evidence.

**Author decision required** on how to report this. Nothing has been written into the manuscript from these numbers yet.

### Incidental figure for Reviewer 1 Comment 16

The hourly surface temperature series has 4,504 observations against 5,089 model timesteps over the same period, i.e. roughly 11.5 % missing. A further 117 profile values were rejected by the range filter (0-25 °C). These are measured numbers usable for the missing-data disclosure.

### Water level result is strong

Pearson r 0.987, RMSE 0.027 m over 3,180 observations. Relevant to Reviewer 1 Comment 7, which asks for hydrological calibration performance indicators that can be reported without disclosing the restricted dataset.


---

## Work completed 2026-09-08 (governing results now in the manuscript)

Build clean at each step: 29 pages, zero undefined references or citations, zero rendering placeholders, zero spacing defects.

### Section 3.1 rewritten (R1-8, R3-2, R1-9, R2-9 partial)

Now reports the full-season ThermalTune results, with a new performance table (`tab:performance`) covering the hourly surface series, four profile depths, the 50-band mean, and water level.

Per the author's decision, the acceptance criteria are **restated against the Feldbauer et al. benchmark** (median RMSE 1.2 °C, median r 0.98, 95 % of 73 lakes below 2 °C) rather than the previous self-chosen thresholds of RMSE < 1 °C and r > 0.95. This also retires the R1-9 question about threshold provenance: an external benchmark cannot be accused of having been set after seeing the results.

The shortfall is reported rather than hidden, and framed as evidence for the manuscript's own argument that a short calibration window leaves heat loss unconstrained.

### New Appendix: Temperature Validation by Depth (R2-8)

Three model-versus-observation panels at 1, 20 and 50 m (Figures 11-13, from `d_hydro_post.py --export-figure`), a per-depth error table at 5 m intervals, and a diagnosis: the model transports heat downward too strongly during stratification, placing the thermocline too deep and leaving the metalimnion too warm. At 20 m the model reaches ~11 °C in late summer against observations near 7 °C.

The 50-band table exported to `data/validation/temperature_by_depth_ThermalTune_2024.csv`.

**Note on the 50-depth overlay figure.** `--export-figure "Temperature vs. Depth Profiles_All"` was tried first and rejected: with fifty overlapping curves it reproduces precisely the unreadability Reviewer 2 complained about in Figure 5. The separate single-depth pairings are what answer the comment.

### New Appendix: Model Configuration (R3-1, R2-6)

Full configuration table transcribed from `ThermalTune/input/FlowFMnew.mdu`: solver version, mesh, layers, timestep, Courant limit, solver and advection settings, k-epsilon closure with its coefficients, eddy viscosity and diffusivity, heat-exchange and friction parameters, and initial and boundary conditions. The §2.2 turbulence sentence now names the closure and cross-references the appendix.

### Abstract (R1-1)

Now carries measured values: RMSE 1.7 °C, Pearson r 0.96, with metalimnetic errors noted.

### REVERSED DECISION — Figure 8 nitrogen observations

The author approved uncommenting the ground-truth plotting in `NewWAQPlots.py`. **It was implemented, inspected, and reverted**, because the resulting figure is misleading:

- The model represents only the **concentration increment** from the hypothetical release. The grab samples measure **absolute background** concentration. Overlaying them on one axis makes the model appear to under-predict by four orders of magnitude when it does not represent background at all.
- On a "days post-incident" axis, most observations fall between -700 and 0 days, i.e. before the hypothetical event.

`src/D3D/NewWAQPlots.py` is restored to its committed state and `Fig8.png` is unchanged.

**The observations are used instead in a way that is defensible**, as a magnitude reference in §3.2. This required correcting a parsing detail: the WAQ export files use an underscore as the decimal separator (`1_33671501317E-05`), which `NewWAQPlots.py` handles via `CONFIG.decimal = "_"`.

| Site | Peak NH4 increment | Peak NO3 increment |
|---|---|---|
| Release point | 1.19 gN/m3 | 1.19 gN/m3 |
| Spjelkavikelva | 1.23e-3 | 1.27e-3 |
| Vasstrandlia intake | 1.99e-5 | 3.48e-5 |
| Profiler | 5.99e-6 | 1.56e-5 |
| Far field | 3.08e-7 | 1.21e-5 |

Observed background: NH4 0.001-0.011, NO3 0.079-0.120 gN/m3.

At the intake the predicted increments are about 2 % (NH4) and 0.04 % (NO3) of the lowest measured background, while at the release point ammonium exceeds background by three orders of magnitude. **The operational conclusion is that the worst-case release would not produce a detectable change at the drinking water intake** — a more useful finding for the supplier than absolute concentrations, and one that uses the observational record honestly without claiming validation.

### Bug found in d_hydro_post.py

At line 8603 the `_requested_outputs_available` guard tests `wants_his`, `wants_map` and `wants_validation` but omits `wants_export`. `--export-figure` on its own therefore always aborts with "No output files could be loaded," even after the HIS file has loaded successfully. Worked around by passing `--plot-validation` alongside `--export-figure`; not fixed, as that repository was not in scope.

### Still open

R2-5 mass balance, R2-3 resampling stability, R1-11 weather splicing, R1-7 hydrological calibration narrative, R3-3 workflow detail, R3-4 latency, Phase 5 repository work. Under R2-7, Figures 3 and 4 are redrawn; the Figure 1 annotation is with the author. Six TODO comments remain in `main.tex`, five needing author knowledge.


---

## Bug fixes (2026-09-08)

### 1. `d_hydro_post.py` — `--export-figure` aborted on its own

`src/hydro/d_hydro_post.py` line 8600, in `main()`. The `_requested_outputs_available` guard tested `wants_his`, `wants_map` and `wants_validation` but not `wants_export`, so exporting a figure without also requesting a viewer or a validation report always failed with "No output files could be loaded" even though the HIS dataset had loaded successfully.

Added `or (wants_export and _his_ds is not None)`.

Verified: `--export-figure "Temperature vs. Depth Profiles_20m"` alone now succeeds and reports identical statistics (N=389, r=0.819, RMSE=2.954 °C) to the previous `--plot-validation` workaround.

### 2. Underscore decimal separators in the WAQ export CSVs

The WAQ time-series CSVs stored values as `1_33671501317E-05`. Any reader using the default `.` separator turns these into NaN, and because the leading rows of each file are literal `0` the result surfaces as a plausible-looking column of near-zeros rather than an error. This is what produced the all-zero peak concentrations on my first attempt at the Section 3.2 comparison.

**Data.** 46 files under `data/Nitrogen/` normalised to standard `.` notation. Each conversion was verified by re-parsing: the converted column equals the original parsed with `decimal='_'`, value for value, across all 46 files with zero mismatches.

`data/Calibration.csv` was deliberately **excluded**. It matched the `digit_digit` search only inside a Windows directory name (`...mnth _0Secchi`), not a decimal, and rewriting it would have corrupted a stored path.

**Code.** `CONFIG.decimal` changed from `"_"` to `"."` in both `src/D3D/NewWAQPlots.py` and `src/D3D/WAQHisPostProcess.py`, and a `_check_numeric()` guard added to `read_series()` in both.

**The first guard was wrong and the negative test caught it.** It failed only when a column parsed to *entirely* NaN, which never happens here because the opening rows are zeros that parse cleanly. It now fails when any present-but-unparseable cell is found, and reports how many and an example. On the underscore file it reports "2203 of 2209 values did not parse (e.g. '4_81925055418E-10')".

**Regression.** `NewWAQPlots.py`, `WAQHisPostProcess.py` and `CSVplotter.py` all exit 0, and `data/Nitrogen/combined.png` (the source of Figure 8) is byte-identical before and after, confirming the change is behaviour-preserving. The Section 3.2 peak-increment figures were recomputed from the normalised files and are unchanged.

**Incidental.** `WAQHisPostProcess.py` sets `show_plots: bool = True`, so `plt.show()` blocks on a GUI window and the script hangs when run non-interactively. Worked around with `MPLBACKEND=Agg`; it should be made non-blocking during the Phase 5 repository work.


### R2-5 mass balance — blocked, decision needed

`src/utils/waq/waq_balance.py` works: `load_balance()` reads `protist_demo-bal.his` and returns 30 substances (including NH4 and NO3) across 200 station/layer combinations, with per-station `mass`, `processes`, `loads_in`, `loads_out`, `transport_in`, `transport_out`.

But the reviewer asks for the **domain-integrated** mass at each timestep against the 3.5 kg released, and that is not obtainable from the artifacts present:

- Only one WAQ run exists, `WAQTestLoads/protist_demo`. It is an algae/nutrient demo driven by `FlowFM2026_VicoDico` hydrodynamics, not the nitrogen release scenario in the manuscript.
- Whole-model totals come only from the `.mon` report, and this run's `.mon` (482 MB, 3.6 M lines) contains no BALANCE sections, so `read_mon_balance()` returns zero timesteps. The balance output style that emits whole-model totals was evidently not enabled.
- The manuscript's nitrogen scenario output survives only as the exported CSVs in `data/Nitrogen/`; its DELWAQ balance artifacts were not retained.

Answering R2-5 therefore requires re-running the nitrogen WAQ scenario with whole-model balance output enabled. **A consequence worth weighing:** such a re-run would be driven by the ThermalTune hydrodynamics, whereas Figures 7 and 8 come from the superseded runs. Producing a mass balance on new flow fields while leaving those figures on the old ones would be internally inconsistent, so a re-run implies regenerating Figures 7 and 8 as well.


### CORRECTION — mass balance was available all along (R2-5 now answered)

The entry above claiming a WAQ re-run was required is **wrong and is withdrawn.** The author corrected it: whole-model balance is produced by `src/waq/g_waq_post.py --plot-balance`.

My error was to call the low-level reader `waq_balance.read_mon_balance()` directly with a truncated six-substance list. The `.mon` parser needs the full thirty-substance list to locate its blocks, so it returned zero timesteps and I concluded, wrongly, that the balance sections were absent. Run through `g_waq_post.py` the same file yields 30 substances, 200 stations and 857 timesteps without difficulty.

**Result (whole-domain, full season, from the solver's own balance output):**

| Term | Ammonium (kg N) | Nitrate (kg N) |
|---|---|---|
| Initial stock | 2,577 | 26,640 |
| Final stock | 502 | 31,500 |
| Change in stock | -2,075 | +4,858 |
| Loads | +1,695 | +10,259 |
| Boundary outflow | -130 | -4,818 |
| Reaction processes | -3,640 | -539 |
| **Residual** | **-0.31 (0.015 %)** | **-43.5 (0.42 %)** |

Written up as a new appendix, with a one-sentence pointer from §3.2. Two limits are stated in the text rather than glossed: the balance comes from the nutrient configuration rather than the release scenario itself (same solver, mesh, coupling and process library, so the conservation property carries, but that specific run was not repeated); and mass conservation is weaker than transport accuracy, since a scheme can conserve mass exactly while still spreading a plume too widely. The second point is what keeps R2-10 open as genuine future work rather than something this check disposes of.

Manuscript now 30 pages, build clean, zero rendering placeholders.


---

## R3-3, R3-4 and R1-16 answered (2026-09-08)

New Appendix E, *Operational Workflow, Data Coverage and Latency*, with pointers from §2.2 and §4. Manuscript now 32 pages, build clean.

### Workflow, automated versus manual (R3-3)

A table now divides the pipeline explicitly. Eight stages are automated (surface-sonde retrieval hourly, profile retrieval twice daily, weather retrieval hourly, quality control on ingestion, forcing assembly, model execution, post-processing against withheld observations, dashboard publication). Three remain manual: model configuration changes, USV launch and recovery, and USV mission upload and data extraction.

The text makes the point that keeping configuration changes manual is a deliberate consequence of the overfitting argument in §2.2, not an unfinished piece of automation.

### Data coverage (R1-16), measured over 22 April to 20 November 2024

| Stream | Coverage | Detail |
|---|---|---|
| Weather forcing | 100 % | complete by construction: 94.0 % on-site sensor, 6.0 % reanalysis backfill |
| Profiler, surface sonde | 88.5 % | 4,504 of 5,089 hourly intervals |
| Profiler, vertical profiles | 95.8 % | at least one profile on 204 of 213 days; 19,068 depth records |
| Water level | 62.4 % | 3,178 of 5,089 hourly intervals |

Derived mixing depth provenance: 45.3 % from a profile pair, 34.4 % from a single profile, 12.0 % persisted, 8.3 % monthly climatology.

The forcing pipeline already records provenance per value, which is what makes these numbers reportable at all. The text draws out the distinction that matters: **forcing gaps are filled because the model cannot advance without a value, while validation gaps are never filled**, so no synthetic value can enter an error statistic.

### Latency (R3-4) — and a reconciliation

Measured over the nine full-season runs in `tuner_fixed/tune_log.txt`: median **32.5 minutes** wall clock for **212 simulated days**, a speed-up of about **9,400x**. Advancing the model one hour therefore costs on the order of one second.

This resolves the apparent contradiction flagged earlier in this file, that a 6.07 h run time could not fit inside an hourly update interval. The two figures describe different things: the multi-hour figures are offline calibration over a whole season, not an operational update. §2.2 now says so explicitly.

Latency is therefore set by publication cadence, not computation: under two hours for the hourly streams, and up to twelve hours for anything derived from the vertical profiles. The manuscript now states both rather than quoting a single sub-two-hour figure.

### Robustness (R3-4, second half)

Three observed failure modes documented: a forcing gap is substituted and the run continues; a failed retrieval leaves the previous forcing file in place, so the result is a stale rather than an absent nowcast; a failed model run leaves the preceding nowcast standing.

Stated honestly rather than dressed up: none of this has been fault-injection tested, and there is no alerting to distinguish a stale nowcast from a current one at the point of use. Both are named as prerequisites for operational reliance and carried to the Discussion as future work.

### Note on the QA/QC layer

`BrusdalsvatnetDT/QA_QC_PREPROCESSING.md` specifies that a literal `"NAN"` string is replaced with `0` on ingestion. For temperature or pH that would convert missing data into a plausible value rather than a gap. Checked against the 2024 season: the profiler channels used in this manuscript contain no exact zeros, so no comparison reported here is affected. The practice remains a latent hazard for any channel whose valid range includes zero, and is worth changing during the Phase 5 work.


---

## R1-7 and R1-11 answered (2026-09-08)

Manuscript at 32 pages, build clean, audit clean. Seven TODO comments in source, none rendering.

### R1-7 hydrological calibration

§2.4 no longer says the calibration is "omitted here". It now describes the procedure: a volume balance closed hourly from observed surface elevation, metered abstraction, precipitation and modelled evaporation, with the residual attributed to inflow and allocated across the eight tributaries by catchment area.

**A caveat had to be added that the reviewer did not ask for.** The obvious performance indicator is the modelled-versus-observed water level, which agrees closely (Pearson r 0.987, RMSE 0.027 m, N = 3,178). Presenting that as validation would have been wrong, because the observed elevation is one of the inputs from which the inflow series is derived. Checked directly: d(level)/dt correlates 0.57 with the reconstruction's Net Accumulation term, so the dependence is real though not a pure derivative. The text now reports the statistic as **a consistency check on the volume balance, not an independent test of the hydrology**, and states that an independent check would need metered inflows, which do not exist at this site.

Also established: the measured outflow record covers 53.4 % of the 2020-2026 monitoring period but **0 % of the simulated 2024 season**, so the 2024 outflow is itself part of the reconstruction. This is stated in the text.

Only aggregate indicators are reported; the restricted series are not redistributed, consistent with the Data Availability Statement.

### R1-11 weather splicing — and a discrepancy with the previous draft

The forcing dataset records provenance per value. Across the simulated season 94.0 % of hourly values came from the on-site station and 6.0 % from reanalysis, and the substitution is concentrated rather than spread: April to September were covered almost without interruption, while **221 hourly values in October and 83 in November** were completed from reanalysis. No offset or rescaling is applied at the join; the text says so, and says no consequential discontinuity was identified.

**The discrepancy:** the previous draft described this as "seasonally appropriate historical weather data from the digital twin's database of sensor readings". The dataset tags the substituted values as *reanalysis*, not as sensor readings from other years. These are different mechanisms. The text now follows the dataset, and a TODO asks the author to confirm which is correct for the run presented — it is possible the earlier description refers to a different or earlier scenario run.

### Corrupted forcing files in BrusdalsvatnetDT

Three files contain unresolved `git stash pop` conflict markers (`<<<<<<< Updated upstream` / `>>>>>>> Stashed changes`) and would fail or be misread if used as model input:

- `FlowFM_meteo.tim` (markers at lines 1, 459, 653)
- `forcing/rainfall.tim`
- `forcing/windxy.tim`

Same class of defect as the four conflicted CSVs already recorded in `Postprocess`. Not repaired here: that repository is outside the agreed scope, and the correct resolution depends on which side of each conflict is wanted. Flagged for the author, and relevant to Reviewer 3 Comment 5 on reproducibility.


---

## Data Availability Statement rewritten (2026-09-08)

Per the author: the water level and outflow records come from a separate source that cannot be shared, headline statistics only are to be reported, and parts of the codebase such as the Delft3D FM kernel will not be distributed. The statement now says both explicitly, in two labelled parts.

**Restricted data.** Names the lake surface elevation and outflow records, states they originate from a separate third-party monitoring system and that permission to redistribute is not held, and states that no part of the series appears in the article or the repository. What is reported instead is the procedure and the aggregate indicators (the correlation and error statistics in §2.4). It also states the consequence honestly: the hydrological forcing cannot be regenerated from the repository alone, and the figures depending on it are reproducible only in the sense that the derived forcing files are supplied.

**Third-party software.** States that the repository holds the code written for this study and not its dependencies; that the Delft3D FM kernel is not redistributed but is obtained separately from Deltares under its own open-source licence; and that Appendix B records the kernel version and full configuration so the simulations can be repeated with an independently obtained solver. Python dependencies are declared by version rather than vendored.

Verified rendering on page 23: paragraph breaks and italic sub-headings come out correctly (`\endgraf` is needed inside the MDPI macro, which does not accept blank-line paragraph breaks).

### The model configuration is now distributable — 5.45 MB, not 29 GB

`data/d3d/` had been populated since the earlier survey and now holds ~29 GB across two projects, **none of it tracked**, because the root `.gitignore` excluded `/data/d3d/` wholesale. The Data Availability Statement as written would therefore have been false.

Inspection showed the size is entirely in `output/`: the `input/` directory of the governing run is 9.2 MB, and the genuinely necessary configuration is **35 files totalling 5.45 MB** — mesh, `.mdu`, `.ext`, eleven boundary `.pli`/`.tim` pairs, meteorological forcing, initial-condition fields and the DIMR config.

`.gitignore` rewritten to distribute exactly that set: it re-includes one directory level at a time (git cannot re-include a path whose parent is still excluded), keeps only the governing ThermalTune run, and continues to exclude all model output, MPI partition files, solver caches, `.dia` and `.log`. Verified with `git check-ignore`: output and the non-governing copy remain ignored; `git status -uall` lists exactly the 35 intended files.

**Integrity checked before recommending distribution.** `FlowFM_meteo.tim`, `rainfall.tim` and `windxy.tim` share filenames with the three conflict-corrupted files found in `BrusdalsvatnetDT`. The copies under `data/d3d/` are clean: 5,089 lines each, exactly matching the 5,089 hourly model timesteps, with no conflict markers. The BrusdalsvatnetDT copies are stale duplicates (653 lines, with `git stash pop` markers) and are not the inputs used for the reported runs.

**Outstanding:** the 35 files are un-ignored but **not yet committed**. A TODO in the manuscript records that they must be committed and pushed before submission, or the Data Availability Statement is false.


---

## R2-3 stability, pipeline repair, and a factual correction (2026-09-08)

### The path-planning pipeline now runs, and reproduces the published result

Phase 5A work, done because R2-3 could not be answered otherwise.

- **Stale data replaced.** `data/1.Sampling_Priority.csv` held only the first 30 rows of the analysis, at 1e-10 of the scale used by the committed downstream files. Verified against `BrusdalsvatnetDT/Sampling_Priority.csv`: coordinates match exactly and values match after multiplication by 1e10, so it was the same analysis truncated and rescaled. Replaced with the authoritative 51-row file.
- **Broken paths fixed** in all five scripts: they referenced `Sampling_Priority.csv`, `cluster_info.csv`, `clustered_coordinates.csv` and `highscore_path.csv`, none of which exist under those names. Now point at the `1.`-`4.` prefixed files.
- **Footgun defused.** `superseded/PathOptimization1.py` wrote `highscore_path.csv` with a two-column schema incompatible with the plotters, silently corrupting the pipeline for anyone who ran it. It now writes `superseded_shortest_path.csv`.
- **Normalisation implemented** in `a.PointSelection.py`, so the code matches the revised Equations 8-9 (Reviewer 2 Comment 4). Weights are now dimensionless, which also removes the x1e10 inconsistency between the two plotters.

**The repaired pipeline reproduces the committed route exactly**: 51 cells to 6 clusters, visiting clusters {0, 2, 3, 5}, matching `4.highscore_path.csv` cell for cell. This is a meaningful reproducibility result in its own right.

### FACTUAL CORRECTION — 51 cells, not 50

The committed `2.clustered_coordinates.csv` contains 51 rows, partitioned 9/24/6/10/1/1. The published figure therefore used **51** cells. The manuscript said 50 in two places; both corrected.

### Stability results (new Appendix F)

`src/PathPlanning/c.StabilityAnalysis.py`, output in `data/validation/sampling_plan_stability.csv`.

| Test | Result |
|---|---|
| Leave-one-out, cluster count preserved | 49/51 (96.1 %) |
| Leave-one-out, route preserved | 48/51 (94.1 %) |
| Co-association within multi-cell clusters | 0.987 to 1.000 |
| Bootstrap, 6 clusters recovered | 41.2 % (5 clusters in 43.4 %) |
| Bootstrap, most frequent selected set | 17.9 % |

**The contrast is the finding.** Cluster membership is essentially fixed, but which clusters the route visits is not. The reason is concrete: the route uses 5,647 m of its 6,000 m budget, so a modest change in weights makes a different combination feasible. The manuscript now says the identification of *where* the sensitive regions are deserves more confidence than the specific ordering of visits, and that such a plan is one good option among several of similar value rather than a uniquely optimal route.

**What this does not establish, stated in the text:** these tests resample *cells*, not *model configurations*. Sigma is still estimated from three runs, and the per-configuration fields needed to test a fourth or fifth were not retained. That remains future work.

### BLOCKER — broken virtual environment

`a.PointSelection.py`, `PathPlotter.py` and `PathPlotter2.py` cannot run: the venv has **attrs 18.2.0**, which provides only the `attr` module, while **`affine` 3.0.1 requires `attrs>=21.3.0`** for the `attrs` namespace. The chain `affine` to `rasterio` to `contextily` therefore fails on import.

`requirements.txt` does not pin `attrs`, so a clean install would resolve correctly; this venv is simply stale. Not fixed here, per the standing instruction not to install packages. **`pip install -U "attrs>=21.3"` in `.venv` would restore all three scripts.** `c.StabilityAnalysis.py` deliberately avoids contextily so the analysis runs regardless.

Manuscript at 33 pages, build clean, audit clean.


---

## Cover letter rebuilt against the compiled PDF (2026-09-08)

Written to `docs/manuscript/Cover_letter_revised.docx` rather than overwriting `Cover_letter.docx`, which was locked by Word at the time. The template's own styling is preserved (built from `Cover_letter_TEMPLATE_original.docx`). Validated: zip intact, XML well-formed, 315 paragraphs, 36 `Response:` and 36 `Changes in manuscript:` blocks, signed Russell Primeau.

Before writing it, the manuscript was audited to establish what is actually present: 9 tables, 11 figures and 6 appendices (A sensor specifications, B model configuration, C temperature validation by depth, D mass balance, E workflow/coverage/latency, F sampling-plan stability).

### Three responses now state that work is outstanding

The audit found three items I had previously assumed were done and which are not in the PDF. The letter says so rather than claiming them:

- **R2-9 (Figure 6).** Not addressed. Figure 6 still derives from the superseded two-month runs, so the axis definition, error bars and the disputed scaling cannot be settled until it is regenerated from the full-season runs. The letter confirms the reviewer was right to check the arithmetic and points to the measured timings now in Appendix E.
- **R1-5 and R1-6 (ensemble size, parameter ranges).** Not tabulated. Appendix B reports the calibrated values but not the number of configurations evaluated or the ranges explored. R3-1 carries the same caveat.
- **R1-4 and R3-2 (calibration/validation period split).** Not done. The withheld-forcing separation is explicit and the statistics are tabulated, but the season is not split temporally. The letter states this and offers to add it.

### Coherence issue to resolve before submission

**Figure 6 is inconsistent with Section 3.1.** Section 3.1 now reports full-season ThermalTune results, while Figure 6 plots the superseded two-month convergence study. A reader comparing the two will find different runs presented as the same campaign. Resolving R2-9 and this coherence problem are the same task.

### Tone

Where reviewers found real errors the letter concedes them directly and names what was wrong: the denitrification stoichiometry, the Equation 8/9 normalisation, the battery-capacity justification, the 50-versus-51 cell count, and the state of the repository. The covering summary leads with the fact that reported performance is now *worse* than in the previous draft and explains why that is the right outcome, rather than burying it.


---

## Reviewer references removed and prose tightened (2026-09-08)

Four passages in the rendered text referred to reviewers or to earlier versions of the manuscript, which is inappropriate: revisions stand on their scientific merit, not on who requested them. All four rewritten (turbulence closure note, mass balance appendix opening, coverage table introduction, stability appendix opening). Verified: zero occurrences of "reviewer" now render. `%` comments addressed to the author still mention reviewer numbers, which is useful and does not appear in the PDF.

The one remaining self-reference is the SSRN preprint disclosure, which is required and is retained.

Six new blocks were rewritten more tersely, with all figures and cross-references preserved: Section 3.1 (482 to ~300 words), Appendix C, Appendix D, Appendix F, the Section 2.4 hydrological passage and the Section 3.2 background comparison. Verified by comparison against a pre-edit copy: all 9 table labels, 11 figure labels, 6 appendix labels and 13 equation labels intact, and every quoted numerical value preserved.

One error was made and caught: the Appendix C replacement span included the depth-error table, deleting it and leaving `tab:depthrmse` undefined. The table was recovered verbatim from the pre-edit copy and reinserted; the build then returned zero undefined references.

## R2-9 answered, and Figure 6 was worse than the comment suggested

Investigating the axis definition exposed a more serious problem than the one raised. **Figure 6 plotted two-month and full-season runs on shared axes.** An RMSE accumulated over a two-month spring window is not comparable with one accumulated over a season that includes autumn cooling, so the figure invited exactly the comparison it should have prevented, and it is why the superseded two-month configurations appeared to outperform the full-season ones.

`src/D3D/CSVplotter.py` rewritten to plot only the 11 full-season configurations, excluding 14 shorter runs, with the reason documented in the module docstring.

**Axis definition.** The horizontal axis is simulated time per unit wall-clock time, a dimensionless speed-up, now stated in both the axis label and the text, with its observed range of 213 to 941.

**Scaling.** Checked against `Calibration.csv` rather than accepted from either side. On a consistent full-season basis at 40 layers, going from 36,197 to 65,900 3D cells changes RMSE from 1.336 to 1.325 °C, under 1 %, for a 1.6-fold increase in run time. Cost scales sub-linearly because the compared runs share a timestep count, so per-timestep overhead and output writing dominate at smaller meshes. The previously quoted 9,884-to-65,904 comparison mixed a low-resolution 2D mesh with a high-resolution one at equal layer count and is no longer used.

**Error bars.** Added as the RMSE range across configurations sharing a mesh and layer count. Because each point is a single deterministic simulation this is explicitly not a sampling error, and the text says so. The bar spans 1.076 to 2.852 °C at fixed mesh and layer count, driven by eddy viscosity and diffusivity.

**The finding this produces is stronger than the original claim.** Variation from settings other than resolution exceeds anything gained by refining the grid, which justifies fixing the mesh and directing effort at the physical parameters. That is a better argument than asserting convergence to an asymptote.

Manuscript at 32 pages, build clean, audit clean, 8 TODO comments in source and none rendering.


---

## R1-5, R1-6 and the remainder of R3-1 answered (2026-09-08)

The calibration campaign is now described concretely, from `hydro_explore_optimize.json` and `Calibration.csv` rather than from recollection.

**Section 2.2** describes calibration as the two-stage process it was. The first stage varied model structure (mesh resolution, vertical layers, water clarity, filtering options, vertical eddy coefficients, Courant limit, maximum timestep) across 25 configurations, 11 of them full-season. The second tuned nine continuous parameters for surface heat exchange and vertical mixing.

**The objective is now stated**, which matters because it determines what was actually optimised: a weighted sum of the hourly surface RMSE at double weight, the RMSE at 30 m, and the RMSE of depth-integrated heat content. The third term prevents a configuration scoring well by compensating a warm bias at one depth against a cold bias at another. Correlation and error at 1, 20, 30 and 40 m were monitored but not optimised, so they remain diagnostic rather than fitted. Search was a Sobol sequence followed by Nelder-Mead within a 60-simulation budget.

**New table in Appendix B** gives all nine parameters with search scale, bounds and selected value. Each selected value was checked against its bound: **none lies at a bound**, so the optimum is interior to the search space rather than truncated by it, and the manuscript says so.

Manuscript now 34 pages, 10 tables, build clean, audit clean, zero rendering placeholders and zero reviewer references in the rendered text.

## Cover letter updated

Rebuilt with corrected responses for R1-5, R1-6, R2-9 and R3-1, which previously stated the work was not done. The banner now names only the one item left open by choice.

Two admissions of incomplete work remain in the letter and are deliberate:

- **R1-4 and R3-2** — the season is not split into calibration and validation periods. The letter states this and offers to add it.
- **R2-7** — the letter is back to its submitted wording and still says the Figure 1 and Figure 3 redraws are outstanding. Figures 3 and 4 have since been redrawn, so **the letter understates what is done** and needs a pass by the author, who is also handling the Figure 1 annotation.

Note that the letter *does* refer to reviewers throughout, which is correct: it is addressed to them. The prohibition applies to the manuscript, where zero such references now render.


---

## Figure 2 caption completed, and two of my errors corrected (2026-09-08)

**Source of the request.** Reviewer 2 Comment 7 asks for the datum/projection, the source and resolution of the base imagery, and a link to Section 3.2, all in the caption. The link was made during Phase 1; the other two were left as a TODO because they could not be determined from any repository.

**My inference was wrong.** From `FlowFM_net.nc` I established that the model mesh is WGS 84 geographic (EPSG:4326) and suggested that as the likely figure datum. The author corrected this: the figure is rendered in Web Mercator (EPSG:3857), centred at 62.4722525 N, 6.4774372 E, over the ESRI World Imagery (Clarity) basemap. Both statements can be true at once, since the model CRS and the rendering CRS are independent, which is exactly why the inference should not have been offered.

Caption now reads: projection, centre point and base imagery, appended to the existing sentence. Per the author, imagery resolution is deliberately **not** added, since the scale bar conveys it directly and at whatever scale the figure is reproduced. The cover letter says so politely rather than silently omitting it.

**Second error, caught while regenerating the change list.** The earlier prose-tightening pass replaced a span in Section 3.2 that included the sentence pointing to the mass balance appendix. Appendix D was left orphaned, referenced from nowhere in the body. LaTeX does not warn about an unreferenced label, so the build stayed clean and the omission was invisible. Restored, and all six appendices are now verified as referenced from the body: sensorspecs 3, modelconfig 3, tempvalidation 1, massbalance 1, workflow 2, stability 1.

This is the second time a replacement span has swallowed adjacent content, after the depth table in Appendix C. Checking cross-reference counts, not just the build log, is the reliable test.

## Change list regenerated

`docs/revision/CHANGE_LIST.md` was stale: its line numbers dated from the Phase 0 and 1 revision, when the manuscript was 24 pages rather than 34, and it recorded only what had been done to the Figure 2 caption rather than what remained outstanding.

Regenerated against the current `main.tex` by locating each changed passage programmatically, so the line numbers are correct by construction and will not silently rot. 42 rows, all anchors matched. It now also carries an explicit table of outstanding items (the two figure redraws, the period split, the two declined analyses, and the uncommitted model configuration) and a list of the remaining TODO comments with their line numbers.

---

## Cross-document status audit (2026-09-08)

Internal documents (this tracker, `CHANGE_LIST.md`) and external documents (the compiled PDF, `Cover_letter.docx`) were checked against each other and against the repositories. Current true state: **34 pages, 10 tables, 11 figures, 6 appendices, 6 `%` TODOs, zero rendering placeholders, zero reviewer references in rendered text, zero undefined references or citations.**

### Statements corrected because they had gone stale

| Stale claim | Where | Truth |
|---|---|---|
| Model configuration "NOT YET COMMITTED" | `main.tex` TODO at the DAS | The 35 files (5.44 MB) are committed **and pushed**; `git ls-tree HEAD -- data/d3d` returns 35 and `main` is level with `origin/main`. TODO removed; the DAS is now true. |
| Status columns showing ⏸ Phase 2/3/4 | tracker, R1 / R2 / R3 tables | 19 of them had landed. Updated in place. |
| "Nine TODO markers remain" / "Six TODO comments remain" / "24 pages" | tracker, two places | Six TODOs, 34 pages. |
| Cover letter written to `Cover_letter_revised.docx` | tracker | It is `Cover_letter.docx` (319 paragraphs, 36/36 blocks). The `_revised` file no longer exists. |
| BLOCKER: broken venv, `attrs` 18.2.0 | tracker | Resolved by the author; `attrs` 26.1.0, contextily imports. |
| "Coherence issue: Figure 6 inconsistent with Section 3.1" | tracker | Resolved when Figure 6 was regenerated from full-season runs only. |
| "Commit the 5.45 MB model configuration" listed as outstanding | `CHANGE_LIST.md` | Done. |
| `adjustwidth` decision ☐ | tracker, cross-cutting table | Removed during Phase 0. |

### ⚠️ CONTRADICTION — the two computational-speed figures differ by a factor of ten

This is the most exposed claim left in the manuscript, and Reviewer 2 has already demonstrated a willingness to check this exact arithmetic.

- **Figure 6 and Section 3.1** report a speed-up of **213 to 941** times real time. From `data/Calibration.csv`, those eleven full-season runs took 11.6 to 23.7 wall-clock hours on the high-resolution 40-layer mesh.
- **Appendix E** reports **approximately 9,400** times real time: 212 simulated days in a median 32.5 minutes.
- The manuscript states one computing environment (Table 3) and offers this reconciliation: *"That figure refers to simulating an entire season during offline calibration, not to an operational update."* **This does not hold.** The 32.5-minute figure is itself an entire season, so the two numbers describe the same task and cannot be separated this way.

**Two further problems with the same sentence.** Appendix E attributes the timings to "nine full-season runs of the selected configuration." They are the nine runs in `D3DFMRunner/data/projects/tuner_fixed/tune_log.txt`, a one-at-a-time sweep over Ozmidov length scale, Forester iterations, and the Dalton and Stanton numbers. Their parameter values (Ozmidov 0 or 0.01; Dalton and Stanton -1 to -1.6; Forester 0, 5, 20 or 100) match **none** of the selected values in Table A3 (0.0266; -0.794; -1.466; 15), and their surface RMSE is about 2.08 against the selected configuration's 1.73. They share the mesh and vertical discretisation, not the configuration.

**Likely true explanation, not yet verifiable from the repositories.** The committed `dimr_config_parallel.xml` requests **12 MPI partitions**, and the stated hardware is 2 x Xeon Gold 5118, so 24 cores are available. A 10x speed-up from 12-way domain decomposition is entirely plausible. The `Calibration.csv` runs come from a different machine and path (`D:\Russell\Delft3D\Projects\ESwA\...`), and how they were partitioned is not recorded anywhere in either repository. **Author input needed:** were the ESwA calibration runs serial or fewer-partition? If so, both numbers stand and the fix is one sentence naming the partition counts.

### ⚠️ CONTRADICTION — Figure 6's best configuration outperforms the reported one, unexplained

Figure 6's vertical axis is labelled *mean depth-wise RMSE*, and its best full-season point reaches **1.076 °C**. Table 6 reports the selected configuration's *mean of 50 depth bands* as **2.15 °C**. Same quantity by name, twice the error, no explanation in the text.

The selected configuration is **not one of the eleven points in Figure 6**. The Figure 6 campaign runs 25 April to 20 November with Secchi depth 1.0 m, Courant limit 0.7, maximum timestep 30 s and Vicoww/Dicoww between 1e-6 and 1e-3. The selected configuration (`FlowFMnew.mdu`, now committed) runs 22 April to 20 November with Secchi 2.0 m, Courant 0.5, maximum timestep 20 s, Vicoww 5.27e-3 and Dicoww 6.06e-5 — every one of these outside the first-stage grid.

There is a defensible answer and the manuscript already contains half of it: the second stage optimised a weighted objective (surface RMSE at double weight, RMSE at 30 m, and depth-integrated heat content), not mean depth-wise RMSE, so the selected configuration is not expected to win on Figure 6's axis. What is missing is any sentence connecting the two, and the reader is left to infer that a configuration twice as accurate was available and passed over.

A related loose end: Section 2.2 lists the Courant limit and maximum timestep among the **first-stage** structural variables, but the selected values (0.5 and 20 s) appear in no first-stage run and are not among the nine second-stage parameters either. Where they came from is unstated.

### Repository — one concrete break at HEAD

51 files under `data/Nitrogen/` carry the decimal-separator normalisation (`_` to `.`) in the working tree but are **uncommitted**. `NewWAQPlots.py` and `WAQHisPostProcess.py` now set `CONFIG.decimal = "."` and raise on unparseable cells, so a fresh clone of HEAD fails on Figure 8 with a `ValueError`. The guard is behaving correctly; the committed data is what is wrong. The Data Availability Statement promises "the derived datasets from which the figures in this article are generated," so this must be committed before submission.

### Phase 5 work not started

No `src/paths.py`, `src/waq_io.py`, `src/geo_io.py`, `src/make_figures.py`, or `figures/README.md`. `src/D3D/__pycache__/*.pyc` are still tracked. `src/superseded/PathOptimization1.py` still present (now writing to its own filename, so no longer a footgun). `requirements.txt` still omits `pillow`.

### Follow-up, same day

- **Nitrogen CSVs committed** by the author. `git status` is clean apart from this tracker and the change list; the repository at HEAD now regenerates Figure 8. The corresponding row has been dropped from the change list's outstanding table.
- **Four hyperref warnings fixed.** `Token not allowed in a PDF string (Unicode)` fired twice for `superscript` and twice for `\circ`, both reported at the `\begin{document}` line because that is where hyperref writes the PDF info dictionary. The sources were the affiliation superscripts in `\Author` (MDPI template default, five of them) and the degree symbol added to the abstract during this revision. Both are now wrapped in `\texorpdfstring`, so the typeset output is unchanged while the PDF metadata reads "Russell Primeau, Razak Seidu, ..." and "1.7 degrees Celsius". Rebuilt: 34 pages, **zero** token warnings, zero undefined references or citations. The remaining log warnings are `fancyhdr` `\headheight` notices from the MDPI class and are cosmetic.

**Note on terminology used earlier in this file:** *DAS* means the Data Availability Statement (the `\dataavailability{}` block in `main.tex`).

---

## Speed-up contradiction resolved (2026-09-08)

Author confirmed: the calibration campaign behind Figure 6 was run **serially on a separate workstation**; the full-year ThermalTune run and the operational system use **MPI partitioning**. Confirmed independently in `ThermalTune/output/FlowFMnew.dia`, whose recorded command line is `dflowfm-cli.exe --partition:ndomains=12:icgsolver=6 FlowFMnew.mdu` — twelve partitions, PETSc solver.

Both figures therefore stand. The manuscript now says which scheme each belongs to:

- **Section 3.1** states that Figure 6's runs are serial, on a machine separate from Table 3, and that serial execution was deliberate — results are not exactly reproducible across partition schemes and several timing components scale poorly and unevenly with partition count, so holding the scheme fixed isolates the effect of the configuration. The axis is a relative comparison within that campaign, not operational throughput.
- **Appendix E** no longer calls those nine runs "the selected configuration" (they are a one-at-a-time sweep sharing only the mesh, vertical discretization and forcing) and now attributes the 32.5-minute median to the Table 3 machine under twelve MPI partitions.
- The old reconciliation sentence — "that figure refers to simulating an entire season ... not to an operational update" — is **removed**, because it was false: the 32.5-minute figure is itself a whole season. Replaced with the execution-scheme explanation, and with an explicit statement that any benchmark of the online workflow refers to the partitioned configuration.
- **Appendix B** gains a `Domain decomposition — 12 MPI partitions` row beside the solver.

Rebuilt: 34 pages, zero token warnings, zero undefined references or citations, zero rendering placeholders, zero reviewer references in rendered text, all six appendices referenced.

### ⚠️ NEW FINDING — a tuned parameter the solver ignored

`ThermalTune/output/FlowFMnew.dia` reports nine keywords accepted into `FlowFMnew.mdu` but never used. Seven are inert output or process switches. Two are worth attention, and one is a defect in a reported result:

> `** WARNING: While reading 'FlowFMnew.mdu': keyword [numerics] maxitverticalforester=15 was in file, but not used. Check possible typo.`

**Table A3 reports "Vertical Forester filter iterations, bounds 0 to 20, selected 15" as one of the nine tuned parameters, and the solver ignored it.** D-Flow FM 1.2.184 takes this per constituent (`Maxitverticalforestersal`, `Maxitverticalforestertem`); neither key is present in the `.mdu`, so the vertical Forester filter was at its default of zero throughout. The optimiser therefore explored a dimension with no effect on the model, and the manuscript reports a calibrated value for a setting that did nothing. A reviewer reproducing the run sees this warning in their own `.dia`.

This is an author decision and has **not** been changed: the honest options are to drop the row and describe eight tuned parameters instead of nine, or to keep it with a footnote recording that the setting was inactive. Note that Section 2.2's first stage separately varied "the horizontal and vertical filtering options" through the `HMF?` and `VFF?` columns of `Calibration.csv`, which are different keys — that statement is unaffected.

The second warning, `[wind] cdbreakpoints` and `windspeedbreakpoints` unused, is **benign**: `ICdtyp = 6` selects the Wüest (2005) formulation, which computes the drag coefficient rather than interpolating breakpoints. The values are inert leftovers, not a misconfiguration.

---

## Forester row dropped, file names purged, Figure 6 reconciled (2026-09-08)

### Vertical Forester filter

Per the author, the row is **removed** rather than footnoted. Later calibration iterations found that increasing this value was generally harmful to accuracy; the Figure 6 campaign did use it, but the calibration behind the reported results did not. The second stage is now described as **eight** continuous parameters, in Section 2.2, in Table A3 and in the cover letter. No note about the ignored keyword appears anywhere in the manuscript — the setting is simply not part of the reported calibration.

Section 2.2's first stage still lists "the horizontal and vertical filtering options" among the structural variables, which remains true of the campaign it describes.

### Author directive — no file or project names in the manuscript

**Standing rule: the rendered text must contain no file names, paths, project names or script names.** The reader must be able to follow everything without opening the repository; sharing the files is supplementary validation, not a substitute for description. Use general descriptive terms for assumptions and configuration.

Audited by scanning the rendered text for snake_case, camelCase, filename extensions and Windows paths, then re-scanning the compiled PDF independently. **One violation found and fixed:** Appendix F ended with "reproducible from the repository via `src/PathPlanning/c.StabilityAnalysis.py`", now "reproducible from the accompanying repository."

Everything else the scan raised is benign: `\label` and `\citep` keys (which do not render), math subscripts, `pH`, `gN`, `fDOM`, and a manufacturer datasheet URL. The cover letter is clean by the same test.

**One deliberate exception**, flagged rather than removed: the Data Availability Statement contains the repository URL, which ends in the repository's name. A repository cannot be shared without naming it, and the journal requires the link. It is confined to the statement whose purpose is to give it.

### Figure 6 contradiction closed

Added to Section 3.1, after the mesh-resolution conclusion:

> The configuration reported below is not among the points plotted here. It was selected in the second stage, against a weighted objective dominated by the surface series and by depth-integrated heat content rather than by the depth-averaged error on this axis, and with values of water clarity, timestep, Courant limit and vertical mixing outside the range explored in the first. It therefore scores worse on this axis than the best point shown, and the two are not competing candidates under the same criterion.

This removes the unexplained gap between Figure 6's best point (1.076 °C) and the 2.15 °C reported in Table 6 for the same named quantity, and it does so without naming any run, file or project.

Rebuilt: 34 pages, zero token warnings, zero undefined references or citations, zero rendering placeholders, zero reviewer references, zero file names.

---

## Framing made explicit, and R2-7 closed (2026-09-08)

### Author-supplied figures close two outstanding items

Figures 1, 3 and 4 have been redrawn by the author, with the captions updated to match. This closes **R2-7 in full**, which had been the last reviewer comment carrying outstanding work other than by choice.

- **Figure 1** now names this system's own components — sensors and water body, data processing and the hydrodynamic water quality model, and the three applications — closing the real-to-virtual-to-application loop, in place of the generic Grieves diagram.
- **Figure 3** draws the withheld-data decision explicitly: the first profile of the season sets the initial condition, every later profile is marked *never forcing*, and all of them pass instead to validation and model selection.
- **Figure 4** carries the update rates the reviewer asked to see, attached to the steps they govern: retrieval at each platform's publication interval, an hourly model run at twelve MPI partitions costing about a second per simulated hour, and a nowcast published under two hours old. The partition count agrees with the Appendix B row added earlier the same day.

Putting the rates on the update loop rather than on the conceptual framework figure is the better placement, and the cover letter now says so rather than claiming the request was met literally.

### Three framing points now stated in the text

The author identified three things a reader must not have to infer. All three are now in the Introduction.

**1. The method is not what is under test.** Section 1.3 states that the capabilities and limitations of process-based hydrodynamic water quality modelling are established in the reviews cited, that evaluating them is not an aim of this study, and that the governing equations, the discretization and the solver are standard and applied as published, with none of the modelling machinery offered as a contribution. Section 2.2 already described the solver as off-the-shelf; the Introduction now says it first.

**2. Why 3D process-based.** A new paragraph gives both halves of the argument. Predictions derived from conservation laws can be interrogated, tested against quantities they were not fitted to, and extended beyond a short observational record — with the machine-learning emulation of reservoir water quality cited as the comparison point. And resolving vertical and horizontal structure is a precondition for all three applications: the abstraction point lies at depth, the depth at which a plume travels determines whether it reaches that point, and the sampling method depends on contrast between locations.

**3. Novelty is the integration.** The claim in Section 1.2 has been rewritten. It previously rested on "a process-based twin of a drinking water source reservoir, validated against in situ observations", which put the weight on the model. It now states that what is novel is not the model, the equations or the solver, all of which are standard, but the systems integration of a near real-time in situ sensing network with a three-dimensional process-based model of a drinking water source, and the applications the coupling makes possible.

The contributions paragraph was adjusted from "What is technically new here" to "What this paper adds to that work", so it no longer reads as a claim of technical novelty in the model itself.

### Prior art that had to be acknowledged

Searching the bibliography for support surfaced an entry staged but never cited: an operational online three-dimensional forecasting platform for lake hydrodynamics, with a companion automated calibration framework. **Leaving this uncited while claiming a three-dimensional process-based twin as the distinguishing feature would have been a real exposure.** Both are now cited in the novelty paragraph, and the claim is differentiated on the drinking-water-source application and the integration rather than on the dimensionality of the model.

Six previously staged, uncited entries are now used: the dimensionality study, the machine-learning emulation paper, the two Baracchini papers, and two modelling overviews. All resolve; the build reports no undefined citations.

### Cover letter aligned

Three changes: the novelty response now matches the reframed claim and names the acknowledged prior art; the R2-7 response says both figures have been redrawn and explains where the update rates went; and a new paragraph in the covering summary states the scope of the modelling claim, so a reviewer meets it before the point-by-point section.

Manuscript now **35 pages**, build clean, zero undefined references or citations, zero rendering placeholders, zero reviewer references, zero file or project names. Change list at 52 rows, all anchors matched.

---

## Review of the author's manual revision (2026-09-08, later)

The manuscript was substantially rewritten by the author between sessions. It is shorter (28 pages), more careful, and corrects several errors of mine. Five of the six remaining TODOs were resolved; one remains, on manufacturer accuracy and resolution columns.

### Build defects found and fixed

- **The document did not compile.** Two blank lines inside the Equation 10 display terminated math mode, so LaTeX reported *Missing $ inserted* and abandoned the rest of the document at page 27. Blank lines removed; no content changed.
- **Two citations had no bibliography entry.** `Piccolroaz2024` and `Hipsey2020assessment` were cited in Section 1.3 and the Discussion but were absent from `sources.bib`. Both entries added, **verified against the Crossref API rather than recalled**: Piccolroaz et al., *Reviews of Geophysics* 62(1) e2023RG000816, doi 10.1029/2023RG000816; Hipsey et al., *Environmental Modelling & Software* 128, 104697, doi 10.1016/j.envsoft.2020.104697. Both are apt for the passages that cite them.
- **A dangling figure reference.** Appendix C and Section 3.1 both point to a residual plot, and the residual dataset and its plotting script existed, but no float carried the label, so `Figure ??` rendered. The float was added.

### My own duplicated work, withdrawn

I wrote `src/D3D/ResidualPlotter.py` before noticing that `src/D3D/ExportThermalResiduals.py` already existed and targets the same `Fig14.png`. Mine has been deleted and the figure regenerated with the author's script, which is the better of the two: three stacked panels matching the depth-validation figure rather than three overlaid series. Two scripts writing one filename is the same footgun as the superseded path optimizer.

### Corrections the author made to my work

- **"Warm bias persists at every depth" was wrong.** The column I described as a bias is the error at the last paired time. The table caption now defines it, and the text states that it is not mean seasonal bias. The residual figure shows why this mattered: at 1 m the model runs about 1.45 °C *cool* on average, so a persistent warm bias was never true.
- **The stability analysis had a real bug of mine.** DBSCAN relabels clusters between runs, so comparing label sets counted relabelling as a changed route. Comparing the original geographical regions instead moves the bootstrap agreement from 17.9 % to 63.3 %. The rewritten script also emits the LaTeX fragment the appendix inputs, so the reported numbers cannot drift from the analysis.
- **The calibration narrative was withdrawn.** The two-stage description, the Sobol and Nelder--Mead search, and the tuned-parameter table are gone. The configuration reported is supplied rather than optimised within this study, and the appendix now says so: *"No private optimization procedure is part of the study reported here."* This is the honest position and it supersedes the R1-5, R1-6 and R3-1 responses as previously written.
- **The operational loop is no longer described as running.** The abstract, Figure 4's caption and Appendix E now distinguish implemented components from a demonstrated unattended service, and the under-two-hours latency claim is withdrawn as unmeasured.

### Cover letter re-synchronised

Every number the letter asserts was checked against the manuscript and the appendix fragments it inputs. **Fifteen paragraphs asserted things the paper no longer contains** and were rewritten: the calibration procedure and parameter table (R1-5, R1-6, R3-1), the grab-sample percentage comparison (R2-2), the stability figures (R2-3), the mass-balance residual, which is 0.0085 % not 0.015 % (R2-5), the speed-up range (R2-9), the automation claims (R3-3), and the latency and robustness claims (R3-4). Re-checked afterwards: the only numbers now in the letter but not the manuscript are section numbers and the reviewer's own arithmetic quoted back in the comment text.

### Repository

The rewritten Data Availability Statement asserts that *"the repository documents which plots can be regenerated from those artifacts."* That was not true: `README.md` still carried empty `Fig. ()` placeholders, a duplicated bullet and pre-rename filenames. It has been rewritten with a figure-by-figure provenance table distinguishing what regenerates here from what comes from solver post-processing that is not distributed. Provenance was verified per figure rather than assumed; two rows were corrected during writing, since neither the profiler calibration history nor panel (a) of the sampling-plan figure is produced by any script in this repository.

All eight scripts run to completion from the repository as it stands.

---

## Calibration discussion reinstated, without the automated search (2026-09-08)

Per the author: the calibration iteration and its table go back in, but **nothing** describing the optimizer or search methods implemented in `D3DFMRunner` — no Sobol exploration, no Nelder--Mead refinement, no evaluation budget, and no weighted objective. That configuration describes a different process from the one that produced these results. The author's point stands on its own: a procedure carried out by hand is not thereby less informative, and reporting it does not oblige the study to ship the tooling.

### Sources used, and deliberately not used

| Reinstated content | Source |
|---|---|
| Twenty-five configurations, eleven full-season | `data/Calibration.csv` |
| Ranges for mesh, layers, clarity, filtering, vertical eddy coefficients, Courant limit, timestep | `data/Calibration.csv` |
| Selected values for Dalton, Stanton, Ozmidov, Prandtl and the four eddy coefficients | the committed `.mdu` |
| *Nothing* | `hydro_explore_optimize.json` |

### What went into the manuscript

- **Section 2.2** now opens the calibration description with "by iterative adjustment across successive runs rather than by an automated search", lists the settings varied with a pointer to the new ranges table, names the parameters adjusted in the later iterations, and states the basis on which iteration stopped: comparison against the withheld profiler observations, continued until further adjustment produced no further improvement. It says plainly that the retained configuration is the best of those tried rather than the result of a formal optimization, and that the sequence of trials is not a reproducible search path.
- **New Table A3**, *Settings varied during the calibration campaign*, with the range covered for each of nine settings, followed by a note that the later hand-adjusted parameters have no retained range and that their values appear in the configuration table.
- **Ozmidov length scale** added to the configuration table, which had omitted it.
- The three sentences that had disclaimed any describable process were rewritten: Section 2.2's "a separate supplied configuration", Section 3.1's "was supplied separately... does not describe its optimization history", and Appendix B's "No private optimization procedure is part of the study reported here". Each now distinguishes campaign membership from provenance without denying that a process existed.

The Forester filter row stays out, for the reason the author gave and because the solver's own log records the keyword as read but unused.

Verified after the edit: zero occurrences of Sobol, Nelder--Mead, simplex, evaluation budget or weighted-objective language in the rendered text. Build clean at **29 pages**, zero errors, zero undefined references.

### Cover letter

Eight paragraphs rewritten across R1-5, R1-6 and R3-1. One of them, on the weighted objective with the surface series at double weight, was a description of the automated optimizer that my earlier sweep had missed entirely; it is replaced by the statement that the adjustment was made by hand. A guard now asserts that none of the withdrawn vocabulary survives anywhere in the letter except where a reviewer's own comment is quoted back.

### Note for future edits to the letter

**Paragraph indices are not stable.** The document was opened and saved in Word between sessions, which merged runs and took the paragraph count from 320 to 256. Index-based edits silently hit the wrong paragraph or fail outright. All edits are now anchored on a distinctive substring of the target paragraph and assert a unique match.

### latexdiff

`latexdiff` needs the pure-Perl module `Algorithm::Diff`, which is absent from the only Perl on this machine, Git Bash's `/usr/bin/perl`. No installation is being requested: the same marked-up `.tex` can be produced with Python's standard-library `difflib`, which needs nothing added. That route requires reading the submitted `.tex` from the manuscript repository history, which needs the author's approval first.

### CORRECTION — an unsupported provenance claim, withdrawn (2026-09-08)

The author challenged the reinstated text and was right to. **My error was not confusing Figure 6 with the tuner runs** — those are kept distinct throughout — but asserting that the reported thermal configuration came from *"later iterations"* of the manual campaign behind Figure 6, and then inventing a stopping rule for it. Neither was supported by anything. I inferred a lineage from the instruction to reinstate the calibration discussion rather than from evidence.

The evidence runs the other way. All nine parameters in the committed `.mdu` are exactly the nine in the optimizer's parameter list, every one interior to its configured bounds and non-round to six significant figures:

| Parameter | Value | Configured bounds |
|---|---|---|
| Dalton | $-0.79447$ | $-1.6$ to $-0.6$ |
| Stanton | $-1.46559$ | $-1.6$ to $-0.6$ |
| Xlozmidov | 0.0266392 | 0.0 to 0.1 |
| PrandtlNumberTemperature | 0.192679 | 0.1 to 10.0 |
| Vicoww | 0.00527104 | 1e-06 to 0.01 |
| Dicoww | 6.06011e-05 | 1e-05 to 0.001 |
| Vicouv | 0.0225008 | 0.001 to 0.3 |
| Dicouv | 0.0953328 | 0.001 to 0.3 |

That is the signature of an automated search result, not of hand-picked values, and it is consistent with the author's original statement that no such procedure is part of the study reported here.

**Resolution, confirmed by the author.** The manuscript says nothing about how the reported configuration was reached. What remains is only what `Calibration.csv` supports: the configuration campaign behind Figure 6, described as proceeding "by iterative adjustment across successive runs rather than by an automated search" — with that sentence now bound grammatically to the campaign so it cannot be read as a general claim — and Table A3's ranges, scoped explicitly to that campaign in three places. The reported configuration is presented by its settings alone.

**Appendix E's throughput benchmark stays**, per the author: the nine runs share the mesh, vertical discretization and period, so the median of 32.5 minutes characterizes the solver on that hardware regardless of why the runs were launched. The manuscript describes them only as "nine supplied full-season runs sharing a common mesh and vertical discretization".

**Cover letter re-synced again.** Four paragraphs still carried the withdrawn lineage. R1-6 now separates what can be answered from what cannot: the campaign's settings and ranges are reported; for the evaluated configuration the settings themselves are given rather than a tuning history, and no stopping criterion is supplied, because reconstructing one after the fact would be worse than saying nothing. The guard list now also rejects "later iterations", "made by hand" and "best of those tried".

**Lesson recorded:** when told to reinstate removed material, reinstate only what the sources support. The instruction said what to restore, not that a lineage existed between two run sets. The two remaining uses of "optimization" in the manuscript are the route optimizer in Sections 2.3 and 3.3, which is unrelated.

---

## Cover letter: responses trimmed to the change (2026-09-08)

Per the author, the individual responses had accumulated a great deal of material that does not belong in them: descriptions of the previous state of the manuscript, code and data; endorsements of a reviewer's opinion; and third-person references to the reviewer. A response should say what changed, or what did not, and stop.

Fifty paragraphs rewritten. Removed throughout:

- **Endorsements** — "The reviewer was right to ask", "The reviewer is correct and we are grateful for the close reading", "Both points are accepted", "We accept this", "We agree that", "Reviewer 3 was right".
- **Previous-state narration** — "has been promoted out of the middle of a methods paragraph", "Section 2.4 no longer says", "the comparison makes the failure visible in a way the previous figure did not", "the previously quoted comparison mixed meshes... and is no longer used".
- **Meta-commentary** — "We should be straightforward about", "In preparing this response we found", "Checking the arithmetic exposed a more serious problem than the one raised", "Thank you for bringing this to our attention".

**Brief concessions retained**, per the author's follow-up: politeness stays, and acknowledging that something was wrong or misleading is appropriate where a reviewer found a genuine error, provided it is one clause and not a paragraph. So the letter still says "Equation 12 was wrong as printed", "The inconsistency was real", "The claim was too strong", "This justification was not supported", "The count was wrong", "the earlier wording was open to that reading", and "The repository did not support reproduction as submitted" — each followed immediately by the change.

The covering summary is kept and lightly tightened; it is addressed to the editor and reviewers, so collective references there are appropriate. Navigational cross-references between comments ("addressed under Reviewer 2, Comment 11") are also kept, since they save the reader hunting.

Letter now 6,393 words across 256 paragraphs, 36 comments each with a Response and a Changes line. Re-verified afterwards: the only numbers in the letter that are not in the manuscript are section numbers and the reviewer's own arithmetic quoted back in a comment.

---

## Two arguments added (2026-09-08)

### Observability, in Section 1.3

The strongest motivation for a process-based model had been left implicit: it is not only about interpretability, but about what can be observed at all. A new paragraph states that many contaminants are hazardous at concentrations only laboratory analysis resolves, while instruments suitable for continuous deployment cover a limited set of largely physical and optical parameters. Where a hazard is optically expressed it can be observed at high frequency and over wide areas; for a dissolved contaminant established only by grab sampling, no comparable observation stream exists, so neither a data-driven surrogate nor a soft sensor has enough data to be trained or verified against. The paragraph concedes that a process-based model is not exempt from that scarcity, and closes on what it does retain: internal consistency with the conservation laws it solves.

Three previously staged but uncited entries now support it: a review of online surface water quality monitoring technology, a chapter on on-line monitoring for drinking water contamination, and a review of physical-to-virtual sensing.

**Correction to the author's framing, and it strengthens the argument.** The author described Qiu et al. as using optical sensors for chlorophyll. Checking the paper, its monitoring is **video-based observation and satellite remote sensing** -- its own keywords are "satellite remote sensing" and "video monitoring". The text therefore says that the framework tracks algal blooms by video and satellite imagery. This makes the contrast sharper rather than weaker: a surface bloom is visible at a distance, which is exactly what a dissolved contaminant is not.

### Areas for future work, in the Conclusions

The Conclusions previously disposed of future work in one sentence. It now carries an explicit list of seven areas, ordered by how directly each bears on the claims made: chemical and biological validation against a tracer experiment or monitored release; independent validation of the velocity field; transport-specific mesh convergence; the calibration/validation split together with resampling over model configurations; field execution of a planned mission and comparison against alternative sampling strategies; end-to-end operation of the update loop as an unattended service; and replication at water bodies differing in size, depth, residence time and dominant hazard.

The list covers both the analyses deferred from the review and the tasks needed to establish the approach and its transferability independently of any comment. It closes by saying that none is addressed here and that the claims should be read accordingly.

Three responses in the cover letter now point at it, so the deferred items are visibly captured rather than left as promises scattered across the letter.

Build clean at 29 pages, zero errors, zero undefined references.

### Why temperature is the calibration target (2026-09-08)

Section 2.2 already noted, citing Xia et al., that calibrating a 3D hydrodynamic model to temperature alone can overlook important dynamics but remains common practice. What it did not say is *why* the alternative is not taken. Three sentences added:

> The alternative is seldom available. Measuring a three-dimensional velocity field across a water body of this size requires instrumentation deployed at many locations and depths at once, and surveys of lake modelling practice describe calibration as contending with limited direct measurements rather than a surplus of them. Assessments of aquatic ecosystem models likewise find that validation routinely stops at the comparison of simulated state variables against observations, with the process rates and fluxes that would constrain circulation seldom tested.

This turns "no velocity data exist at this site" from a local excuse into a statement about the field, which is the stronger position and is consistent with the equifinality limitation in the Discussion.

**Citations.** `Hipsey2020assessment` was already in use and is the precise support: its assessment hierarchy distinguishes conceptual, state, process and system validation and reports that only the first two are routinely undertaken. A new entry was added and **verified against the Crossref API**, not recalled: Regev, Mesman, Paule-Mercado, Schmid and Siebers, *Navigating lake modelling and calibration: insights from literature and community practice*, Ecological Modelling 515, 111529, 2026, doi 10.1016/j.ecolmodel.2026.111529. Its abstract names limited direct measurements among the recurring challenges of lake model calibration, so it supports the claim made rather than being cited on the strength of its title. Both resolve in the rendered bibliography as [55] and [22].

Build clean at 29 pages, zero errors, zero undefined references.

## Jargon sweep (2026-09-08)

Scanned the rendered text for specialist limnological, numerical, chemical and statistical vocabulary, reporting every term with its first use, its section and its context, so that each could be judged as remove, gloss or keep.

**Removed from the abstract.** "Metalimnion" is gone, along with the depth-band framing and the over-specific "at 2.95~m depth". The clause now reads: a root-mean-square error of 1.73 °C near the surface and 2.15 °C averaged across depth, with the largest discrepancies at intermediate depths in summer. The headline numbers that Reviewer 1 Comment 1 asked for are retained; the stratum name is not. **The abstract now contains no specialist vocabulary at all.**

**Replaced with plain words.**

| Was | Now |
|---|---|
| "Within lentic surface waters" | "Within lakes and reservoirs" |
| "with larger metalimnetic errors" (Conclusions) | "with the largest errors at intermediate depths" |
| "This dimictic, oligotrophic enlarged natural lake" | "The lake is nutrient-poor, and mixes from top to bottom twice a year, in spring and autumn." |
| "turnover in dimictic lakes provides uniform initial and final conditions" | "these twice-yearly mixing events leave the water column at a uniform temperature, providing well-defined initial and final conditions" |
| "the epilimnion, metalimnion and hypolimnion" (Appendix C) | "the surface mixed layer, the transitional layer in which temperature falls sharply with depth, and the cold deep water beneath it" |

**Glossed at first use**, where the term earns its place: vertical stratification ("the layering of a water column by temperature and density"); nowcast ("an estimate of conditions as they are rather than a forecast of conditions to come"); eutrophication ("the nutrient enrichment that drives algal growth"); DBSCAN (now "a density-based clustering analysis (DBSCAN)"); fDOM (expanded to fluorescent dissolved organic matter in the instrument table).

**Kept without gloss, deliberately.** The numerical vocabulary in Section 2.2 and the model configuration appendix -- Courant limit, advection, closure, hydrostatic, eddy viscosity, z-layers, PETSc, Perot, Ozmidov, Smagorinsky, turbulent Schmidt and Prandtl numbers. These sit beside the governing equations and in a table of solver settings whose purpose is reproducibility; a reader who needs them knows them, and glossing each would bury the section. Turbidity, ammonium and nitrate are standard for the venue.

**No DBSCAN citation was added.** The canonical reference is a 1996 conference paper without a DOI, and the entry could not be verified through Crossref, so the algorithm is named and described rather than cited.

Build clean at 29 pages, zero errors, zero undefined references, zero token warnings.

## Document-history language removed (2026-09-08)

Per the author, nothing in the manuscript may refer to a preceding version of the document or code, or to reviewers, editors, comments or review. Everything must read as the author addressing the reader, not as commentary on the document.

Scanned the rendered text for "revised", "previous", "earlier", "prior", "former", "supersedes", "no longer", "now", "has/have been added or corrected", "in response to", "this draft", "the present version", and for reviewer, editor, referee and comment.

**Result: zero references to reviewers, editors, referees or comments were found in the rendered text**, and zero instances of "now" used as document commentary. That part was already clean.

**Fourteen fixes made.** "Revised" appeared eleven times and meant something only relative to a draft the reader has never seen. The runs are renamed so each is self-contained.

| Was | Now |
|---|---|
| the revised thermal run / simulation | the thermal simulation |
| *Revised thermal configuration performance* (table caption) | *Thermal simulation performance* |
| Because the historical and revised runs differ | Because the campaign runs and the thermal simulation differ |
| the historical configuration campaign / comparison | the configuration campaign / comparison |
| not the configuration of every historical experiment | not the configuration of every experiment reported here |
| retain the earlier scenario outputs | use outputs from a separate scenario configuration |
| The earlier scenario uses meteorological forcing | The scenario simulation uses meteorological forcing |
| Neither describes the earlier contaminant demonstrations | Neither describes the contaminant demonstrations |

The preprint disclosure previously enumerated what had changed since the preprint: *"The present article supersedes that version and presents the revised thermal evaluation, expanded model and sensor documentation, and explicit distinctions between demonstrated capabilities and proposed operational use."* That list is document commentary and is gone. What remains is a scholarly cross-reference: **"A preliminary account of this work is available as a preprint [9]; the present article supersedes it."**

This is the one place a preceding version is still named. It is kept deliberately: declaring a preprint is a disclosure obligation, it was asked for in the text, and the wording now reads as a citation of a separate deposited artifact rather than as revision history. Removing it entirely is the author's call.

**Kept as legitimate content**, since they describe the world rather than the document: "prior knowledge" and "previously computed timestep" in the model description; "prior applications to seasonally stratified lakes" in the literature; "Previous assessment has identified several specific hazards" about earlier studies of the lake; "weather forcing data from previous years"; and "systems of this kind are no longer rare" about the state of the field. Also kept: "retained", "archived" and "supplied", which describe data provenance, not document versions.

**Two remaining hits in the PDF are publisher boilerplate**: the "Received / Revised / Accepted" date block that MDPI fills in, and the Disclaimer/Publisher's Note referring to "the editor(s)". Neither is author text.

Build clean at 29 pages, zero errors, zero undefined references, zero token warnings, one TODO comment remaining.

---

## Pre-submission pass (2026-09-08)

### Done in this pass

- **PDF reduced from 25.6 MB to 14.6 MB.** Figure 2 was 4348 px wide with an alpha channel, rendered at 0.99 textwidth: about 670 dpi, more than twice what print resolves. Resampled to 3200 px (about 490 dpi, still well above the 300 dpi minimum) and flattened to RGB. Figure 5's alpha channel was dropped at full resolution. Originals are backed up in the session scratchpad under `fig_originals/`.
- **DRAFT banner removed from the cover letter.** It instructed its own deletion before sending, and everything it asked to be verified has been. The one item left open by choice is stated twice in the letter body, so nothing is lost.
- **False claim corrected.** Appendix A said the instrument table "combines manufacturer specifications with the operational calibration record". It carries no manufacturer specification columns. Now: "reports the measured parameters, their units and the operational calibration record for each channel." This matters because it is the exact table Reviewer 2 Comment 7 asked about.

### Verified clean

Build: 29 pages, zero errors, zero undefined references or citations, zero token warnings. No dangling cross-references, no unreferenced figure or table labels, no space-before-punctuation. Letter and manuscript agree on every number; the only numbers in the letter not in the paper are section numbers and the reviewer's own arithmetic quoted back. The 3.5 kg mass basis is arithmetically consistent: 3.5 kg NH4NO3 at 35 % nitrogen gives 1.225 kg N, split as 0.6125 kg each.

### Left for the author

**Blocking.** Nothing is committed or pushed in either repository. The Data Availability Statement points at the GitHub repository, so it is false until this is done. Uncommitted: `main.tex`, `sources.bib`, `Cover_letter.docx`, and untracked `Fig3.svg` and `Fig4.svg` in the manuscript submodule; `README.md`, the plotting scripts, the stability analysis and the regenerated figures in the superrepository.

**Author action.** Red highlighting: the passage-level change list is superseded, so highlight whole sections per `CHANGE_LIST.md`.

**Optional, roughly fifteen minutes.** The single remaining TODO adds manufacturer accuracy and resolution columns to the instrument table from the EXO manual. With the false claim above now corrected, leaving them out is defensible; adding them closes Reviewer 2 Comment 7 completely.

**Known soft inconsistency.** Figure 4 still annotates the nowcast as "under 2 h old" while Appendix E states the full interval has not been measured. The caption frames the whole figure as a proposed loop, which covers it, but the annotation would be better as a design target or removed. Needs an edit to `Fig4.svg`.

**Standing assumptions a reader may probe.** The mass balance is computed on a nutrient run rather than the release scenario, and says so. The provenance of the reported configuration is deliberately unstated. Figure 9a and Figure 10 are not reproducible from the repository, which `README.md` records.
