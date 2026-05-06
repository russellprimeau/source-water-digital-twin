# Plot data from Deflt3D WAQ simulation output written to a CSV file (to avoid needing to develop code for reading
# WAQ-style HIS NetCDF file).csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pathlib import Path

from cartopy.mpl.clip_path import bbox_to_path

# Plot ALL data:
# releases = ["SingleBlast", "MultipleBlasts"]
releases = ["SingleBlast"]
# releases = ["MultipleBlasts"]
models = ["CnrvTrcr", "DcyTrcr", "Eutroph", "Simp"]

# Plot selected data:
# releases = ["SingleBlast"]
models = ["Eutroph"]
# models = ["Multiconsult"]
# ObsPt= ["Source"]

ObsPt= ["Source", "Spjelkavikelva", "Vasstrandlia", "Profiler", "FarField"]
# ObsPt= ["Source"]
DisplayPt = {"Source":"Blast Site", "Spjelkavikelva":"Spjelkavikelva", "Vasstrandlia":"Vasstrandlia Pump Intake",
             "Profiler":"Profiler", "FarField":"Nørebotnen"}
output_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen")

# # Single-blast models:
# # 1. Conservative Tracer
# input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\CnrvTrcr")
# species = ["CnrvTrcr"]
#
# # 2. Decaying Tracer
# input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\DcyTrcr")
# species = ["DcyTrcr"]
#
# # 3. Eutrophication model
# input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\Eutroph")
# species = ["EutrophNH4", "EutrophNO3"]
#
# # 4. Simple Oxygen model
# input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\Simp")
# species = ["SimpNH4", "SimpOxy"]
#
# # Distbuted-blast models
# # 1. Eutrophication model
# input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\MultipleBlasts\Eutroph")
# species = ["EutrophNH4", "EutrophNO3", "EutrophOXY"]

# Full list of chemical species and observation points:
allspecies = ["CnrvTrcr", "DcyTrcr", "SimpNH4", "SimpOxy", "EutrophNH4", "EutrophNO3", "EutrophOXY"]

for i, (release) in enumerate(releases):
    for j, (model) in enumerate(models):
        if release == "SingleBlast":
            if model == "CnrvTrcr":
                input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\CnrvTrcr")
                species = ["CnrvTrcr"]
            elif model == "DcyTrcr":
                input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\DcyTrcr")
                species = ["DcyTrcr"]
            elif model == "Eutroph":
                input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\Eutroph")
                species = ["NH4", "NO3"]
            elif model == "Simp":
                input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\SingleBlast\Simp")
                # species = ["NH4", "Oxy"]
                species = ["NH4"]
        elif release == "MultipleBlasts":
            if model == "Eutroph":
                input_directory = Path(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\MultipleBlasts\Eutroph")
                # species = ["NH4", "NO3", "OXY"]
                species = ["NH4", "NO3"]


        # Read in time series data for each species and observation point,
        # with conversion factors for concentration units
        for k, (spec) in enumerate(species):
            # Create an empty DataFrame to store the concatenated data
            for l, (pt) in enumerate(ObsPt):
                col_name = release + model + spec + pt
                file = spec+pt
                infilename = file+'.csv'
                # print(f'File {release}, {model}, {spec}, {pt}): ', infilename)
                in_path = input_directory / infilename
                if pt in DisplayPt:
                    pt = DisplayPt.get(pt)

                df = pd.read_csv(in_path, parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'], header=0, decimal='_')
                if i == 0 and j == 0 and k == 0 and l == 0:
                    combined_df = pd.DataFrame()
                    reference = pd.Timestamp('2024-08-01 00:00:00')
                    df.insert(1,'days_past', (df['Time [yyyy.MM.dd HH:mm:ss]'] - reference).dt.total_seconds() / (24 * 3600))
                    df.columns.values[2] = col_name
                    combined_df[('index1', 'index1','index1','Time [yyyy.MM.dd HH:mm:ss]')] = df.iloc[:, 0]
                    combined_df[('index2', 'index2', 'index2', 'days_past')] = df.iloc[:, 1]
                    combined_df[(release, model, spec, pt)] = df.iloc[:, 2]
                else:
                    combined_df[(release, model, spec, pt)] = df.iloc[:,1]
                if spec == 'NH4':
                    combined_df[(release, model, spec, pt)] = combined_df[(release, model, spec, pt)] #+ 0.011
                    print(combined_df)
                if spec == 'NO3':
                    combined_df[(release, model, spec, pt)] = combined_df[(release, model, spec, pt)] #+ 0.11
                    print(combined_df)
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

combined_df.columns = pd.MultiIndex.from_tuples(combined_df.columns)
combined_df.columns.names = ['release', 'model', 'species', 'location']

groundtruthNO3 = pd.read_csv(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\GroundTruth\NO3.csv",
                          parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'],sep=',',header=0,decimal='.')
reference = pd.Timestamp('2024-08-01 00:00:00')
groundtruthNO3.insert(1,'days_past',
                   (groundtruthNO3['Time [yyyy.MM.dd HH:mm:ss]'] - reference).dt.total_seconds() / (24 * 3600))

groundtruthNH4 = pd.read_csv(r"M:\Documents\External Projects\Fremmerholen\Output\Nitrogen\GroundTruth\NH4.csv",
                          parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'],sep=',',header=0,decimal='.')
reference = pd.Timestamp('2024-08-01 00:00:00')
groundtruthNH4.insert(1,'days_past',
                   (groundtruthNH4['Time [yyyy.MM.dd HH:mm:ss]'] - reference).dt.total_seconds() / (24 * 3600))

# Plotting
plt.figure(figsize=(13, 6))
plt.rcParams['font.size'] = 16

# plt.semilogy(groundtruthNO3['days_past'], groundtruthNO3['NO3 [gN/m3]'], 'bo', label='Measured NO3, [gN/m3]')
# plt.semilogy(groundtruthNH4['days_past'], groundtruthNH4['NH4 [gN/m3]'], 'r+', label='Measured NH4, [gN/m3]')

# NO3species = ["CnrvTrcr", "DcyTrcr", "NO3"]
# NH4species = ["NH4"]

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

# 'label' must be last argument
# label=f'{column[0]}_{column[1]}_{column[2]}_{column[3]}

for m, column in enumerate(NO3_cols):
    print(m, scalarMap.to_rgba(m))
    plt.semilogy(combined_df[('index2', 'index2', 'index2', 'days_past')], combined_df[column], color=scalarMap.to_rgba(m),
                 label=f'{column[3]}, {column[2]}')

for n, column in enumerate (NH4_cols):
    print(n, scalarMap.to_rgba(n))
    plt.semilogy(combined_df[('index2', 'index2', 'index2', 'days_past')], combined_df[column], '--',
                 color=scalarMap.to_rgba(n), label = f'{column[3]}, {column[2]}')

plt.xlabel('Days post-incident')
# plt.xlim(-75,95)
# plt.xticks(rotation=45)
plt.ylabel('Concentration (gN/m3)')
plt.grid()
plt.legend(bbox_to_anchor=(0.5,1), loc='lower center', markerscale=1, ncols=2, fontsize=16)
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

outfilename='combined'+'.png'
out_path = output_directory / outfilename

plt.savefig(out_path, dpi=600)
combined_df.to_csv('combined_columns.csv')

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

