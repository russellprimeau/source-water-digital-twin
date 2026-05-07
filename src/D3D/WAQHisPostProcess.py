"""
WAQHisPostProcess.py

Plot data from Deflt3D WAQ simulation output written to a CSV file (to avoid needing to develop code for reading WAQ-style HIS NetCDF file).csv
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'

# Lists of chemical species and observation points, used to loop through output CSV files from different model versions
# species = ["CnrvTrcr", "DcyTrcr", "SimpNH4", "SimpOxy", "EutrophNH4", "EutrophNO3", "EutrophOXY"]
species = ["NH4", "NO3"]
ObsPt= ["Source", "Spjelkavikelva", "Vasstrandlia", "Profiler", "FarField"]
DisplayPt = {"Source":"Blast Site", "Spjelkavikelva":"Spjelkavikelva", "Vasstrandlia":"Vasstrandlia Pump Intake",
             "Profiler":"Profiler", "FarField":"Nørebotnen"}
input_directory = DATA_DIR
output_directory = DATA_DIR

# Read in time series data for each species and observation point, with conversion factors for concentration units
for spec in species:
    # Create an empty DataFrame to store the concatenated data
    for ind, (pt) in enumerate(ObsPt):
        file = spec+pt
        infilename = file+'.csv'
        in_path = input_directory / infilename
        if pt in DisplayPt:
            pt = DisplayPt.get(pt)

        df = pd.read_csv(in_path, parse_dates=['Time [yyyy.MM.dd HH:mm:ss]'], decimal='_')
        df.insert(1,'days_past', (df['Time [yyyy.MM.dd HH:mm:ss]'] - df['Time [yyyy.MM.dd HH:mm:ss]'].iloc[0]).dt.total_seconds() / (24 * 3600))
        if spec == 'EutrophNH4':
            df.iloc[:,2] *= 1287  # Convert concentration values from gN/m3 to ug NH4/L
            df.rename(columns={df.columns[2]: 'NH4 [ug/L]'}, inplace=True)
        elif spec == 'EutrophNO3':
            df.iloc[:,2] *= 4427  # Convert concentration values from gN/m3 to ug NO3/L
            df.rename(columns={df.columns[2]: 'NO3 [ug/L]'}, inplace=True)
        if ind == 0:
            y_col = df.columns[2]
            df = df.rename(columns={y_col:pt})
            combined_df = df
        else:
            df = df.rename(columns={y_col:pt})
            combined_df = pd.concat([combined_df, df.iloc[:,2]], axis=1)
            # Calculate cumulative load for Spjelkavikelva, to feed Lillevatnet analysis
            if pt == "Spjelkavikelva":
                df["Mass"] = df["Spjelkavikelva"]*3.6*180 # Calculate g/hr as g/m3 * 3.6 s*m3/l*hr * 180 l/s
                cumulative = {'Timesteps':[24, 168, 720, 2209], 'Period':['1 day', '1 week', '1 month', '3 months'],
                              'Cumulative load, g':[0.5,0.5,0.5,0.5]}
                cumulativeN = pd.DataFrame(data=cumulative)
                for i in range(len(cumulativeN['Timesteps'])):
                    cumulativeN.iloc[i,2] = df['Mass'].iloc[:cumulativeN.iloc[i,0]].sum()
                sumfilename = 'sum' + spec + '.csv'
                sumout_path = output_directory / sumfilename
                cumulativeN.to_csv(sumout_path, index=False)


    x_col = df.columns[0]

    print(combined_df.head())

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.rcParams['font.size'] = 15
    for column in combined_df.columns[2:]:
        plt.semilogy(combined_df['days_past'], combined_df[column], label=column)
    plt.xlabel('Days post-incident')
    plt.xticks(rotation=45)
    plt.ylabel('Concentration, '+y_col)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # To view the figure:
    plt.show()

    outfilename=spec+'.png'
    out_path = output_directory / outfilename

    plt.savefig(out_path)
    plt.close()

    # Save out a table of showing the time at which the maximum value occurs for each observation point
    results = []
    for col in combined_df.columns[1:]:
        max_value = combined_df[col].max()
        max_index = combined_df[col].idxmax()
        corresponding_datetime = combined_df.loc[max_index, 'Time [yyyy.MM.dd HH:mm:ss]']
        results.append({'Column': col, 'Max Value': max_value, 'Datetime': corresponding_datetime})

    # Convert the results to a DataFrame and save
    results_df = pd.DataFrame(results)
    maxfilename = 'max' + spec + '.csv'
    maxout_path = output_directory / maxfilename
    results_df.to_csv(maxout_path, index=False)

    # Save out a table showing the time at which the minimum value occurs for each observation point
    minresults = []
    for col in combined_df.columns[1:]:
        min_value = combined_df[col].min()
        min_index = combined_df[col].idxmin()
        corresponding_datetime = combined_df.loc[min_index, 'Time [yyyy.MM.dd HH:mm:ss]']
        minresults.append({'Column': col, 'Min Value': min_value, 'Time': corresponding_datetime})

    # Convert the results to a DataFrame and save
    minresults_df = pd.DataFrame(minresults)
    minfilename = 'min' + spec + '.csv'
    minout_path = output_directory / minfilename
    minresults_df.to_csv(minout_path, index=False)

