from dataclasses import dataclass, field
from math import pi as π, exp, log10, floor
from scipy.linalg import expm
from data_structures import MotorData
from numpy import array, sqrt, eye, empty, arange, shape
from numpy.linalg import eig, inv
from matplotlib import pyplot as plt, ticker as tkr

class VoltageOverload(Exception):
    pass

class VoltageUnderload(Exception):
    pass

@dataclass
class _SystemData:
    λ           : None = None
    σ_d         : None = None
    ω_d         : None = None
    Underdamped : None = None
    ω_n         : None = None
    ζ           : None = None
    T_s         : None = None
    T_p         : None = None
    pOV         : None = None

@dataclass
class Motor:
    Data: MotorData = field(default_factory = lambda: MotorData())

    
    def __post_init__(self):
        self.System = _SystemData()

        A = self._Find_A()
        B = array([[1 / self.Data.L], [0]])

        λ, null = eig(A)
        σ_d = abs(λ.real)
        ω_d = abs(λ.imag[0])
        Underdamped = True if ω_d != 0 else False
        ω_n = sqrt(σ_d.prod())
        ζ = self._Find_ζ(ω_d, σ_d, Underdamped, ω_n)
        T_s = 4 / min(σ_d)

        if Underdamped:
            T_p = π / ω_d
            pOV = 100 * exp(-ζ * π / sqrt(1 - ζ**2))

        ω_t, t, AinvB = self._Find_Response(A, B, T_s)


        # Storing as Object Data
        self.System.A = A
        self.System.B = B
        self.System.λ = λ
        self.System.σ_d = σ_d
        self.System.ω_d = ω_d
        self.System.Underdamped = Underdamped
        self.System.ω_n = ω_n
        self.System.ζ = ζ
        self.System.T_s = T_s
        self.System.ω_t = ω_t
        self.System.t = t
        self.System.AinvB = AinvB
        if Underdamped:
            self.System.T_p = T_p
            self.System.pOV = pOV

        self.SystemPlot = _SystemPlot(self.System, self.Data)

    def WriteVoltage(self, Voltages: dict[float], rpm: bool = False) -> dict[float]:
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

        return dict(zip(["Left", "Right"], ω))

    def _Find_A(self) -> array:
        R, L, k, J, D = self.Data.R, self.Data.L, self.Data.k, self.Data.J, self.Data.D
        
        A = array([
            [-R/L, -k/L],
            [ k/J, -D/J],
            ])

        return A

    def _Find_ζ(self, ω_d, σ_d, Underdamped, ω_n) -> float:
        if Underdamped:
            ζ = sqrt(1 / (ω_d / σ_d[0] + 1))
        else:
            ζ = sum(σ_d) / 2 / ω_n

        return ζ

        sqrt(1 / (ω_d / σ_d + 1))

    def _Find_Response(self, A, B, T_s) -> array:
        T = 1.5 * T_s
        i_max = 1000
        δt = T / i_max
        Ainv = inv(A)
        AinvB = Ainv @ B
        ω_t = empty((1, i_max), dtype = float)
        t   = empty((1, i_max), dtype = float)
        for i in range(i_max):
            ω_t[0, i] = ((expm(A * δt * i) - eye(2)) @ AinvB)[1, 0]
            t[0, i] = δt * i
        return ω_t.squeeze(), t.squeeze(), AinvB

