# A Digital Twin Prototype for Protecting Surface Source Waters

Code, model inputs, and data accompanying the article of the same name, which
presents a digital twin prototype for the Brusdalsvatnet drinking water reservoir
in Norway. The Python scripts reproduce the figures and selected tables from the
included data.

## Contents

| Directory                                                          | Contents and manuscript references                                                                            |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [Configuration comparison](data/configuration_comparison/README.md) | 24 run records representing 21 model configurations; Figure 6 and Table A3.                                   |
| [Thermal simulation](data/thermal_simulation/README.md)             | Model inputs, profiler records, and temperature comparisons; Table 3, Figure 5, Figures A2–A3, and Table A4. |
| [Scenario simulation](data/scenario_simulation/README.md)           | Inputs and reduced outputs for the nitrogen-release scenario; Figures 7–8.                                   |
| [Transport ensemble](data/transport_ensemble/README.md)             | Conservative-tracer ensemble and mesh/layer refinement cases; Figure 9a and Tables A5–A7.                    |
| [Sampling plan](data/sampling_plan/README.md)                       | Retained cells, clusters, route, and supplementary analyses; Figure 9, Appendix G, and Table A10.             |
| [Profiler calibration](data/profiler_calibration/README.md)         | Calibration records and surface-sonde operating hours; Figure 10.                                             |

## Setup and reproduction

Run commands from the repository root using a Python environment with the packages
in [requirements.txt](requirements.txt):

```sh
python -m pip install -r requirements.txt
python src/figures/make_fig8.py
```

The analysis and plotting scripts use the included data and run offline. Figures
and generated LaTeX fragments are written to the untracked `output/` directory.
Sampling scripts and extraction commands also write files under `data/`; some
scripts print summaries to the terminal.

### Figures and tables

Figures 1–4 are a framework diagram, a site map, and two component schematics.
Their source materials are not included in this repository's reproduction workflow.

| Manuscript item               | Script                                                              | Output or supporting data                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Figure 5; Table A4 statistics | [ExportThermalProfiles.py](src/model/ExportThermalProfiles.py)       | `Fig5.png`; `--extract` rebuilds `data/thermal_simulation/validation/temperature_by_depth_2024.csv`, supporting Table A4. |
| Figure 6                      | [CSVplotter.py](src/model/CSVplotter.py)                             | `Fig6.png` from `data/configuration_comparison/calibration.csv`.                                                            |
| Figure 7                      | [make_fig7.py](src/figures/make_fig7.py)                             | `Fig7.png` from `data/scenario_simulation/fields/nh4_36h.nc`.                                                               |
| Figure 8                      | [make_fig8.py](src/figures/make_fig8.py)                             | `Fig8.png` from `data/scenario_simulation/series/`.                                                                         |
| Figure 9                      | [make_fig9.py](src/figures/make_fig9.py)                             | `Fig9.png` from `data/sampling_plan/`.                                                                                      |
| Figure 10                     | [make_fig10.py](src/figures/make_fig10.py)                           | `Fig10.png` from the two CSVs in `data/profiler_calibration/`.                                                              |
| Figure A2                     | [make_fig11_13.py](src/figures/make_fig11_13.py)                     | `Fig11.png`–`Fig13.png` from the thermal validation records.                                                               |
| Figure A3                     | [ExportThermalResiduals.py](src/model/ExportThermalResiduals.py)     | `Fig14.png` from the thermal residual records.                                                                                |
| Table A3                      | [BuildCalibrationTable.py](src/model/BuildCalibrationTable.py)       | `calibration_ranges.tex` from `data/configuration_comparison/calibration.csv`.                                              |
| Tables A5, A7                 | [MeshConvergence.py](src/model/MeshConvergence.py)                   | `release_balance_table.tex` and `convergence_table.tex` from `data/transport_ensemble/mesh_convergence.csv`.              |
| Table A6                      | [BuildSamplingPriority.py](src/model/BuildSamplingPriority.py)       | `ensemble_table.tex`; also updates the retained sampling cells (see below).                                                   |
| Appendix G                    | [c.StabilityAnalysis.py](src/PathPlanning/c.StabilityAnalysis.py)    | CSV/JSON summaries in`data/sampling_plan/` and `sampling_stability_results.tex`.                                            |
| Table A10                     | [ClusterRadius.py](src/PathPlanning/ClusterRadius.py)                | `cluster_radius_sweep.csv` and `score_semivariogram.csv` in `data/sampling_plan/`.                                        |
| Appendix F throughput         | [BuildThroughputBenchmark.py](src/model/BuildThroughputBenchmark.py) | Prints a summary from`data/thermal_simulation/throughput/benchmark_runs.csv`.                                                 |

