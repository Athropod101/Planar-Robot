# NOTE: posibilities for future improvements:
# 1. Make a function "DashLine" for all the horizontal and vertical lines.
from matplotlib import pyplot as plt, ticker as tkr, table as tab, text as txt
from dataclasses import dataclass, field
import numpy as np
import etc.data_structures as ds
from math import degrees
import yaml

def Poles(ax: plt.Axes, σ: np.array, ω: np.array) -> None:
    nbins = 8
    msize = 20

    Underdamped = not (ω[0] == ω[1])
    w = max(ω) # Extracting positive frequency

    # Initial setup
    ax.set_title("S-Plane Stability", style = "italic")
    ax.scatter(σ, ω, s = msize, marker = "o", zorder = 10, color = "red")
    ax.set_xlim(right = -np.min(σ))
    ax.grid(True)

    # Moving Spines
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


    # Generating Ticks
    ax.xaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
    if Underdamped:
        ax.yaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
    else:
        ax.set_yticks([0] * nbins)

    # Statically Locking Ticks
    ax.set_xticks(ax.get_xticks())
    ax.set_yticks(ax.get_yticks())

    # Making y-axis imaginary
    ax.set_yticklabels([f"{y.get_text()}j" for y in ax.get_yticklabels()])

    # Erasing 0 from the Tick Labels
    for xlabel, ylabel in zip(ax.get_xticklabels(), ax.get_yticklabels()):
        xpos, _ = xlabel.get_position()
        _, ypos = ylabel.get_position()
        Erasex = (xpos < np.min(σ)) or (xpos == 0) or (xpos > -np.min(σ))
        Erasey = (ypos < -w) or (ypos == 0) or (ypos > w)

        xlabel.set_visible(~Erasex)
        ylabel.set_visible(~Erasey)

    # Annotating Real Axis
    ax.annotate(
            f'Real (σ)',
            xy = (1, 0.5),
            xycoords = 'axes fraction',
            xytext = (-50, 5),
            textcoords = 'offset points',
            fontweight = 'bold'
            )

    # Annotating Imaginary Axis
    ax.annotate(
            f'Imag (ω)',
            xy = (0.5, 1),
            xycoords = 'axes fraction',
            xytext = (5, -10),
            textcoords = 'offset points',
            fontweight = 'bold'
            )

    # Underdamped Extra Lines
    if Underdamped:
        for i in range(σ.shape[0]):
            if ω[i] == 0: continue
            # Percent Overshoot
            ax.plot([σ[i], 0], [ω[i], 0], color = "black", linestyle = '--', alpha = 0.5)

            # y-Lines
            ax.plot([σ[i], 0], [ω[i]] * 2, color = "black", linestyle = '--', alpha = 0.5)

            # x-Lines
            ax.plot([σ[i]] * 2, [ω[i], 0], color = "black", linestyle = '--', alpha = 0.5)

def Table(ax: plt.Axes, Collumns: dict, Title: str) -> tab.Table:
    colors = ['lightgray', 'white']
    HeaderColor = '#6dd0ee'
    ax.set_title(Title, style = 'italic')

    # Deleting spines
    for i, spine in enumerate(ax.spines.keys()):
        ax.spines[spine].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    colLabels = list(Collumns.keys())
    cellText = list(map(list, zip(*Collumns.values()))) # Transposes them

    n = len(cellText)
    m = len(colLabels)
    cellColors = [None] * n
    rowColors = [colors[0] if col % 2 == 0 else colors[1] for col in range(m)]
    cellColors = [rowColors for _ in range(n)]

    Table = ax.table(
            cellText = cellText,
            cellColours = cellColors,
            colLabels = colLabels,
            loc = 'upper center', cellLoc = 'center', colColours = [HeaderColor] * m)
    Table.auto_set_font_size(False)
    Table.set_fontsize(11)
    C, R = GetTableScale()
    Table.scale(C, R)
    return Table

def Response(ax: plt.Axes, x: np.array, t: np.array, Title: str, xlabel: str, unit: str = "ms", tscale: float = 1e3, T_s: float = None, T_p: float = None) -> None:
    nbins = 8
    t = t * tscale
    Underdamped = True if T_p is not None else False
    Stable = True if not isinstance(T_s, list) else False
    T_s = T_s[0] if not Stable else T_s

    # Initial Setup
    ax.plot(t, x, zorder = 5)
    ax.set_title(Title, style = "italic")
    ax.margins(x = 0)
    ax.set_xlabel(f"Time ({unit})")
    ax.set_ylabel(xlabel)
    ax.grid(True)

    # Trim the y-lim so the value of t = 0 is snug on a corner.
    if x[-1] > x[0]:
        ax.set_ylim(bottom = x[0])
    else: 
        ax.set_ylim(top = x[0])

    # Setting Convergence/Zero-Crossing Line
    y = x[-1] if Stable else x[t >= T_s * tscale][0]
    ax.axhline(
            y = y,
            color = "black",
            linestyle = '--',
            alpha = 0.5,
            zorder = 0,
            )

    # Generating Ticks
    ax.xaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
    ax.yaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))

    # Removing 0-Tick:
    ax.set_xticks(ax.get_xticks()[1:])

    # Plotting Settling Time
    textloc = 0 if x[-1] >= 0 else 0.9
    T_s = T_s * tscale
    x_T_s = x[t >= T_s][0]
    ax.plot([T_s] * 2, sorted([x_T_s, 0]), color = "black", linestyle = "--", alpha = 0.5)
    ax.annotate(
            r'$\mathregular{T_s}$' + f' = {int(T_s)} {unit}',
            xy = (2/3, textloc),
            xycoords = 'axes fraction',
            xytext = (5, 5),
            textcoords = 'offset points',
            fontweight = 'bold'
            )

    # Plotting Peak Time
    T_p_lim = 3/4 * T_s if Stable else None
    if Underdamped:
        T_p = T_p * tscale
        x_T_p = x[t >= T_p][0]
    elif Stable:
        x_T_p = np.max(x)
        T_p = t[x == x_T_p][0] # Have to index it cause otherwise its a (1,) array...

    if Stable and (T_p < T_p_lim):
        ax.plot([T_p] * 2, sorted([x_T_p, 0]), color = "black", linestyle = "--", alpha = 0.5)
        ax.plot([0, T_p], [x_T_p] * 2, color = "black", linestyle = "--", alpha = 0.5)
        ax.annotate(
                r'$\mathregular{T_p}$' + f' = {int(T_p)} ms',
                xy = (2 / 3 * T_p / T_s, textloc),
                xycoords = 'axes fraction',
                xytext = (5, 5),
                textcoords = 'offset points',
                fontweight = 'bold'
                )

