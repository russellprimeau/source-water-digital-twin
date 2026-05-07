"""
CSVplotter.py

Generates a scatter plot of Delft3D model calibration iterations based on data from a CSV file. 
Filters data rows and creates a scatter plot.

Output: 
-"calibration_w_sizes.png"
    - The x-axis represents 'Simulation Time/Run Time'.
    - The y-axis represents 'Root Mean Squared Error'.
    - The size of the points is scaled based on the '3D Cells' column.
    - The color of the points is determined by the 'Correlation' column, using a colormap.
    - A colorbar is added to indicate the correlation values.
    - A legend is created to indicate the size of the points based on the number of 3D cells.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'

# Step 1: Read the CSV file
data = pd.read_csv(DATA_DIR / 'Calibration.csv', sep=';', header=0)
# filtered_data = data[data['Include?'] > -1]  # Replace with your condition
data['End'] = pd.to_datetime(data['End'],dayfirst=True)
filtered_data = data[(data['End'] > pd.Timestamp('26.06.2024 00:00')) & (data['Simulation Time/Run Time'] < 1400)]  # Replace with your condition
# red_data = data[(data['Index'] > 16) & (data['Index'] < 20)]  # Replace with your condition

# Step 2: Extract the necessary columns
x = filtered_data['Simulation Time/Run Time']  # Replace with your x-axis column name
y = filtered_data['Root Mean Squared Error']  # Replace with your y-axis column name
z = filtered_data['Correlation']
sizes = filtered_data['3D Cells']/800  # Replace with the column name for scaling


norm = colors.Normalize(vmin=z.min(), vmax=z.max())  # Normalize the z values to the range [0, 1]
cmap = cm.spring  # Choose a colormap
colors = cmap(norm(z))  # Map the normalized z values to colors


# x2 =red_data['Simulation Time/Run Time']  # Replace with your x-axis column name
# y2 = red_data['Root Mean Squared Error']  # Replace with your y-axis column name
# red_sizes = red_data['3D Cells']/800  # Replace with the column name for scaling


# Create the scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, s=sizes, alpha=1.0, c=colors)

# Create legend with example sizes
divider = make_axes_locatable(ax)  # Create a divider for the existing axes instance
example_sizes = [10000/800, 40000/800, 70000/800]  # Example sizes
example_labels = ['≤ 10,000 cells', '10,000 - 40,000 cells', '40,000 - 70,000 cells']  # Corresponding labels


# Create a colorbar
cax = divider.append_axes("right", size="2%", pad=0.05)  # Append axes to the right of the current axes
cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), label='Correlation', cax=cax)

# Create proxy artists for the legend
handles = [plt.scatter([], [], s=size, label=label, color='black') for size, label in zip(example_sizes, example_labels)]

# Add legend
ax.legend(handles=handles, title='3D Cells Per Model Iteration', loc='upper right')


# Retrieve existing handles and labels
handles, labels = scatter.legend_elements()

# Step 3: Create a scatter plot

plt.rcParams['axes.titlesize'] = 25  # You can adjust the size as needed
plt.rcParams['axes.labelsize'] = 25  # Adjust the size for axis labels
ax.set_xlabel('Simulation Time/Run Time')  # Replace with your x-axis label
ax.set_ylabel('Root Mean Squared Error')  # Replace with your y-axis label
# plt.title('Calibration Iterations')
ax.grid(True)
plt.tight_layout()  # Keeps the legend from extending out of the figure
plt.savefig(DATA_DIR / 'calibration_w_sizes.png', dpi=500)
plt.show()
