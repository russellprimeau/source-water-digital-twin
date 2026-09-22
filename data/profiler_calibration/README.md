# Profiler calibration

Calibration records and surface-sonde operating hours used in Figure 10.

| File | Contents |
| --- | --- |
| `calibration_events.csv` | One row per calibration point, with reference values and readings before and after adjustment. |
| `surface_uptime_hours.csv` | One timestamp per hour of surface-sonde logging. |

## Calibration columns

Group points by `parameter` and `event`. Each event contains one to three points;
different events can share an end time.

| Column | Meaning |
| --- | --- |
| `parameter` | Sensor parameter and unit: DO (% Sat), Sp Cond (µS/cm), Turbidity (FNU), fDOM (QSU), fDOM (RFU), or pH. |
| `event` | Calibration event number within each parameter. |
| `calibration_end_time` | Time the calibration ended. |
| `point` | Point number (1, 2, or 3) within the event. |
| `standard` | Reference value, in the parameter's units. |
| `pre_calibration_value` | Reading before adjustment. |
| `post_calibration_value` | Reading after adjustment. |

From the repository root, generate Figure 10 from these two files:

```sh
python src/figures/make_fig10.py
```
