from dataclasses import dataclass, field
from math import pi as π, exp, log10, floor
from data_structures import MotorData
import numpy as np
from matplotlib import pyplot as plt, ticker as tkr

class VoltageOverload(Exception):
    pass

class VoltageUnderload(Exception):
    pass

@dataclass
class Motor:
    Data: MotorData
    Plot: _SystemPlot
    A: np.array = field(init = False)
    B: np.array = field(init = False)
    System: SOStateSpace = field(init = False)
    x_t: np.array = field(init = False)
    t: np.array = field(init = False)

    
    def __post_init__(self):
        self.A = self._buildA()
        self.B = self._buildB()
        self.System = SOStateSpace(self.A)
        self.x_t, self.t = self.System.StepResponse(self.B)


    def WriteVoltage(self, Voltages: dict[float], rpm: bool = False) -> None:
        k = self.Data.k
        D = self.Data.D
        R = self.Data.R

        V_max = self.Data.V_max
        V_min = self.Data.V_min
        V = [Voltages["Left"], Voltages["Right"]]

        CONV = 30 / π if rpm == True else 1

        if max(V) > V_max:
            raise VoltageOverload(
                    f"\nERROR!!! Written voltage greater than maximum allowable motor voltage!\n\n"
                    f"Motor has been damaged. Shutting down simulation..."
                    )

        if min(V) < V_min:
            raise VoltageUnderload(
                    f"\nERROR!!! Written voltage less than minimum motor voltage!\n\n"
                    f"Under-voltaged robot behavior undefined in simulation. Shutting down..."
                    )

        ω = list(map(lambda v: (k * v / (D * R + k**2)) * CONV, V))

        self.ω = dict(zip(["Left", "Right"], ω))

    def _buildA(self) -> np.array:
        R, L, k, J, D = self.Data.R, self.Data.L, self.Data.k, self.Data.J, self.Data.D
        return np.array([
            [-R/L, -k/L],
            [ k/J, -D/J],
            ])

    def _buildB(self) -> np.array:
        L = self.Data.L
        return np.array([[1/L],[0]])

