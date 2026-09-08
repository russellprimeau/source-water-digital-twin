"""
WAQHisPostProcess.py

Post-process Delft3D WAQ history output that has already been exported to CSV.
The script is intended for quick IDE-driven analysis of one configured
release/model directory, currently the SingleBlast/Eutroph nitrogen results.

Inputs
------
CSV files are read from ``CONFIG.input_directory``. Each active species and
observation point is expected to use the file name pattern
``{species}{observation_point}.csv``; for example, ``NH4Source.csv`` or
``NO3Spjelkavikelva.csv``. Each CSV must contain the timestamp column
``Time [yyyy.MM.dd HH:mm:ss]`` and exactly one concentration column unless an
expected concentration column is configured.

Processing
----------
For each species, the script reads all configured observation-point time
series, renames the concentration columns to display-location names, and merges
the series by timestamp with an outer join. This avoids assuming that files
have identical row order or identical timestamps. ``days_past`` is computed once
from the merged timestamp column. Max/min summaries are calculated only for
concentration columns, and cumulative Spjelkavikelva load is estimated with the
configured flow rate and cumulative periods.

Outputs
-------
For each species, the script writes a semilog concentration plot
(``{species}.png``), max/min summary CSVs (``max{species}.csv`` and
``min{species}.csv``), and a Spjelkavikelva cumulative-load table
(``sum{species}.csv``) under ``CONFIG.output_directory``. Figures are saved
before optional display via ``plt.show()``.

Known limitations
-----------------
The workflow remains a top-level exploratory script with manually edited
configuration. It assumes the first non-time column in each input file is the
concentration series and uses a simple fixed-flow load calculation.
"""

from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
NITROGEN_DIR = DATA_DIR / "Nitrogen"
TIME_COLUMN = "Time [yyyy.MM.dd HH:mm:ss]"


@dataclass(frozen=True)
class WAQHisConfig:
    """Editable run settings for the WAQ history post-processing workflow."""

    input_directory: Path = NITROGEN_DIR / "SingleBlast" / "Eutroph"
    output_directory: Path = NITROGEN_DIR / "SingleBlast" / "Eutroph" / "Analysis"
    species: tuple[str, ...] = ("NH4", "NO3")
    observation_points: tuple[str, ...] = (
        "Source",
        "Spjelkavikelva",
        "Vasstrandlia",
        "Profiler",
        "FarField",
    )
    display_points: dict[str, str] = field(
        default_factory=lambda: {
            "Source": "Blast Site",
            "Spjelkavikelva": "Spjelkavikelva",
            "Vasstrandlia": "Vasstrandlia Pump Intake",
            "Profiler": "Profiler",
            "FarField": "Nørebotnen",
        }
    )
    reference_date: pd.Timestamp | None = None
    show_plots: bool = True
    decimal: str = "."
    expected_concentration_columns: dict[str, str] = field(default_factory=dict)
    cumulative_location: str = "Spjelkavikelva"
    cumulative_periods: tuple[tuple[int, str], ...] = (
        (24, "1 day"),
        (168, "1 week"),
        (720, "1 month"),
        (2209, "3 months"),
    )
    spjelkavikelva_flow_lps: float = 180.0


CONFIG = WAQHisConfig()


# Lists of chemical species and observation points, used to loop through output CSV files from different model versions
# species = ["CnrvTrcr", "DcyTrcr", "SimpNH4", "SimpOxy", "EutrophNH4", "EutrophNO3", "EutrophOXY"]


def concentration_column(df: pd.DataFrame, path: Path, expected_column: str | None = None) -> str:
    """Return the single concentration column for an input CSV."""
    if TIME_COLUMN not in df.columns:
        raise ValueError(f"{path} is missing required time column {TIME_COLUMN!r}")

    if expected_column is not None:
        if expected_column not in df.columns:
            raise ValueError(f"{path} is missing expected concentration column {expected_column!r}")
        return expected_column

    candidates = [column for column in df.columns if column != TIME_COLUMN]
    if len(candidates) != 1:
        raise ValueError(
            f"{path} must contain exactly one non-time concentration column; "
            f"found {candidates!r}"
        )
    return candidates[0]


def _check_numeric(df, source_column, path):
    """Fail loudly if a concentration column did not parse as numbers.

    The WAQ export previously used '_' as the decimal separator, which pandas
    silently turns into NaN when reading with the default '.'.  Downstream that
    surfaces as a column of zeros rather than an error, so the condition is
    checked here instead of being discovered in a figure.
    """
    raw = df[source_column]
    values = pd.to_numeric(raw, errors="coerce")
    # A cell that is present but does not parse is the failure we care about:
    # reading '1_33E-05' with decimal='.' yields NaN, and any row that happens to
    # be a literal 0 still parses, so an "all NaN" test would miss it entirely.
    unparsed = values.isna() & raw.notna() & (raw.astype(str).str.strip() != "")
    if unparsed.any():
        sample = raw[unparsed].iloc[0]
        raise ValueError(
            f"{path}: column '{source_column}' has {int(unparsed.sum())} of {len(raw)} "
            f"values that did not parse as numbers (e.g. {sample!r}). "
            f"Check the decimal separator; CONFIG.decimal is currently {CONFIG.decimal!r}."
        )
    return values


