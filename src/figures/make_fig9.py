"""Regenerate sampling scores and route from the retained public point dataset.

No new simulation, imagery download, or full-domain spread reconstruction.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'

def main():
    cells=pd.read_csv(DATA/'2.clustered_coordinates.csv')
    clusters=pd.read_csv(DATA/'3.cluster_info.csv')
    route=pd.read_csv(DATA/'4.highscore_path.csv')
    fig,axes=plt.subplots(2,1,figsize=(8,5.4),layout='constrained',sharex=True,sharey=True)
    outline=DATA/'validation/lake_outline_segments.csv'
    if outline.exists():
        a=pd.read_csv(outline).to_numpy().reshape(-1,2,2)
        for ax in axes:
            ax.add_collection(LineCollection(a,color='0.65',lw=.6))
    score='Depth-averaged uncertainty'
    sc=axes[0].scatter(cells.Longitude,cells.Latitude,c=cells[score],s=15,cmap='viridis',vmin=0,vmax=1)
    fig.colorbar(sc,ax=axes[0],label='Normalized model spread',shrink=.8,pad=.02)
    axes[0].set_title('(a) Retained 51 highest-scoring cells',loc='left',fontsize=10)
    palette=plt.get_cmap('tab10')
    for row in clusters.itertuples():
        d=cells[cells.cluster==row.cluster]
        label=chr(65+row.cluster)
        axes[1].scatter(d.Longitude,d.Latitude,s=12,color=palette(row.cluster),
                        label=f'{label}: {row.Weight:.2f}')
        axes[1].annotate(label,(row.Longitude,row.Latitude),xytext=(0,-13),
                         textcoords='offset points',ha='center',fontsize=8)
    axes[1].plot(route.longitude,route.latitude,'k.-',lw=1,ms=4)
    for row in route.iloc[:-1].itertuples():
        axes[1].annotate(str(int(row.label)),(row.longitude,row.latitude),xytext=(0,5),
                         textcoords='offset points',ha='center',fontsize=8)
    axes[1].set_title('(b) Cluster weights and selected route (5,647 m)',loc='left',fontsize=10)
    axes[1].legend(title='Cluster: summed normalized score',ncol=3,fontsize=8,
                   title_fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.30),frameon=False)
    for ax in axes:
        ax.set_xlim(6.38,6.575)
        ax.set_ylim(62.459,62.491)
        ax.set_aspect(1/np.cos(np.deg2rad(62.47)))
        ax.set_ylabel('Latitude (°N)')
        ax.grid(alpha=.15)
    axes[-1].set_xlabel('Longitude (°E)')
    fig.savefig(ROOT/'docs/manuscript/Fig9.png',dpi=400)
    plt.close(fig)

if __name__=='__main__':
    main()