@dataclass
class _SystemPlot:
    System: _SystemData
    Data: MotorData

    def __post_init__(self):
        fig, ax = self._BuildFigure()
        self._BuildAxes(ax)
        self._BuildResponse(ax[0], self.System.t, self.System.ω_t, self.System.T_s, self.System.T_p, -self.System.AinvB[1, 0])
        self._BuildPoles(ax[1], self.System.σ_d, self.System.ω_d)
        self._BuildLeftTable(ax[2], self.Data)
        self._BuildRightTable(ax[3], self.System)
        plt.show()

    def _BuildFigure(self):
        fig, ax = plt.subplot_mosaic(
                [['Response', 'Poles'], ['LeftTable', 'RightTable']],
                layout = "constrained"
                )
        ax = list(ax.values())
        fig.suptitle("DC Motor System Data", fontsize = 16, fontweight = 'bold')
        return fig, ax

    def _BuildAxes(self, ax):
        titles = (
                "Transient Response Time",
                )
        ax[0].margins(x = 0)
        ax[0].axhline(
                y = abs(self.System.AinvB[1, 0]),
                color = "black",
                linestyle = '--',
                alpha = 0.5,
                zorder = 0,
                )
        for i in range(2):
            ax[i].set_title(titles[i], style = "italic")

    def _BuildResponse(self, ax, t, ω_t, T_s, T_p, AinvB):
        t = t * 1e3
        nbins = 8
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Angular Velocity (rad/s)")

        # Generating Ticks
        ax.xaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
        ax.yaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))

        response = ax.plot(t, ω_t, zorder = 5)

        # Removing 0-Tick:
        ax.set_xticks(ax.get_xticks()[1:])

        # Flooring x-Lim:
        ax.set_ylim(bottom = 0)

        # Plotting Settling Time
        ω_T_s = ω_t[t >= T_s * 1e3][0]
        ax.plot([T_s * 1e3] * 2, [ω_T_s, 0], color = "black", linestyle = "--", alpha = 0.5)
        ax.annotate(
                r'$\mathregular{T_s}$' + f' = {float(T_s * 1e3):.3f} ms',
                xy = (2/3, 0),
                xycoords = 'axes fraction',
                xytext = (5, 5),
                textcoords = 'offset points',
                fontweight = 'bold'
                )

        # Plotting Peak Time (if Applicable)
        if self.System.Underdamped and (T_p < 4/3 * T_s):
            ω_T_p = ω_t[t >= T_p * 1e3][0]
            ax.plot([T_p * 1e3] * 2, [ω_T_p, 0], color = "black", linestyle = "--", alpha = 0.5)
            ax.annotate(
                    r'$\mathregular{T_p}$' + f' = {float(T_p * 1e3):.3f} ms',
                    xy = (2 / 3 * T_p / T_s, 0),
                    xycoords = 'axes fraction',
                    xytext = (5, 5),
                    textcoords = 'offset points',
                    fontweight = 'bold'
                    )

        ax.grid(True)

    def _BuildLeftTable(self, ax, Data):
        DataText = [["Damping Constant", "Inertia", "Motor Constant", "Resistance", "Inductance", "Minimum Voltage", "Maximum Voltage"],
                    ["D", "J", "k", "R", "L", r"$\mathregular{V_{min}}$", r"$\mathregular{V_{max}}$"],
                    [f"{self.Data.D:.4f}", f"{self.Data.J:.4f}", f"{self.Data.k:.4f}", f"{self.Data.R:.4f}", f"{self.Data.L:.4f}", f"{self.Data.V_min:.4f}", f"{self.Data.V_max:.4f}"],
                    [r"$\mathregular{kgm^2/s}$", r"$\mathregular{kgm^2}$", r"$\mathregular{Vs}$", "Ω", "Ωs", "V", "V"],
                    ]
        Title = "Parameters"

        self._BuildTable(ax, DataText, Title)

    def _BuildRightTable(self, ax, System):
        Title = "System Dynamics"
        if System.Underdamped: 
            SecondFreq = ["Oscillation Frequency", r"$\mathregular{ω_d}$", f"{self.System.ω_d:#.4g}"]
            T_p = f"{float(self.System.T_p * 1e3):#.4g}"
            pOV = f"{self.System.pOV:#.4g}"
        else:
            SecondFreq = ["Exponential Frequency", r"$\mathregular{σ_d}$", f"{self.System.σ_d[1]:#.4g}"]
            T_p = "N/A"
            pOV = "0.0000"
        SystemText = [["Exponential Frequency", SecondFreq[0], "Natural Frequency", "Damping Ratio", "Settling Time", "Peak Time", "Overshoot"],
                      [r"$\mathregular{σ_d}$", SecondFreq[1], r"$\mathregular{ω_n}$", "ζ", r"$\mathregular{T_s}$", r"$\mathregular{T_p}$", "%OV"],
                      [f"{self.System.σ_d[0]:#.4g}", SecondFreq[2], f"{self.System.ω_n:#.4g}", f"{self.System.ζ:#.4g}", f"{float(self.System.T_s * 1e3):#.4g}", T_p, pOV],
                      ["Hz", "Hz", "Hz", "--", "ms", "ms", "%"]]

        self._BuildTable(ax, SystemText, Title)

    def _BuildTable(self, ax, cellText, title) -> None:
        colLabels = ["Datum", "Symbol", "Value", "Unit"]

'''Testing'''
def main() -> None:
    import sys
    sys.path.append("../Plotting/")
    sys.path.append("../Controls/")
    sys.path.append("../etc/")
    import etc.data_structures as ds
    from Plotting import Primitives, MosaicMotor
    from Controls import StateSpace

if __name__ == "__main__":
    main()
