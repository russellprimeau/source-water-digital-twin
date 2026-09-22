# Model-configuration comparison

24 run records representing 21 distinct configurations, used in Figure 6 and
Table A3. Configuration settings are recorded in `calibration.csv` and the model
definitions.

| File or directory | Contents |
| --- | --- |
| `calibration.csv` | One row per run, with settings, comparison statistics, and computational cost. Semicolon-delimited. |
| `mdu/` | Resolved model definitions recorded by D-Flow FM at startup. |
| `input/` | Forcing and boundary conditions for this comparison. |
| `mesh/lowres_net.nc` | Coarse mesh reconstructed from solver output. |

These forcing files differ from the [thermal simulation inputs](../thermal_simulation/README.md)
and should be used with the comparison models.

From the repository root:

```sh
python src/model/CSVplotter.py
python src/model/BuildCalibrationTable.py
```

These commands write Figure 6 and the Table A3 fragment to `output/`.
[ExportConfigurationComparison.py](../../src/model/ExportConfigurationComparison.py)
regenerates the model definitions, coarse mesh, and this README with
`--extract --runs-dir PATH`. This requires the external solver archive; see
[Materials not published](../../README.md#materials-not-published).

## Model and mesh mapping

The resolved definitions all name their grid `flowfm_net.nc`. Use the mesh listed
for each run below:

- `fine`: `input/FlowFM_net.nc` (4,935 faces).
- `coarse`: `mesh/lowres_net.nc` (2,603 faces).

When preparing a run directory, set `NetFile` to the corresponding mesh path,
including the correct filename case on case-sensitive filesystems.

| Model definition | Label in calibration.csv | Mesh |
| --- | --- | --- |
| `2mnth_10_filtered_15s.mdu` | 10 Layer, Low Res, Filtered, Secchi Depth=0, 15s Max dt | coarse |
| `2mnth_10_filtered_Secc1.mdu` | 10 Layer, Filtered, Secchi Depth=1 | fine |
| `2mnth_10_filtered_secchi0.mdu` | 10 Layer, Low-Res Filtered, Secchi Depth=0 | coarse |
| `2mnth_10_unfiltered.mdu` | 10 Layer, Unfiltered, Secchi Depth=7 | fine |
| `2mnth_20_filtered.mdu` | 20 Layer, Filtered, Secchi Depth=7 | fine |
| `2mnth_20_filtered_secchi1_lowres.mdu` | 20 Layer, Low Res, Filtered, Secchi Depth=1 | coarse |
| `2mnth_20_unfiltered.mdu` | 20 Layer, Unfiltered, Secchi Depth=7 | fine |
| `2mnth_40_Low_Secc0.mdu` | 40 Layer, Low Res, Filtered, Secchi Depth=0 | coarse |
| `2mnth_40_Secchi1_Courant4.mdu` | 40 Layer, Filtered, Secchi Depth=1, Courant=0.4 | fine |
| `2mnth_40_filtered.mdu` | 40 Layer, Filtered, Secchi Depth=7 | fine |
| `2mnth_40_filtered_2Secchi.mdu` | 40 Layer, Filtered, Secchi Depth=2 | fine |
| `2mnth_40_filtered_secchi1.mdu` | 40 Layer, Filtered, Secchi Depth=1 | fine |
| `2mnth_40_unfiltered.mdu` | 40 Layer, Unfiltered, Secchi Depth=7 | fine |
| `7mnth_20Low.mdu` | 20 Layer Low Res | coarse |
| `7mnth_20_highres_filtered.mdu` | 20 Layer Full Season High Res | fine |
| `7mnth_20_lowres_contam.mdu` | 20 Layer Full Season Low Res | coarse |
| `7mnth_40High_Dico4.mdu` | 40 Layer High Res Dicoww4 | fine |
| `7mnth_40High_VicDic5.mdu` | 40 Layer High Res VicoDicoww5 | fine |
| `7mnth_40_highresDic.mdu` | 40 Layer High Res Dicoww3 | fine |
| `7mnth_40_highresVicDic.mdu` | 40 Layer High Res VicoDicoww3 | fine |
| `7mnth_40_highres_contam.mdu` | 40 Layer Full Season High Res | fine |
| `7mnth_40_highres_novfilt.mdu` | 40 Layer Full Season High Res noVfilter | fine |
| `7mnth_40_low_filtered.mdu` | 40 Layer Full Season Low Res | coarse |
| `7mnth_40high_Vico6Dico5.mdu` | 40high_Vico6Dico5 | fine |
