"""
NewWAQPlots.py

Create combined plots from Delft3D WAQ history output that has already been
exported to CSV. The script is intended for quick IDE-driven comparisons across
configured releases, models, species, and observation points while preserving a
MultiIndex dataframe that can be filtered for alternative plot layouts.

Inputs
------
Model output CSV files are expected under ``CONFIG.input_directory`` using the
``{release}/{model}`` directory structure. Eutroph and Simp model files use the
``{species}{observation_point}.csv`` naming convention, such as
``NH4Source.csv``. CnrvTrcr and DcyTrcr files use ``{observation_point}.csv``.
Each CSV must contain ``Time [yyyy.MM.dd HH:mm:ss]`` and exactly one
concentration column unless an expected column is configured.

Processing
----------
Each CSV is normalized to timestamp plus one named concentration series. The
series are outer-merged on timestamp, sorted, and assigned a shared
``days_past`` value from ``CONFIG.reference_date``. This avoids assuming the
files have identical row order or identical timestamps. The resulting
``combined_df`` keeps the previous four-level MultiIndex column structure:
release, model, species, and location. ``index1`` and ``index2`` pseudo-levels
hold the timestamp and ``days_past`` columns.

Outputs
-------
The active plotting block writes ``combined.png`` and ``combined_columns.csv``
to ``CONFIG.output_directory``. Ground-truth NH4/NO3 files are read and given
``days_past`` columns, but the active plot does not include them unless the
commented plotting lines are restored.

Known limitations
-----------------
This remains a top-level exploratory plotting script with manually edited
configuration. Several imports and commented plotting sections are retained
because they are useful for alternate plot variants.
"""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

try:
    from cartopy.mpl.clip_path import bbox_to_path
except ModuleNotFoundError:
    bbox_to_path = None

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
NITROGEN_DIR = DATA_DIR / "Nitrogen"
TIME_COLUMN = "Time [yyyy.MM.dd HH:mm:ss]"


@dataclass(frozen=True)
class WAQPlotConfig:
    """Editable run settings for combined WAQ plotting."""

    input_directory: Path = NITROGEN_DIR
    output_directory: Path = NITROGEN_DIR
    releases: tuple[str, ...] = ("SingleBlast",)
    models: tuple[str, ...] = ("Eutroph",)
    species_by_release_model: dict[tuple[str, str], tuple[str, ...]] = field(
        default_factory=lambda: {
            ("SingleBlast", "CnrvTrcr"): ("CnrvTrcr",),
            ("SingleBlast", "DcyTrcr"): ("DcyTrcr",),
            ("SingleBlast", "Eutroph"): ("NH4", "NO3"),
            ("SingleBlast", "Simp"): ("NH4",),
            ("MultipleBlasts", "Eutroph"): ("NH4", "NO3"),
        }
    )
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
    reference_date: pd.Timestamp = pd.Timestamp("2024-08-01 00:00:00")
    show_plots: bool = False
    decimal: str = "_"
    expected_concentration_columns: dict[tuple[str, str, str], str] = field(default_factory=dict)
    no3_plot_species: tuple[str, ...] = ("NO3",)
    nh4_plot_species: tuple[str, ...] = ("NH4",)
    cumulative_periods: tuple[tuple[int, str], ...] = (
        (24, "1 day"),
        (168, "1 week"),
        (720, "1 month"),
        (2209, "3 months"),
    )
    spjelkavikelva_flow_lps: float = 180.0


CONFIG = WAQPlotConfig()

# Plot ALL data:
# releases = ["SingleBlast", "MultipleBlasts"]
releases = list(CONFIG.releases)
# releases = ["MultipleBlasts"]
# models = ["CnrvTrcr", "DcyTrcr", "Eutroph", "Simp"]

# Plot selected data:
# releases = ["SingleBlast"]
models = list(CONFIG.models)
# models = ["Multiconsult"]
# ObsPt= ["Source"]

ObsPt = list(CONFIG.observation_points)
# ObsPt= ["Source"]
DisplayPt = CONFIG.display_points
input_directory = CONFIG.input_directory
output_directory = CONFIG.output_directory

