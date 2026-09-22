# Scenario simulation

Inputs and reduced outputs for the nitrogen-release scenario in Section 3.2 and
Figures 7–8.

| File or directory | Contents |
| --- | --- |
| `flowfm/input/` | D-Flow FM configuration and forcing. `Blast.pli` and `Blast.tim` define the source location and inflow. |
| `waq/input/` | DELWAQ substances, numerical settings, source composition and rates, and output timers. |
| `waq/coupling/` | Coupling manifest `FlowFM.hyd` and boundary file `FlowFM.bnd`. |
| `series/` | Depth-averaged ammonium and nitrate time series at five monitoring sites, used in Figure 8. |
| `fields/nh4_36h.nc` | Ammonium field and mesh at 2024-08-02 16:00, 36 hours after release, used in Figure 7. |
| `observations/` | Laboratory grab samples of in-lake ammonium and nitrate. |

The release is defined in
`waq/input/includes_deltashell/load_data_tables/EUTROPH.tbl`.
Generate Figures 7 and 8 from the repository root:

```sh
python src/figures/make_fig7.py
python src/figures/make_fig8.py
```

## Coupling and extraction

The coupling binaries are not included. Regenerate them using the configuration
and forcing in `flowfm/input/`; `waq/coupling/FlowFM.hyd` records the required
coupling. DELWAQ inputs use `<COUPLING>` in place of an external path.
[ResolveCouplingPaths.py](../../src/model/ResolveCouplingPaths.py) documents how
to substitute the regenerated coupling directory.

`make_fig7.py --extract --runs-dir PATH` rebuilds the field extract from raw solver
output. [VerifyScenarioProvenance.py](../../src/model/VerifyScenarioProvenance.py)
checks the site series against that output with the same flags. Both require the
external run archive; see [Materials not published](../../README.md#materials-not-published).