def DualPlotFrame(ax: plt.Axes, t: list, x1: list, x2: list, Title: str, ylabel: str, legendlabels: list[str], bounds: list[float] = None) -> plt.Line2D:
    ax.margins(x = 0)

    # Drawing Empty Lines
    Lines = [None] * 2
    for i in range(2):
        Lines[i], = ax.plot([], [])

    # Drawing y-bound lines
    y = []
    if bounds == None:
        y.append(0)
        y.append(min(x1[1:] + x2[1:])) # Ignore first entry to ignore 0-initial conditions on capped quantities.
        y.append(max(x1 + x2)) # 0-IC is free to be max if in our plots if applicable.
    else:
        y = bounds
    for i in range(len(y)):
        ax.axhline(
                y = y[i],
                color = "black",
                linestyle = "--",
                alpha = 0.5,
                zorder = 0,
                )

    # Adjusting y-margins
    if bounds == None:
        margin = 1.05 # This is the default matplotlib margin. I have to set lims because the plot doesn't exist yet, so margins won't work properly.
        ax.set_ylim(top = y[2] * margin, bottom = y[1] * margin)

    # Setting Ticks
    ax.set_xticks([0, t[-1]])
    ax.set_yticks(sorted(y))

    # Title and Labels
    ax.set_title(Title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Time (s)")

    # Setting Legend
    ax.legend(
            labels = legendlabels,
            fontsize = 'small',
            handlelength = 0.1,
            loc = 'center right',
            )

    return Lines

def MapFrame(ax: plt.Axes, x: list, y: list, y_set) -> plt.Line2D:
    # Making the line
    Line, = ax.plot([], [])

    # Set-point Line
    ax.axhline(
            y = y_set,
            linestyle = "--",
            color = "black",
            alpha = 0.5,
            zorder = 0,
            )

    # Setting Limits
    margins = 1.05 # The matplotlib standard
    xlims = [min(x), max(x)]
    ylims = [min(y), max(y)]
    minlim = 0.1 + y_set
    for lim in [ylims, xlims]: # Making sure y_set isn't literally at the spine.
        if lim[0] > -minlim: lim[0] = -minlim
        if lim[1] <  minlim: lim[1] =  minlim
        minlim = minlim - y_set
    ax.set_xlim([lim * margins for lim in xlims])
    ax.set_ylim([lim * margins for lim in ylims])

    # Setting Ticks
    ax.set_xticks([0, round(x[-1], 2)])
    ax.set_yticks(sorted([y_set, y[0]]))

    # Setting Titles
    ax.set_title("Robot Position Map")
    ax.set_xlabel("x-Position (m)")
    ax.set_ylabel("y-Position (m)")
    return Line

def Marker(ax: plt.Axes, θ, x, y) -> plt.Line2D:
    Line, = ax.plot(x, y, marker = (3, 0, (degrees(θ) + 30)),
            markersize = 15,
            linestyle = '-',
            color = 'cyan',
            mec = 'black',
            )
    return Line

def PoseText(ax: plt.Axes, Pose: ds.Position) -> txt.Text:
    Pose = ax.text(
            x = 0.975,
            y = 0.5,
            s = Pose.Pose,
            transform = ax.transAxes,
            ha = 'right',
            va = 'center',
            )
    return Pose

def GetTableScale() -> tuple[list[int]]:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    TAR = config['Figure Data']['Table Scale']
    return (TAR['Cols'], TAR['Rows'])

def main() -> None:
    fig, ax = plt.subplots()
    # Testing Poles
    ''' WORKS!!!
    σ = np.array([[-1, -1]])
    ω = np.array([[-1, 1]])

    Poles(ax, σ, ω)
    '''
    # Testing Tables
    Title = "Characters"
    Collumns = {
            "Name": ["Tianno", "Suleica", "John", "Faden"],
            "Height": ["6'0", "6'0", "6'2", "6'2"],
            "Specialization": ["Dragon", "Saint", "Knight", "Warlock"],
            }
    tab = Table(ax, Collumns, Title)
    # Testing Response
    t = np.arange(0, 1, 0.001)
    xlabel = "x axis"
    ''' Undamped works
    Title = "Simple Undamped"
    x = (lambda T: -np.exp(-10 * T) * np.cos(20 * T) + 1)(t)
    Response(ax, x[0], t[0], Title, xlabel, T_s = 0.6, T_p = 0.123)
    '''
    ''' Works!!!
    Title = "Simple Overdamped"
    x = (lambda T: -np.exp(-10 * T) * np.cos(20 * T) + 1)(t)
    Response(ax, x[0], t[0], Title, xlabel, T_s = 0.5)
    '''
    plt.show()

if __name__ == "__main__":
    main()
