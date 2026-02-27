from dataclasses import dataclass, field
import numpy as np
from matplotlib import pyplot as plt, table as tb
from Plotting.Primitives import *

def MosaicMotor(Suptitle: str, 
                t: np.array, x: np.array, xTitle: str, xLabel: str,
                σ: np.array, ω: np.array,
                TableTitles: dict[str], TableContents: dict[dict],
                T_s: float = None, T_p: float = None) -> tuple[plt.Figure, plt.Axes, tb.Table]:

    fig, ax = plt.subplot_mosaic([
        ['x(t)', 'Poles'],
        ['Left Table', 'Right Table']],
        layout = "constrained")
    fig.suptitle(Suptitle, fontsize = 16, fontweight = "bold")

    Response(ax['x(t)'], x, t, xTitle, xLabel, T_s = T_s, T_p = T_p)
    Poles(ax['Poles'], σ, ω)
    tab = {"Left": None, "Right": None}
    tab["Left"] = Table(ax['Left Table'], TableContents["Left"], TableTitles["Left"])
    tab["Right"] = Table(ax['Right Table'], TableContents["Right"], TableTitles["Right"])
    return fig, ax, tab

def main() -> None:
    Suptitle = "Mosaic Test"
    t = np.arange(0, 1, 0.001).reshape(1, -1) # -1 means "figure that one out, numpy"
    x = (lambda T: -np.exp(-10 * T) * np.cos(20 * T) + 1)(t)
    t = t[0]
    x = x[0]
    xTitle = "Simple Undamped"
    xLabel = "x axis"
    
    σ = np.array([[-1, -1]]).squeeze()
    ω = np.array([[-1, 1]]).squeeze()

    TableTitles = {"Left": "Characters", "Right": "Monsters"}
    TableContents = {"Left": {
                         "Name": ["Tianno", "Suleica", "John", "Faden"],
                         "Height": ["6'0", "6'0", "6'2", "6'2"],
                         "Specialization": ["Dragon", "Saint", "Knight", "Warlock"],
                         },
                     "Right": {
                         "Species": ["Nuckelavee", "Wendigo", "Leanan Sidhe", "Woodpecker", "Shadeling"],
                         "Type": ["Demon", "Demon", "Faerie", "Ghoul", "Demon"],
                         "Chapter": [1, 4, 8, 3, "Epilogue"],
                         }
                     }

    T_s = 0.9
    T_p = 0.134

    fig, ax, tab = MosaicMotor(Suptitle, t, x, xTitle, xLabel, σ, ω, TableTitles, TableContents, T_s = T_s, T_p = T_p)
    plt.show()

if __name__ == "__main__":
    main()
