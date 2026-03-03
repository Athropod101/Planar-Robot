'''
This class is responsible for computing the full robot system's dynamics. It exists OUTSIDE of the simulation loop, calculating loop constants and checking whether or not the system will stably converge. Its public outputs are:

    1. Constants: Computation of variables like γ for particular system analysis.
    2. Stability: Determination of whether or not the robot will actually converge during simulation. Instability will raise an error, ending the simulation early.
    3. Plots    : Setting up the plot mosaic for...
        a. The unit response of x, y, θ as well as the pole plot around small angles. 
        b. The unit response of the motor feedback system as well as the pole plot at the saturated error region.
'''

from dataclasses import dataclass, field
from math import pi as π
import numpy as np
# Project Modules
import etc.data_structures as ds
from Plotting.Primitives import *
from Plotting.Mosaics import *
from Controls.StateSpace import *
from Systems.motor import *

@dataclass
class Robot:
    Motor: Motor
    Body: ds.BodyData
    Control: ds.ControllerData

    β: float = field(init = False)
    γ: float = field(init = False)
    System_Sat: SOStateSpace = field(init = False)
    System_Small: StateSpace = field(init = False)
    x_t_sat: np.array = field(init = False)
    t_sat: np.array = field(init = False)

    def __post_init__(self):
        # Constant Computing
        self.β = self.Body.r / self.Body.l
        self.γ = self.Motor.α * self.β
        self.ω_set = self.Motor.SetSpeed(self.Control.V_set)
        self.Vel_set = self.ω_set * self.Body.r * π / 30

        # Handling Saturated Error
        self.A_sat = self._buildA("Saturated")
        self.B_sat = self._buildB("Saturated")
        self.System_Sat = SOStateSpace(self.A_sat)
        self.x_t_sat, self.t_sat = self.System_Sat.StepResponse(self.B_sat, U = np.array([[-π/2]]))
        θ_t = self.x_t_sat[0] * 180 / π
        TableTitles = {"Left": "Parameters", "Right": "System Dynamics"}
        Headers = {"Datum": None, "Symbol": None, "Value": None, "Unit": None}
        TableContents = {"Left": self._buildLeftTable(Headers), "Right": self._buildRightTable(Headers)}
        self.Figure_sat, self.Axes_sat, self.Tables_sat = MosaicMotor(
                Suptitle = "Robot Saturated Error Analysis",
                t = self.t_sat[0], x = θ_t, xTitle = "Step Response", xLabel = "Angle (degrees)",
                σ = self.System_Sat.σ_d, ω = self.System_Sat.ω_d,
                TableTitles = TableTitles, TableContents = TableContents,
                T_s = self.System_Sat.T_s, T_p = self.System_Sat.T_p
                )

        # Handling Small Error
        y_set = 0.01
        self.A_small = self._buildA("Small")
        self.B_small = self._buildB("Small")
        self.System_Small = StateSpace(self.A_small)
        self.x_t_small, self.t_small = self.System_Small.StepResponse(self.B_small, U = np.array([[y_set]]))
        self.x_t_small[1] = self.x_t_small[1] * 180 / π
        self.Figure_small, self.Axes_small, self.Table_small = MosaicRobot(
                Suptitle = "Robot Small Error Analysis",
                t = self.t_small[0], x = self.x_t_small, xTitles = ["Step Response (Position)", "Step Response (Orientation)"], xLabels = ["Position (m)", "Angle (degrees)"], 
                σ = self.System_Small.σ_d, ω = self.System_Small.ω_d,
                TableTitle = TableTitles["Left"], TableContents = TableContents["Left"],
                T_s = self.System_Small.T_s, T_p = self.System_Small.T_p
                )
        # Adding the set point line:
        if self.System_Small.Stable:
            t_zc = self.t_small.squeeze()[self.x_t_small[0] >= y_set][0] * 1000
            self.Axes_small['x(t)1'].plot([0, t_zc], [y_set] * 2, linestyle = "--", color = "black", alpha = 0.5, zorder = 0)
            self.Axes_small['x(t)1'].plot([t_zc] * 2, [0, y_set], linestyle = "--", color = "black", alpha = 0.5, zorder = 0)
 
    def _buildA(self, Mode: str) -> np.array:
        kp   = self.Control.kp
        ki   = self.Control.ki
        kt   = self.Control.kt
        γ    = self.γ
        Vel_set = self.Vel_set
        match Mode:
            case "Saturated":
                return np.array([
                    [0  ,   1],
                    [-γ * ki, -kp * γ],
                    ])
            case "Small":
                return np.array([
                    [0,         Vel_set,   0],
                    [0,               0,   1],
                    [- π/2 * kt,    -ki * γ, -kp * γ],
                    ])

    def _buildB(self, Mode: str) -> np.array:
        ki = self.Control.ki
        kt = self.Control.kt
        γ = self.γ
        match Mode:
            case "Saturated":
                return np.array([[0], [γ * ki]])
            case "Small":
                return np.array([[0], [0], [π/2 * kt *γ * ki]])

    def _buildLeftTable(self, Headers) -> list:
        cellData = [["Differential", "Wheel Radius", "Proportional", "Integral", "Derivative", "Tangent", "Set Voltage", "Set Wheel Speed"],
                    ["l", "r", r"$\mathregular{k_{p}}$", r"$\mathregular{k_{i}}$", r"$\mathregular{k_{d}}$", r"$\mathregular{k_{t}}$", r"$\mathregular{V_{set}}$", r"$\mathregular{ω_{set}}$"],
                    [f"{self.Body.l:.4f}", f"{self.Body.r:.4f}", f"{self.Control.kp:.4f}", f"{self.Control.ki:.4f}", f"{self.Control.kd:.4f}", f"{self.Control.kt:.4f}", f"{self.Control.V_set:.4f}", f"{int(self.ω_set)}"],
                    ["m", "m", "--", "1/s", "s", "1/m", "V", "rpm"],
                    ]
        return {header: col for header, col in zip(Headers.keys(), cellData)}

    def _buildRightTable(self, Headers) -> list:
        if self.System_Sat.Underdamped: 
            SecondFreq = ["Oscillation Frequency", r"$\mathregular{ω_d}$", f"{self.System_Sat.ω_d[1]:#.4g}"]
            T_p = f"{float(self.System_Sat.T_p * 1e3):#.4g}"
            pOV = f"{self.System_Sat.pOV:#.4g}"
        else:
            SecondFreq = ["Exponential Frequency", r"$\mathregular{σ_d}$", f"{abs(self.System_Sat.σ_d[1]):#.4g}"]
            T_p = "N/A"
            pOV = "0.0000"
        cellData = [["Exponential Frequency", SecondFreq[0], "Natural Frequency", "Damping Ratio", "Settling Time", "Peak Time", "Overshoot"],
                      [r"$\mathregular{σ_d}$", SecondFreq[1], r"$\mathregular{ω_n}$", "ζ", r"$\mathregular{T_s}$", r"$\mathregular{T_p}$", "%OV"],
                      [f"{abs(self.System_Sat.σ_d[0]):#.4g}", SecondFreq[2], f"{self.System_Sat.ω_n:#.4g}", f"{self.System_Sat.ζ:#.4g}", f"{float(self.System_Sat.T_s * 1e3):#.4g}", T_p, pOV],
                      ["Hz", "Hz", "Hz", "--", "ms", "ms", "%"]]
        return {header: col for header, col in zip(Headers.keys(), cellData)}

    def Speed(self, Voltage) -> float:
        return Voltage * self.Motor.α * self.Body.r

def main():
    Data = ds.MotorData()
    motor = Motor(Data)
    Body = ds.BodyData()
    Control = ds.ControllerData()

    robot = Robot(motor, Body, Control)
    plt.show()
    
if __name__ == "__main__":
    main()
