from dataclasses import dataclass, field
from math import pi as π
import numpy as np
# Project Modules
import etc.data_structures as ds
from Plotting.Primitives import *
from Plotting.MosaicMotor import *
from Controls.StateSpace import *

class VoltageOverload(Exception):
    pass

class VoltageUnderload(Exception):
    pass

@dataclass
class Motor:
    Data: ds.MotorData
    A: np.array = field(init = False)
    B: np.array = field(init = False)
    System: SOStateSpace = field(init = False)
    x_t: np.array = field(init = False)
    t: np.array = field(init = False)
    α: float = field(init = False)

    
    def __post_init__(self):
        self.A = self._buildA()
        self.B = self._buildB()
        self.System = SOStateSpace(self.A)
        self.x_t, self.t = self.System.StepResponse(self.B)
        TableTitles = {"Left": "Parameters", "Right": "System Dynamics"}
        Headers = {"Datum": None, "Symbol": None, "Value": None, "Unit": None}
        TableContents = {"Left": self._buildLeftTable(Headers), "Right": self._buildRightTable(Headers)}
        self.Figure, self.Axes, self.Tables = MosaicMotor(
                Suptitle = "Motor System Analysis",
                t = self.t[0], x = self.x_t[1], xTitle = "Unit Step Response", xLabel = "Angular Velocity (rad/s)",
                σ = self.System.σ_d, ω = self.System.ω_d,
                TableTitles = TableTitles, TableContents = TableContents,
                T_s = self.System.T_s, T_p = self.System.T_p
                )
        self.α = self.Data.k / (self.Data.D * self.Data.R + self.Data.k**2)

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
    
    def SetSpeed(self, V_set: float) -> float:
        return self.α * V_set * 30 / π

    def _buildA(self) -> np.array:
        R, L, k, J, D = self.Data.R, self.Data.L, self.Data.k, self.Data.J, self.Data.D
        return np.array([
            [-R/L, -k/L],
            [ k/J, -D/J],
            ])

    def _buildB(self) -> np.array:
        L = self.Data.L
        return np.array([[1/L],[0]])

    def _buildLeftTable(self, Headers) -> list:
        cellData = [["Damping Constant", "Inertia", "Motor Constant", "Resistance", "Inductance", "Minimum Voltage", "Maximum Voltage"],
                    ["D", "J", "k", "R", "L", r"$\mathregular{V_{min}}$", r"$\mathregular{V_{max}}$"],
                    [f"{self.Data.D:.4f}", f"{self.Data.J:.4f}", f"{self.Data.k:.4f}", f"{self.Data.R:.4f}", f"{self.Data.L:.4f}", f"{self.Data.V_min:.4f}", f"{self.Data.V_max:.4f}"],
                    [r"$\mathregular{kgm^2/s}$", r"$\mathregular{kgm^2}$", r"$\mathregular{Vs}$", "Ω", "Ωs", "V", "V"],
                    ]
        return {header: col for header, col in zip(Headers.keys(), cellData)}

    def _buildRightTable(self, Headers) -> list:
        if self.System.Underdamped: 
            SecondFreq = ["Oscillation Frequency", r"$\mathregular{ω_d}$", f"{self.System.ω_d[1]:#.4g}"]
            T_p = f"{float(self.System.T_p * 1e3):#.4g}"
            pOV = f"{self.System.pOV:#.4g}"
        else:
            SecondFreq = ["Exponential Frequency", r"$\mathregular{σ_d}$", f"{abs(self.System.σ_d[1]):#.4g}"]
            T_p = "N/A"
            pOV = "0.0000"
        cellData = [["Exponential Frequency", SecondFreq[0], "Natural Frequency", "Damping Ratio", "Settling Time", "Peak Time", "Overshoot"],
                      [r"$\mathregular{σ_d}$", SecondFreq[1], r"$\mathregular{ω_n}$", "ζ", r"$\mathregular{T_s}$", r"$\mathregular{T_p}$", "%OV"],
                      [f"{abs(self.System.σ_d[0]):#.4g}", SecondFreq[2], f"{self.System.ω_n:#.4g}", f"{self.System.ζ:#.4g}", f"{float(self.System.T_s * 1e3):#.4g}", T_p, pOV],
                      ["Hz", "Hz", "Hz", "--", "ms", "ms", "%"]]
        return {header: col for header, col in zip(Headers.keys(), cellData)}

'''Testing'''
def main() -> None:
    Data = ds.MotorData()
    motor = Motor(Data)
    plt.show()

if __name__ == "__main__":
    main()