@dataclass
class _SystemPlot:
    System: _SystemData
    Data: MotorData

    def __post_init__(self):
        fig, ax = self._BuildFigure()
        self._BuildAxes(ax)
        self._BuildResponse(ax[0], self.System.t, self.System.ω_t, self.System.T_s, self.System.T_p, -self.System.AinvB[1, 0])
        self._BuildPoles(ax[1], self.System.σ_d, self.System.ω_d)
        self._BuildTable(ax[2], self.System, self.Data)
        plt.show()

    def _BuildFigure(self):
        fig, ax = plt.subplot_mosaic(
                [['Response', 'Poles'], ['Table', 'Table']],
                layout = "constrained"
                )
        ax = list(ax.values())
        fig.suptitle("DC Motor System Data")
        return fig, ax

    def _BuildAxes(self, ax):
        titles = (
                "Transient Response Time",
                "S-Plane Stability",
                )

        ax[0].margins(x = 0)
        ax[0].axhline(
                y = abs(self.System.AinvB[1, 0]),
                color = "black",
                linestyle = '--',
                alpha = 0.5,
                zorder = 0,
                )

        ax[1].spines['left'].set_position('zero')
        ax[1].spines['bottom'].set_position('zero')
        ax[1].spines['right'].set_visible(False)
        ax[1].spines['top'].set_visible(False)

        for i in range(2):
            ax[i].set_title(titles[i])

    def _BuildResponse(self, ax, t, ω_t, T_s, T_p, AinvB):
        t = list(map(lambda T: T * 1e3, t))
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
        ax.plot([T_s * 1e3] * 2, [AinvB, 0], color = "black", linestyle = "--", alpha = 0.5)
        ax.annotate(
                r'$\mathregular{T_s}$' + f' = {int(T_s * 1e6)} μs',
                xy = (2/3, 0),
                xycoords = 'axes fraction',
                xytext = (5, 5),
                textcoords = 'offset points',
                fontweight = 'bold'
                )

        # Plotting Peak Time (if Applicable)
        if self.System.Underdamped:
            ax.plot([T_p * 1e3] * 2, [AinvB, 0], color = "black", linestyle = "--", alpha = 0.5)
            ax.annotate(
                    r'$\mathregular{T_p}$' + f' = {int(T_p * 1e6)} μs',
                    xy = (2 / 3 * T_p / T_s, 0),
                    xycoords = 'axes fraction',
                    xytext = (5, 5),
                    textcoords = 'offset points',
                    fontweight = 'bold'
                    )

        ax.grid(True)

    def _BuildPoles(self, ax, σ_d, ω_d):
        nbins = 8
        ω_d = abs(ω_d)
        σ_d = (-σ_d[0], -σ_d[1])
        ax.scatter(σ_d, [ω_d, -ω_d], s = 20, marker = 'o', zorder = 10, color = "red")
        ax.set_xlim(right = -min(σ_d))
        ax.grid(True)

        # Generating Ticks
        ax.xaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
        if self.System.Underdamped:
            ax.yaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins))
        else:
            ax.set_yticks([0] * nbins)

        # Statically Locking Ticks
        ax.set_xticks(ax.get_xticks())
        ax.set_yticks(ax.get_yticks())

        # Adding j to all y-Tick Labels
        ax.set_yticklabels([f"{y.get_text()}j" for y in ax.get_yticklabels()])

        # Erasing 0 from the Tick Labels
        for xlabel, ylabel in zip(ax.get_xticklabels(), ax.get_yticklabels()):
                xpos, _ = xlabel.get_position()
                _, ypos = ylabel.get_position()
                Erasex = (xpos < min(σ_d)) or (xpos == 0) or (xpos > -min(σ_d))
                Erasey = (ypos < -ω_d) or (ypos == 0) or (ypos > ω_d)

                xlabel.set_visible(~Erasex)
                ylabel.set_visible(~Erasey)


        # Underdamped Extra Lines
        if self.System.Underdamped:
            # Percent Overshoot
            ax.plot([σ_d[0], 0], [ω_d, 0], color = "black", linestyle = '--', alpha = 0.5)
            ax.plot([σ_d[0], 0], [-ω_d, 0], color = "black", linestyle = '--', alpha = 0.5)

            # y-Lines
            ax.plot([σ_d[0], 0], [ω_d] * 2, color = "black", linestyle = '--', alpha = 0.5)
            ax.plot([σ_d[0], 0], [-ω_d] * 2, color = "black", linestyle = '--', alpha = 0.5)

            # x-Lines
            ax.plot([σ_d[0]] * 2, [ω_d, 0], color = "black", linestyle = '--', alpha = 0.5)
            ax.plot([σ_d[0]] * 2, [-ω_d, 0], color = "black", linestyle = '--', alpha = 0.5)

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

    def _BuildTable(self, ax, System, Data):
        for i, spine in enumerate(ax.spines.keys()):
            ax.spines[spine].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        colLabels = ["Datum", "Symbol", "Value", "Unit"] * 2
        DataText = [["Damping Constant", "Inertia", "Motor Constant", "Resistance", "Inductance", "Minimum Voltage", "Maximum Voltage"],
                    ["D", "J", "k", "R", "L", r"$\mathregular{V_{min}}$", r"$\mathregular{V_{max}}$"],
                    [f"{self.Data.D:.4f}", f"{self.Data.J:.4f}", f"{self.Data.k:.4f}", f"{self.Data.R:.4f}", f"{self.Data.L:.4f}", f"{self.Data.V_min:.4f}", f"{self.Data.V_max:.4f}"],
                    [r"$\mathregular{kgm^2/s}$", r"$\mathregular{kgm^2}$", r"$\mathregular{Vs}$", "Ω", "Ωs", "V", "V"],
                    ]

        if System.Underdamped: 
            SecondFreq = ["Oscillation Frequency", r"$\mathregular{ω_d}$", f"{int(self.System.ω_d)}"]
            T_p = f"{int(self.System.T_p * 1e6)}"
            pOV = f"{self.System.pOV:.4f}"
        else:
            SecondFreq = ["Exponential Frequency", r"$\mathregular{σ_d}$", f"{int(self.System.σ_d[1])}"]
            T_p = "N/A"
            pOV = "0.0000"
        SystemText = [["Exponential Frequency", SecondFreq[0], "Natural Frequency", "Damping Ratio", "Settling Time", "Peak Time", "Overshoot"],
                      [r"$\mathregular{σ_d}$", SecondFreq[1], r"$\mathregular{ω_n}$", "ζ", r"$\mathregular{T_s}$", r"$\mathregular{T_p}$", "%OV"],
                      [f"{int(self.System.σ_d[0])}", SecondFreq[2], f"{int(self.System.ω_n)}", f"{self.System.ζ:.4f}", f"{int(self.System.T_s * 1e6)}", T_p, pOV],
                      ["Hz", "Hz", "Hz", "", "μs", "μs", "%"]]

        cellText = DataText + SystemText
        cellText = list(map(list, zip(*cellText)))

        cellColors = [['lightgray'] * 8, ['w'] * 8]
        for i in range(3): cellColors = cellColors + [['lightgray'] * 8, ['w'] * 8]
        cellColors.pop()

        Table = ax.table(cellText = cellText, cellColours = cellColors, colLabels = colLabels, loc = 'center', cellLoc = 'center', colColours = ['#6dd0ee'] * 8)
        Table.auto_set_font_size(False)
        Table.set_fontsize(10)
        Table.auto_set_column_width(range(8))

'''Testing'''
def main() -> None:
    TestMotor = Motor()

    def Display(Vl, Vr, RPM = False) -> None:
        ω = {k: round(v, 2) for k, v in TestMotor.WriteVoltage({"Left": Vl, "Right": Vr}, RPM).items()}
        print(ω)

    #print("\nTesting Write Voltage:")
    #Display(5, 5)
    #print("\nTesting Below Minimum Voltage:")
    #Display(2, 3)
    #Display(3, 2)
    #print("\nTesting RPM:")
    #Display(5, 5, True)
    #print("\nTesting Above Maximum Voltage:")
    #Display(7, 3)

if __name__ == "__main__":
    main()
