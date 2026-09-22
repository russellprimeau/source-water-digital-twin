# Transport ensemble and refinement study

Conservative-tracer inputs and reduced outputs for seven candidate configurations
and four mesh/layer refinement cases. The archived ensemble contains five members
and supplies the sampling-plan scores for Figure 9a. The refinement cases cross
two horizontal meshes with two vertical resolutions.

| File or directory | Contents |
| --- | --- |
| `ensemble/spread_by_horizon.nc` | Per-cell model-spread scores and ensemble means at each saved output time. |
| `ensemble/tracer_members.nc` | Layered tracer fields for each ensemble member at one saved time (140 hours after release), used for member-subset calculations. |
| `input/` | Eleven DELWAQ input sets: seven candidates and four refinement cases. |
| `config/` | Generator configurations, including source hydrodynamic run identifiers. `<RUNNER>` denotes the unpublished model-running repository. |
| `coupling/` | `FlowFM.hyd` and `FlowFM.bnd` per run, recording the coupling and counts required for regeneration. |
| `geometry/` | One mesh file per discretization. |
| `mesh_convergence.csv` | Refinement statistics used for Tables A5 and A7. |

[BuildSamplingPriority.py](../../src/model/BuildSamplingPriority.py) reads the
ensemble files and `data/configuration_comparison/calibration.csv`. Use the
[sampling commands](../../README.md#sampling-plan) to reproduce the published plan.
Horizon requests select the nearest saved output; member-subset checks are
available only at the archived member time.

Generate the refinement tables from the repository root:

```sh
python src/model/MeshConvergence.py
```

The coupling binaries are not included. Each run's configuration identifies its
hydrodynamic inputs under [configuration_comparison](../configuration_comparison/README.md).
Regenerate the coupling with D-Flow FM and use
[ResolveCouplingPaths.py](../../src/model/ResolveCouplingPaths.py) to replace
`<COUPLING>` in the DELWAQ inputs. See the repository's
[availability statement](../../README.md#materials-not-published).