# Model output CSV files are expected under DATA_DIR/Nitrogen using the old
# release/model directory structure.

# Full list of chemical species and observation points:
allspecies = ["CnrvTrcr", "DcyTrcr", "SimpNH4", "SimpOxy", "EutrophNH4", "EutrophNO3", "EutrophOXY"]


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


def input_file_name(model: str, spec: str, point: str) -> str:
    """Return the configured WAQ CSV filename for a model/species/point."""
    if model in ["CnrvTrcr", "DcyTrcr"]:
        return f"{point}.csv"
    return f"{spec}{point}.csv"


def read_series(
    path: Path,
    output_column: tuple[str, str, str, str],
    expected_column: str | None = None,
) -> pd.DataFrame:
    """Read one WAQ CSV and return timestamp plus one MultiIndex-ready value column."""
    df = pd.read_csv(path, parse_dates=[TIME_COLUMN], header=0, decimal=CONFIG.decimal)
    source_column = concentration_column(df, path, expected_column)
    series_df = df[[TIME_COLUMN, source_column]].rename(columns={source_column: output_column})
    return series_df.sort_values(TIME_COLUMN)


def build_combined_dataframe() -> pd.DataFrame:
    """Read configured model outputs and merge all series by timestamp."""
    merged_df: pd.DataFrame | None = None
    value_columns: list[tuple[str, str, str, str]] = []

    for release in releases:
        for model in models:
            model_directory = CONFIG.input_directory / release / model
            species = CONFIG.species_by_release_model.get((release, model), ())
            for spec in species:
                for point in ObsPt:
                    display_point = DisplayPt.get(point, point)
                    column_key = (release, model, spec, display_point)
                    expected_column = CONFIG.expected_concentration_columns.get((release, model, spec))
                    in_path = model_directory / input_file_name(model, spec, point)
                    series_df = read_series(in_path, column_key, expected_column)
                    value_columns.append(column_key)

                    if merged_df is None:
                        merged_df = series_df
                    else:
                        merged_df = pd.merge(merged_df, series_df, on=TIME_COLUMN, how="outer")

                    if spec == "NH4":
                        merged_df[column_key] = merged_df[column_key]  # + 0.011
                        print(merged_df)
                    if spec == "NO3":
                        merged_df[column_key] = merged_df[column_key]  # + 0.11
                        print(merged_df)

                    # if spec == 'EutrophNH4':
                    #     df.iloc[:,1] *= 1287  # Convert concentration values from gN/m3 to ug NH4/L
                    #     df.rename(columns={df.columns[1]: 'NH4 [ug/L]'}, inplace=True)
                    #     print(df)
                    # elif spec == 'EutrophNO3':
                    #     df.iloc[:,1] *= 4427  # Convert concentration values from gN/m3 to ug NO3/L
                    #     df.rename(columns={df.columns[1]: 'NO3 [ug/L]'}, inplace=True)
                    # if l == 0:
                    #     y_col = df.columns[1]
                    #     df = df.rename(columns={y_col:pt})
                    #     combined_df = df
                    # else:
                    #     df = df.rename(columns={y_col:pt})
                    #     combined_df = pd.concat([combined_df, df.iloc[:,1]], axis=1)
                    #     # Calculate cumulative load for Spjelkavikelva, to feed Lillevatnet analysis
                    #     if pt == "Spjelkavikelva":
                    #         df["Mass"] = df["Spjelkavikelva"]*3.6*180 # Calculate g/hr as g/m3 * 3.6 s*m3/l*hr * 180 l/s
                    #         cumulative = {'Timesteps':[24, 168, 720, 2209], 'Period':['1 day', '1 week', '1 month', '3 months'],
                    #                       'Cumulative load, g':[0.5,0.5,0.5,0.5]}
                    #         cumulativeN = pd.DataFrame(data=cumulative)
                    #         for i in range(len(cumulativeN['Timesteps'])):
                    #             cumulativeN.iloc[i,2] = df['Mass'].iloc[:cumulativeN.iloc[i,0]].sum()
                    #         sumfilename = 'sum' + spec + '.csv'
                    #         sumout_path = output_directory / sumfilename
                    #         cumulativeN.to_csv(sumout_path, index=False)

    if merged_df is None:
        raise ValueError("No release/model/species combinations were configured")

    merged_df = merged_df.sort_values(TIME_COLUMN).reset_index(drop=True)
    days_past = (merged_df[TIME_COLUMN] - CONFIG.reference_date).dt.total_seconds() / (24 * 3600)

    combined = pd.DataFrame()
    combined[("index1", "index1", "index1", TIME_COLUMN)] = merged_df[TIME_COLUMN]
    combined[("index2", "index2", "index2", "days_past")] = days_past
    for column_key in value_columns:
        combined[column_key] = merged_df[column_key]

    combined.columns = pd.MultiIndex.from_tuples(combined.columns)
    combined.columns.names = ["release", "model", "species", "location"]
    return combined


