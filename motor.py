from dataclasses import dataclass, field
from math import pi as π, exp
from scipy.linalg import expm
from data_structures import MotorData
from numpy import array, sqrt, eye, empty, arange, shape
from numpy.linalg import eig, inv
from matplotlib import pyplot as plt

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

        self.SystemPlot = _SystemPlot(self.System)

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
        T = 2 * T_s
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

    def __post_init__(self):
        fig, ax = self._BuildFigure()
        self._BuildAxes(ax)
        self._BuildResponse(ax[0], self.System.t, self.System.ω_t)
        self._BuildPoles()
        plt.show()

    def _BuildFigure(self):
        fig, ax = plt.subplots(1, 2, layout = "constrained")
        fig.suptitle("DC Motor System Data")

        return fig, ax

    def _BuildAxes(self, ax):
        ylines = (
                abs(self.System.AinvB[1, 0]),
                0,
                )
        titles = (
                "Transient Response Time",
                "S-Plane Stability",
                )
        ax[0].margins(x = 0)

        for i in range(2):
            ax[i].axhline(
                    y = ylines[i],
                    color = "black",
                    linestyle = '--',
                    alpha = 0.5,
                    zorder = 0,
                    )

            ax[i].set_title(titles[i])

            ax[1].axvline(
                    x = 0,
                    color = "black",
                    linestyle = '--',
                    alpha = 0.5,
                    zorder = 0,
                    )

    def _BuildResponse(self, ax, t, ω_t):
        response = ax.plot(t, ω_t)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Angular Velocity (rad/s)")

    def _BuildPoles(self):
        pass

'''Testing'''
def main() -> None:
    TestMotor = Motor()
    print(TestMotor.System.Underdamped)
    print(TestMotor.System.pOV)

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