### Sampling plan

Regenerate the retained cells, clusters, route, and Figure 9 in this order. These
commands overwrite the corresponding files in `data/sampling_plan/`.

```sh
python src/model/BuildSamplingPriority.py --days 6 --cells 60
python src/PathPlanning/a.PointSelection.py
python src/PathPlanning/b.PathOptimization2.py
python src/figures/make_fig9.py
```

Then run the supplementary analyses, which use the retained cells and ensemble
data rather than each other's outputs:

```sh
python src/PathPlanning/c.StabilityAnalysis.py
python src/PathPlanning/ClusterRadius.py
```

### Temperature comparison

Rebuild the four validation CSVs from the included profiler records and redraw
Figures 5 and A3:

```sh
python src/model/ExportThermalProfiles.py --extract
python src/model/ExportThermalResiduals.py --extract
```

The pairing code is in [profiler_pairing.py](src/model/profiler_pairing.py).
Other scripts that extract from raw solver output require the external run archive,
located with `--runs-dir PATH` or the `D3DFM_RUNS` environment variable.

## Simulation software

The simulations used the Delft3D FM suite, developed and distributed by
[Deltares](https://oss.deltares.nl/web/delft3dfm):

| Component | Version                          | Used for                                                          |
| --------- | -------------------------------- | ----------------------------------------------------------------- |
| D-Flow FM | 1.2.177.142431 (26 January 2023) | Configuration comparison, scenario simulation, transport ensemble |
| D-Flow FM | 1.2.184 (13 June 2026)           | Thermal simulation                                                |
| DELWAQ    | 4.910                            | Water quality transport and reactions                             |

These products must be obtained separately through authorized distribution channels
and are covered by their own terms.

## Materials not published

- **Raw solver output:** map, history, and restart files total tens of gigabytes.
  The repository includes reduced datasets for reproducing the reported analyses.
- **Hydrodynamic coupling binaries:** volume, area, flow, pointer, length, and
  diffusivity files are omitted because of their size. The `FlowFM.hyd` manifests
  are included. Regenerating the binaries requires running D-Flow FM with the
  corresponding inputs: `data/scenario_simulation/flowfm/` for the scenario, and
  the runs identified by `data/transport_ensemble/config/` under
  `data/configuration_comparison/` for the transport cases.
  [ResolveCouplingPaths.py](src/model/ResolveCouplingPaths.py) replaces the
  `<COUPLING>` tokens in DELWAQ inputs with the regenerated coupling's path.
- **Delft3D FM and DELWAQ kernels:** obtain these separately as described above.
- **Lake-level and outflow records:** third-party monitoring records are not
  authorized for public distribution. Only the aggregate indicators quoted in
  the article are reported.

The included data support reproducing the analyses. Implementing the full framework, including running the simulations, requires compiled solvers in addition to the published model inputs and forcing listed above.

## Licence and citation

The code is licensed under [MIT](LICENSE), and the data under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Deltares products remain
subject to their own terms.

Please cite both the article and this repository; see [CITATION.cff](CITATION.cff).