def read_series(
    path: Path,
    output_column: str,
    expected_column: str | None = None,
) -> tuple[pd.DataFrame, str]:
    """Read one WAQ CSV and return timestamp plus one renamed concentration column."""
    df = pd.read_csv(path, parse_dates=[TIME_COLUMN], decimal=CONFIG.decimal)
    source_column = concentration_column(df, path, expected_column)
    _check_numeric(df, source_column, path)
    series_df = df[[TIME_COLUMN, source_column]].rename(columns={source_column: output_column})
    return series_df.sort_values(TIME_COLUMN), source_column


def add_days_past(df: pd.DataFrame, reference_date: pd.Timestamp | None) -> pd.DataFrame:
    """Insert days after the configured reference date or first merged timestamp."""
    reference = reference_date
    if reference is None:
        reference = df[TIME_COLUMN].min()
    df.insert(1, "days_past", (df[TIME_COLUMN] - reference).dt.total_seconds() / (24 * 3600))
    return df


def merge_species_series(spec: str) -> tuple[pd.DataFrame, list[str], str]:
    """Merge all configured observation-point series for one species by timestamp."""
    merged_df: pd.DataFrame | None = None
    concentration_columns: list[str] = []
    y_col = ""

    for point in CONFIG.observation_points:
        display_point = CONFIG.display_points.get(point, point)
        in_path = CONFIG.input_directory / f"{spec}{point}.csv"
        expected_column = CONFIG.expected_concentration_columns.get(spec)
        series_df, source_column = read_series(in_path, display_point, expected_column)
        concentration_columns.append(display_point)
        if not y_col:
            y_col = source_column

        if merged_df is None:
            merged_df = series_df
        else:
            merged_df = pd.merge(merged_df, series_df, on=TIME_COLUMN, how="outer")

    if merged_df is None:
        raise ValueError("No input series were configured")

    merged_df = merged_df.sort_values(TIME_COLUMN).reset_index(drop=True)
    merged_df = add_days_past(merged_df, CONFIG.reference_date)
    return merged_df, concentration_columns, y_col


def save_cumulative_load(spec: str, combined_df: pd.DataFrame) -> None:
    """Save cumulative Spjelkavikelva load estimates for configured periods."""
    location = CONFIG.display_points.get(CONFIG.cumulative_location, CONFIG.cumulative_location)
    if location not in combined_df.columns:
        return

    mass_g_per_hour = combined_df[location] * 3.6 * CONFIG.spjelkavikelva_flow_lps
    cumulative_df = pd.DataFrame(
        {
            "Timesteps": [period[0] for period in CONFIG.cumulative_periods],
            "Period": [period[1] for period in CONFIG.cumulative_periods],
            "Cumulative load, g": [0.0 for _ in CONFIG.cumulative_periods],
        }
    )
    for row_index, timesteps in enumerate(cumulative_df["Timesteps"]):
        cumulative_df.loc[row_index, "Cumulative load, g"] = mass_g_per_hour.iloc[:timesteps].sum()

    cumulative_df.to_csv(CONFIG.output_directory / f"sum{spec}.csv", index=False)


def save_plot(spec: str, combined_df: pd.DataFrame, concentration_columns: list[str], y_col: str) -> None:
    """Save one semilog concentration plot for a species."""
    plt.figure(figsize=(12, 6))
    plt.rcParams["font.size"] = 15
    for column in concentration_columns:
        plt.semilogy(combined_df["days_past"], combined_df[column], label=column)
    plt.xlabel("Days post-incident")
    plt.xticks(rotation=45)
    plt.ylabel("Concentration, " + y_col)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    plt.savefig(CONFIG.output_directory / f"{spec}.png")
    if CONFIG.show_plots:
        plt.show()
    plt.close()


def save_extrema(
    spec: str,
    combined_df: pd.DataFrame,
    concentration_columns: list[str],
) -> None:
    """Save max/min concentration values and timestamps for each observation point."""
    results = []
    for col in concentration_columns:
        max_value = combined_df[col].max()
        max_index = combined_df[col].idxmax()
        corresponding_datetime = combined_df.loc[max_index, TIME_COLUMN]
        results.append({"Column": col, "Max Value": max_value, "Datetime": corresponding_datetime})

    results_df = pd.DataFrame(results)
    results_df.to_csv(CONFIG.output_directory / f"max{spec}.csv", index=False)

    minresults = []
    for col in concentration_columns:
        min_value = combined_df[col].min()
        min_index = combined_df[col].idxmin()
        corresponding_datetime = combined_df.loc[min_index, TIME_COLUMN]
        minresults.append({"Column": col, "Min Value": min_value, "Time": corresponding_datetime})

    minresults_df = pd.DataFrame(minresults)
    minresults_df.to_csv(CONFIG.output_directory / f"min{spec}.csv", index=False)


def main() -> None:
    """Run the configured WAQ history post-processing workflow."""
    CONFIG.output_directory.mkdir(parents=True, exist_ok=True)

    for spec in CONFIG.species:
        combined_df, concentration_columns, y_col = merge_species_series(spec)
        save_cumulative_load(spec, combined_df)

        print(combined_df.head())

        save_plot(spec, combined_df, concentration_columns, y_col)
        save_extrema(spec, combined_df, concentration_columns)


if __name__ == "__main__":
    main()
