from matplotlib import pyplot as plt, ticker as tkr
from dataclasses import dataclass, field
import numpy as np

def Poles(ax, σ: np.array, ω: np.array) -> None:
    nbins = 8
    msize = 20

    Underdamped = not (ω[0, 0] == ω[0, 1])
    w = ω[0, 1] # Extracting positive frequency

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
        # Percent Overshoot
        ax.plot([σ[0, 0], 0], [w, 0], color = "black", linestyle = '--', alpha = 0.5)
        ax.plot([σ[0, 0], 0], [-w, 0], color = "black", linestyle = '--', alpha = 0.5)

        # y-Lines
        ax.plot([σ[0, 0], 0], [w] * 2, color = "black", linestyle = '--', alpha = 0.5)
        ax.plot([σ[0, 0], 0], [-w] * 2, color = "black", linestyle = '--', alpha = 0.5)

        # x-Lines
        ax.plot([σ[0, 0]] * 2, [w, 0], color = "black", linestyle = '--', alpha = 0.5)
        ax.plot([σ[0, 0]] * 2, [-w, 0], color = "black", linestyle = '--', alpha = 0.5)

def Table(ax, Collumns: dict, Title: str) -> None:
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
    Table.set_fontsize(11)

def Response(ax, x: np.array, t: np.array, Title: str, xlabel: str, unit: str = "ms", tscale: float = 1e3, T_s: float = None, T_p: float = None) -> None:
    nbins = 8
    t = t * tscale
    Underdamped = True if T_p is not None else False
    Stable = True if T_s is not None else False

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

    # Setting Convergence Line if Stable
    if Stable:
        ax.axhline(
                y = abs(x[-1]),
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
    if Stable:
        T_s = T_s * tscale
        x_T_s = x[t >= T_s][0]
        ax.plot([T_s] * 2, sorted([x_T_s, 0]), color = "black", linestyle = "--", alpha = 0.5)
        ax.annotate(
                r'$\mathregular{T_s}$' + f' = {float(T_s):.3f} {unit}',
                xy = (2/3, 0),
                xycoords = 'axes fraction',
                xytext = (5, 5),
                textcoords = 'offset points',
                fontweight = 'bold'
                )

    # Plotting Peak Time
    T_p_lim = 4/3 * T_s
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
                r'$\mathregular{T_p}$' + f' = {float(T_p):.3f} ms',
                xy = (2 / 3 * T_p / T_s, 0),
                xycoords = 'axes fraction',
                xytext = (5, 5),
                textcoords = 'offset points',
                fontweight = 'bold'
                )

def main() -> None:
    fig, ax = plt.subplots()
    # Testing Poles
    ''' WORKS!!!
    σ = np.array([[-1, -1]])
    ω = np.array([[-1, 1]])

    Poles(ax, σ, ω)
    '''
    # Testing Tables
    ''' WORKS!!!
    Title = "Characters"
    Collumns = {
            "Name": ["Tianno", "Suleica", "John", "Faden"],
            "Height": ["6'0", "6'0", "6'2", "6'2"],
            "Specialization": ["Dragon", "Saint", "Knight", "Warlock"],
            }
    Table(ax, Collumns, Title)
    '''
    # Testing Response
    t = np.arange(0, 1, 0.001).reshape(1, -1) # -1 means "figure that one out, numpy"
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


    #plt.show()

if __name__ == "__main__":
    main()
