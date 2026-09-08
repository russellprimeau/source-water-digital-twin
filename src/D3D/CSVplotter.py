"""
CSVplotter.py

Model accuracy against computational cost for the Delft3D FM calibration
campaign, from data/Calibration.csv.

Output: data/calibration_w_sizes.png

  - x: simulated time per unit wall-clock time (dimensionless speed-up).
  - y: mean depth-wise RMSE in water temperature (degrees C).
  - marker size: number of 3D cells.
  - marker colour: Pearson correlation coefficient.
  - vertical bars: the range of RMSE spanned by configurations sharing the
    same mesh and vertical layer count, i.e. the variation attributable to
    settings other than spatial resolution.

Only full-season simulations are plotted.  The campaign also contains shorter
two-month runs, but an RMSE accumulated over a two-month spring window is not
comparable with one accumulated over a full season that includes autumn
cooling, and plotting both on a shared axis invites exactly that comparison.
"""

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"

X_COLUMN = "Simulation Time/Run Time"
Y_COLUMN = "Root Mean Squared Error"
MIN_FULL_SEASON_HOURS = 4000  # separates full-season runs from the two-month set

data = pd.read_csv(DATA_DIR / "Calibration.csv", sep=";", header=0)
data.columns = [c.strip() for c in data.columns]
for column in (X_COLUMN, Y_COLUMN, "Correlation", "3D Cells", "Max Layers", "Simulation Period (h)"):
    data[column] = pd.to_numeric(data[column].astype(str).str.replace(",", ""), errors="coerce")

# Match the actual common comparison window, not just a minimum duration.
# Inclusion flags belonged to the earlier plot; all ten matching-window runs
# are included here so parameter extremes remain visible.
starts = pd.to_datetime(data['Start'], format='%d.%m.%Y %H:%M')
ends = pd.to_datetime(data['End'], format='%d.%m.%Y %H:%M')
full_season = data[(starts == pd.Timestamp('2024-04-25')) &
                   (ends == pd.Timestamp('2024-11-20'))].dropna(
    subset=[X_COLUMN, Y_COLUMN, "Correlation", "3D Cells"]
)
if full_season.empty:
    raise ValueError("No full-season runs found in Calibration.csv; check 'Simulation Period (h)'.")

x = full_season[X_COLUMN]
y = full_season[Y_COLUMN]
z = full_season["Correlation"]
sizes = full_season["3D Cells"] / 800

norm = colors.Normalize(vmin=z.min(), vmax=z.max())
cmap = cm.spring

fig, ax = plt.subplots(figsize=(7.5, 5.2))

# Range of RMSE across configurations sharing a mesh and layer count.  Each
# point is a single deterministic simulation, so this is not sampling error; it
# shows how much of the spread is driven by settings other than the mesh.
for (_cells, _layers), group in full_season.groupby(["3D Cells", "Max Layers"]):
    if len(group) < 2:
        continue
    ax.vlines(
        group[X_COLUMN].mean(),
        group[Y_COLUMN].min(),
        group[Y_COLUMN].max(),
        color="0.55",
        linewidth=1.2,
        zorder=1,
    )

ax.scatter(x, y, s=sizes, c=cmap(norm(z)), alpha=1.0, zorder=2, edgecolors="none")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.05)
plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), label="Pearson correlation coefficient", cax=cax)

example_sizes = [20000 / 800, 40000 / 800, 65000 / 800]
example_labels = ["20,000 cells", "40,000 cells", "65,000 cells"]
handles = [
    plt.scatter([], [], s=size, label=label, color="black") for size, label in zip(example_sizes, example_labels)
]
ax.legend(handles=handles, title="3D cells per model iteration", loc="upper right", fontsize=8, title_fontsize=9)

ax.set_xlabel("Simulated time per unit run time (dimensionless)")
ax.set_ylabel("Mean depth-wise RMSE ($^\\circ$C)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(DATA_DIR / "calibration_w_sizes.png", dpi=500)
print(f"Plotted {len(full_season)} full-season configurations "
      f"(excluded {len(data) - len(full_season)} shorter or incomplete runs).")
print(f"Written: {DATA_DIR / 'calibration_w_sizes.png'}")
