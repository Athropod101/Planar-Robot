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

def main():
    # Testing Poles
    ''' WORKS!!!
    fig, ax = plt.subplots()
    σ = np.array([[-1, -1]])
    ω = np.array([[-1, 1]])

    Poles(ax, σ, ω)
    '''

    plt.show()

if __name__ == "__main__":
    main()
