# Thermal simulation

Model inputs and profiler comparison data for Section 3.1, Table 3, Figure 5,
Figures A2–A3, and Table A4.

| File or directory | Contents |
| --- | --- |
| `input/` | D-Flow FM configuration and forcing. `FlowFMnew.mdu` uses `fixed_net.nc`; partitioned copies for the twelve solver processes are not included. |
| `profiler/Profiler_Step.csv` | Profiler instrument log, June 2020 to November 2024. |
| `profiler/model_profile.nc` | Modelled temperature at the profiler, with nominal and time-varying layer depths. Reduced from the unpublished solver history file. |
| `validation/temperature_profiles_2024.csv` | Modelled and observed temperatures paired by time and depth in fifty one-metre bands. |
| `validation/temperature_profile_gaps_2024.csv` | Observation gaps shaded in the figures. |
| `validation/temperature_by_depth_2024.csv` | Per-depth error statistics supporting Table A4. |
| `validation/temperature_residuals_2024.csv` | Temperature residuals for Figure A3 (`Fig14.png`). |
| `throughput/benchmark_runs.csv` | Run settings and timings used for the Appendix F throughput summary. |

The forcing in `input/` belongs to this simulation; the
[configuration comparison](../configuration_comparison/README.md) has separate inputs.

## Reproducing the comparison

From the repository root, rebuild the four validation CSVs from `profiler/` and
draw Figures 5 and A3:

```sh
python src/model/ExportThermalProfiles.py --extract
python src/model/ExportThermalResiduals.py --extract
```

Omit `--extract` to plot the existing validation records. The pairing code is in
[profiler_pairing.py](../../src/model/profiler_pairing.py).

```sh
python src/figures/make_fig11_13.py
python src/model/BuildThroughputBenchmark.py
```

The first command writes `Fig11.png`–`Fig13.png`, the source images for Figure A2.
The second prints the throughput summary. Figure images go to `output/`.
Table A4 is supported by the statistics CSV; these commands do not generate its LaTeX.

## Instrument log columns

`Profiler_Step.csv` contains one row per reading. The temperature comparison uses
`TIMESTAMP`, `sensorParms(1)`, and `sensorParms(9)`.

| Column | Quantity | Unit |
| --- | --- | --- |
| `TIMESTAMP` | time of the reading | ISO 8601 |
| `sensorParms(1)` | water temperature | degC |
| `sensorParms(2)` | conductivity | uS/cm |
| `sensorParms(3)` | specific conductivity | uS/cm |
| `sensorParms(4)` | salinity | ppt |
| `sensorParms(5)` | pH | |
| `sensorParms(6)` | dissolved oxygen | % saturation |
| `sensorParms(7)` | turbidity | NTU |
| `sensorParms(8)` | turbidity | FNU |
| `sensorParms(9)` | vertical position | m below the surface |
| `sensorParms(10)` | fDOM | RFU |
| `sensorParms(11)` | fDOM | QSU |

`RECORD`, `PFL_Counter`, `CntRS232`, and `RS232Dpt` are datalogger bookkeeping fields.
