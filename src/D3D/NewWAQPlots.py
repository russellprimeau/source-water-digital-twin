"""
NewWAQPlots.py

Plot data from Deflt3D WAQ simulation output written to a CSV file (to avoid needing to develop code for reading WAQ-style HIS NetCDF file)

Inputs:
- CSV files containing time series data for each chemical species and observation point, with columns for time and concentration values.
The file naming convention is assumed to be: [species][observation_point].csv (e.g., "NH4Source.csv", "NO3Spjelkavikelva.csv", etc.)

Outputs:
- A combined plot showing the time series of each chemical species at each observation point.
Different colors and line styles for each model and release scenario.
The x-axis represents time (in days post-incident), and the y-axis represents concentration (in gN/m3).
A legend is included to differentiate between the different lines.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data' / 'Nitrogen'
OUTPUT_DIR = ROOT_DIR / 'build'

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REFERENCE_DATE = pd.Timestamp('2024-08-01 00:00:00')

DISPLAY_PT = {
    "Source":        "Blast Site",
    "Spjelkavikelva":"Spjelkavikelva",
    "Vasstrandlia":  "Vasstrandlia Pump Intake",
    "Profiler":      "Profiler",
    "FarField":      "Nørebotnen",
}

allspecies = ["CnrvTrcr", "DcyTrcr", "SimpNH4", "SimpOxy", "EutrophNH4", "EutrophNO3", "EutrophOXY"]

# Species per release/model combination.
# Using 'EutrophNH4'/'EutrophNO3' instead of 'NH4'/'NO3' activates unit conversion (gN/m3 → ug/L).
MODEL_SPECIES = {
    'SingleBlast': {
        'CnrvTrcr': ['CnrvTrcr'],
        'DcyTrcr':  ['DcyTrcr'],
        'Eutroph':  ['NH4', 'NO3'],         # or ['EutrophNH4', 'EutrophNO3'] for ug/L output
        'Simp':     ['NH4'],                # or ['NH4', 'Oxy']
    },
    'MultipleBlasts': {
        'Eutroph':  ['NH4', 'NO3'],         # or ['NH4', 'NO3', 'OXY']
    },
}

CONFIGS = {
    'eutroph_single': {
        'releases':   ['SingleBlast'],
        'models':     ['Eutroph'],
        'obs_points': ['Source', 'Spjelkavikelva', 'Vasstrandlia', 'Profiler', 'FarField'],
    },
    'all_models_single': {
        'releases':   ['SingleBlast'],
        'models':     ['CnrvTrcr', 'DcyTrcr', 'Eutroph', 'Simp'],
        'obs_points': ['Source', 'Spjelkavikelva', 'Vasstrandlia', 'Profiler', 'FarField'],
    },
    'eutroph_multi': {
        'releases':   ['MultipleBlasts'],
        'models':     ['Eutroph'],
        'obs_points': ['Source', 'Spjelkavikelva', 'Vasstrandlia', 'Profiler', 'FarField'],
    },
    'source_only': {
        'releases':   ['SingleBlast'],
        'models':     ['Eutroph'],
        'obs_points': ['Source'],
    },
}

ACTIVE_CONFIG = 'eutroph_single'  # ← only line to change when switching scenarios

releases = CONFIGS[ACTIVE_CONFIG]['releases']
models   = CONFIGS[ACTIVE_CONFIG]['models']
ObsPt    = CONFIGS[ACTIVE_CONFIG]['obs_points']

output_directory = DATA_DIR


def input_path(release, model, species, obs_point):
    # CnrvTrcr and DcyTrcr output files are named [obs_point].csv (no species prefix);
    # multi-species models (Eutroph, Simp) use [species][obs_point].csv.
    prefix = '' if species == model else species
    return DATA_DIR / release / model / f'{prefix}{obs_point}.csv'


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

# Model output CSV files are expected under DATA_DIR/{release}/{model}/ using the naming
# convention [species][observation_point].csv, such as NH4Source.csv.

combined_df = pd.DataFrame()
days_past = None
datetime_index = None

for release in releases:
    for model in models:
        species = MODEL_SPECIES[release][model]
        for spec in species:
            for pt in ObsPt:
                in_path = input_path(release, model, spec, pt)
                display_pt = DISPLAY_PT.get(pt, pt)

                df = pd.read_csv(in_path, parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'], header=0, decimal='_')

                if days_past is None:
                    datetime_index = df.iloc[:, 0]
                    days_past = (df.iloc[:, 0] - REFERENCE_DATE).dt.total_seconds() / (24 * 3600)

                combined_df[(release, model, spec, display_pt)] = df.iloc[:, 1]

                if spec == 'EutrophNH4':
                    combined_df[(release, model, spec, display_pt)] *= 1287  # gN/m3 → ug NH4/L
                elif spec == 'EutrophNO3':
                    combined_df[(release, model, spec, display_pt)] *= 4427  # gN/m3 → ug NO3/L

                if pt == "Spjelkavikelva":
                    mass = combined_df[(release, model, spec, display_pt)] * 3.6 * 180  # g/m3 * 3.6 s*m3/L*hr * 180 L/s → g/hr
                    timesteps = [24, 168, 720, 2209]
                    periods = ['1 day', '1 week', '1 month', '3 months']
                    cumulative_loads = [mass.iloc[:n].sum() for n in timesteps]
                    cumulativeN = pd.DataFrame({'Timesteps': timesteps, 'Period': periods, 'Cumulative load, g': cumulative_loads})
                    cumulativeN.to_csv(output_directory / f'sum{spec}{release}{model}.csv', index=False)

combined_df.columns = pd.MultiIndex.from_tuples(combined_df.columns)
combined_df.columns.names = ['release', 'model', 'species', 'location']

groundtruthNO3 = pd.read_csv(DATA_DIR / 'GroundTruth' / 'NO3.csv',
                          parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'], sep=',', header=0, decimal='.')
groundtruthNO3.insert(1, 'days_past',
                   (groundtruthNO3['Time [yyyy.MM.dd HH:mm:ss]'] - REFERENCE_DATE).dt.total_seconds() / (24 * 3600))

groundtruthNH4 = pd.read_csv(DATA_DIR / 'GroundTruth' / 'NH4.csv',
                          parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'], sep=',', header=0, decimal='.')
groundtruthNH4.insert(1, 'days_past',
                   (groundtruthNH4['Time [yyyy.MM.dd HH:mm:ss]'] - REFERENCE_DATE).dt.total_seconds() / (24 * 3600))

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

NO3species = ["NO3"]
NH4species = ["NH4"]

NO3_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
                             (combined_df.columns.get_level_values('model').isin(models)) &
                             (combined_df.columns.get_level_values('species').isin(NO3species))]

NH4_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
                             (combined_df.columns.get_level_values('model').isin(models)) &
                             (combined_df.columns.get_level_values('species').isin(NH4species))]

num_cols = NH4_cols.shape[1]
print('num_cols', num_cols)
jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=num_cols)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

# Figure 1: Model output only
plt.figure(figsize=(13, 6))
plt.rcParams['font.size'] = 16

for m, column in enumerate(NO3_cols):
    print(m, scalarMap.to_rgba(m))
    plt.semilogy(days_past, combined_df[column], color=scalarMap.to_rgba(m),
                 label=f'{column[3]}, {column[2]}')

for n, column in enumerate(NH4_cols):
    print(n, scalarMap.to_rgba(n))
    plt.semilogy(days_past, combined_df[column], '--',
                 color=scalarMap.to_rgba(n), label=f'{column[3]}, {column[2]}')

plt.xlabel('Days post-incident')
plt.ylabel('Concentration (gN/m3)')
plt.grid()
plt.legend(bbox_to_anchor=(0.5, 1), loc='lower center', markerscale=1, ncols=2, fontsize=16)
plt.tight_layout()
plt.savefig(output_directory / 'combined_model_only.png', dpi=600)
plt.close()

# Figure 2: Model output with measured data overlay
plt.figure(figsize=(13, 6))
plt.rcParams['font.size'] = 16

plt.semilogy(groundtruthNO3['days_past'], groundtruthNO3['NO3 [gN/m3]'], 'bo', label='Measured NO3, [gN/m3]')
plt.semilogy(groundtruthNH4['days_past'], groundtruthNH4['NH4 [gN/m3]'], 'r+', label='Measured NH4, [gN/m3]')

NO3species = ["NO3"]
NH4species = ["NH4"]

NO3_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
                             (combined_df.columns.get_level_values('model').isin(models)) &
                             (combined_df.columns.get_level_values('species').isin(NO3species))]

NH4_cols = combined_df.loc[:, (combined_df.columns.get_level_values('release').isin(releases)) &
                             (combined_df.columns.get_level_values('model').isin(models)) &
                             (combined_df.columns.get_level_values('species').isin(NH4species))]

num_cols = NH4_cols.shape[1]
print('num_cols', num_cols)
jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=num_cols)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

for m, column in enumerate(NO3_cols):
    print(m, scalarMap.to_rgba(m))
    plt.semilogy(days_past, combined_df[column], color=scalarMap.to_rgba(m),
                 label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}')

for n, column in enumerate(NH4_cols):
    print(n, scalarMap.to_rgba(n))
    plt.semilogy(days_past, combined_df[column], '--',
                 color=scalarMap.to_rgba(n), label=f'{column[3]}')

plt.xlabel('Days post-incident')
plt.xlim(-75, 95)
plt.ylabel('Concentration (g/m3)')
plt.grid()
plt.legend(loc='upper left')
plt.tight_layout()

outfilename = 'combined' + '.png'
out_path = output_directory / outfilename

plt.savefig(out_path, dpi=600)
combined_df.to_csv(DATA_DIR / 'combined_columns.csv')

plt.close()

# Per-species PNG outputs (one figure per species, all models/releases/locations)
for spec_name in combined_df.columns.get_level_values('species').unique():
    spec_cols = combined_df.loc[:, combined_df.columns.get_level_values('species') == spec_name]
    plt.figure(figsize=(12, 6))
    plt.rcParams['font.size'] = 15
    for column in spec_cols.columns:
        label = f'{column[0]}_{column[1]}_{column[3]}'
        plt.semilogy(days_past, combined_df[column], label=label)
    plt.xlabel('Days post-incident')
    plt.ylabel(f'Concentration, {spec_name} (gN/m3)')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_directory / f'{spec_name}.png')
    plt.close()

# Save out a table of showing the time at which the maximum value occurs for each observation point
results = []
for col in combined_df.columns:
    max_value = combined_df[col].max()
    max_index = combined_df[col].idxmax()
    corresponding_datetime = datetime_index.iloc[max_index]
    results.append({'Column': col, 'Max Value': max_value, 'Datetime': corresponding_datetime})

results_df = pd.DataFrame(results)
maxfilename = 'max' + spec + '.csv'
maxout_path = output_directory / maxfilename
results_df.to_csv(maxout_path, index=False)

# Save out a table showing the time at which the minimum value occurs for each observation point
minresults = []
for col in combined_df.columns:
    min_value = combined_df[col].min()
    min_index = combined_df[col].idxmin()
    corresponding_datetime = datetime_index.iloc[min_index]
    minresults.append({'Column': col, 'Min Value': min_value, 'Time': corresponding_datetime})

minresults_df = pd.DataFrame(minresults)
minfilename = 'min' + spec + '.csv'
minout_path = output_directory / minfilename
minresults_df.to_csv(minout_path, index=False)