def read_groundtruth(spec: str) -> pd.DataFrame:
    """Read a ground-truth CSV and calculate days after the configured reference date."""
    groundtruth = pd.read_csv(
        NITROGEN_DIR / "GroundTruth" / f"{spec}.csv",
        parse_dates=[TIME_COLUMN],
        sep=",",
        header=0,
        decimal=".",
    )
    groundtruth.insert(
        1,
        "days_past",
        (groundtruth[TIME_COLUMN] - CONFIG.reference_date).dt.total_seconds() / (24 * 3600),
    )
    return groundtruth


def main() -> None:
    """Run the configured combined WAQ plotting workflow."""
    CONFIG.output_directory.mkdir(parents=True, exist_ok=True)
    combined_df = build_combined_dataframe()

    groundtruthNO3 = read_groundtruth("NO3")
    groundtruthNH4 = read_groundtruth("NH4")

    # Plotting
    plt.figure(figsize=(13, 6))
    plt.rcParams["font.size"] = 16

    # plt.semilogy(groundtruthNO3['days_past'], groundtruthNO3['NO3 [gN/m3]'], 'bo', label='Measured NO3, [gN/m3]')
    # plt.semilogy(groundtruthNH4['days_past'], groundtruthNH4['NH4 [gN/m3]'], 'r+', label='Measured NH4, [gN/m3]')

    # NO3species = ["CnrvTrcr", "DcyTrcr", "NO3"]
    # NH4species = ["NH4"]

    NO3species = list(CONFIG.no3_plot_species)
    NH4species = list(CONFIG.nh4_plot_species)

    NO3_cols = combined_df.loc[:, (combined_df.columns.get_level_values("release").isin(releases)) &
                                 (combined_df.columns.get_level_values("model").isin(models)) &
                                 (combined_df.columns.get_level_values("species").isin(NO3species))]

    NH4_cols = combined_df.loc[:, (combined_df.columns.get_level_values("release").isin(releases)) &
                                 (combined_df.columns.get_level_values("model").isin(models)) &
                                 (combined_df.columns.get_level_values("species").isin(NH4species))]

    num_cols = NH4_cols.shape[1]
    print("num_cols", num_cols)
    jet = cm = plt.get_cmap("jet")
    cNorm = colors.Normalize(vmin=0, vmax=num_cols)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    # 'label' must be last argument
    # label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}

    for m, column in enumerate(NO3_cols):
        print(m, scalarMap.to_rgba(m))
        plt.semilogy(combined_df[("index2", "index2", "index2", "days_past")], combined_df[column], color=scalarMap.to_rgba(m),
                     label=f"{column[3]}, {column[2]}")

    for n, column in enumerate(NH4_cols):
        print(n, scalarMap.to_rgba(n))
        plt.semilogy(combined_df[("index2", "index2", "index2", "days_past")], combined_df[column], "--",
                     color=scalarMap.to_rgba(n), label=f"{column[3]}, {column[2]}")

    plt.xlabel("Days post-incident")
    # plt.xlim(-75,95)
    # plt.xticks(rotation=45)
    plt.ylabel("Concentration (gN/m3)")
    plt.grid()
    plt.legend(bbox_to_anchor=(0.5, 1), loc="lower center", markerscale=1, ncols=2, fontsize=16)
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=3)
    plt.tight_layout()

    # # Individual plots for each NO3
    # ############################################################################################
    #
    # # plt.semilogy(groundtruthNO3['days_past'], groundtruthNO3['NO3 [gN/m3]'], 'bo', label='Measured NO3, [gN/m3]')
    # # plt.semilogy(groundtruthNH4['days_past'], groundtruthNH4['NH4 [gN/m3]'], 'r+', label='Measured NH4, [gN/m3]')
    #
    # # NO3species = ["CnrvTrcr", "DcyTrcr", "NO3"]
    # # NH4species = ["NH4"]
    #
    # NO3species = ["NO3"]
    # NH4species = ["NH4"]
    #
    # NO3_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
    #                              (combined_df.columns.get_level_values('model').isin(models)) &
    #                              (combined_df.columns.get_level_values('species').isin(NO3species))]
    #
    # NH4_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
    #                              (combined_df.columns.get_level_values('model').isin(models)) &
    #                              (combined_df.columns.get_level_values('species').isin(NH4species))]
    #
    # num_cols = NH4_cols.shape[1]
    # print('num_cols', num_cols)
    # jet = cm = plt.get_cmap('jet')
    # cNorm  = colors.Normalize(vmin=0, vmax=num_cols)
    # scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    #
    # # 'label' must be last argument
    # # label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}
    #
    # for m, column in enumerate(NO3_cols):
    #     print(m, scalarMap.to_rgba(m))
    #     plt.semilogy(combined_df[('index2', 'index2', 'index2', 'days_past')], combined_df[column], color=scalarMap.to_rgba(m),
    #                  label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}')
    #
    # #     full label: label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}'
    #
    # for n, column in enumerate (NH4_cols):
    #     print(n, scalarMap.to_rgba(n))
    #     plt.semilogy(combined_df[('index2', 'index2', 'index2', 'days_past')], combined_df[column], '--',
    #                  color=scalarMap.to_rgba(n), label = f'{column[3]}')
    #
    # plt.xlabel('Days post-incident')
    # plt.xlim(-75,95)
    # # plt.xticks(rotation=45)
    # plt.ylabel('Concentration (g/m3)')
    # plt.grid()
    # plt.legend(loc='upper left')
    # # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=3)
    # plt.tight_layout()

    # Individual plots for NH4
    ############################################################################################

    # To view the figure:
    # plt.show()

    outfilename = "combined" + ".png"
    out_path = output_directory / outfilename

    plt.savefig(out_path, dpi=600)
    combined_df.to_csv(output_directory / "combined_columns.csv")

    if CONFIG.show_plots:
        plt.show()
    plt.close()

    # # Save out a table of showing the time at which the maximum value occurs for each observation point
    # results = []
    # for col in combined_df.columns[1:]:
    #     max_value = combined_df[col].max()
    #     max_index = combined_df[col].idxmax()
    #     corresponding_datetime = combined_df.loc[max_index, 'Time [yyyy.MM.dd HH:mm:ss]']
    #     results.append({'Column': col, 'Max Value': max_value, 'Datetime': corresponding_datetime})
    #
    # # Convert the results to a DataFrame and save
    # results_df = pd.DataFrame(results)
    # maxfilename = 'max' + spec + '.csv'
    # maxout_path = output_directory / maxfilename
    # results_df.to_csv(maxout_path, index=False)
    #
    # # Save out a table showing the time at which the minimum value occurs for each observation point
    # minresults = []
    # for col in combined_df.columns[1:]:
    #     min_value = combined_df[col].min()
    #     min_index = combined_df[col].idxmin()
    #     corresponding_datetime = combined_df.loc[min_index, 'Time [yyyy.MM.dd HH:mm:ss]']
    #     minresults.append({'Column': col, 'Min Value': min_value, 'Time': corresponding_datetime})
    #
    # # Convert the results to a DataFrame and save
    # minresults_df = pd.DataFrame(minresults)
    # minfilename = 'min' + spec + '.csv'
    # minout_path = output_directory / minfilename
    # minresults_df.to_csv(minout_path, index=False)


if __name__ == "__main__":
    main()
