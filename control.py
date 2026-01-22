import math as m
import numpy as np
from dataclasses import dataclass

@dataclass
class Control:
    y_set : float
    V_set : float
    dt    : float
    kP    : float
    kI    : float
    kD    : float
    DWR   : float
    m     : float
    V_max : float
    V_min : float
    
    def __post_init__(self):
        self.IError    : float = 0
        self.ThetaError: float = 0
        if self.V_set > self.V_max:
            print(
                    f"Target voltage ({self.V_set} V) exceeds maximum allowable voltage ({self.V_max} V).\n"
                    f"Setting target voltage to maximum allowable voltage (V_set = {self.V_max} V).\n"
                    )
            self.V_set = self.V_max
        self.dV_cap    : float = self.V_set - self.V_min

    def _SetTheta(self, y_new) -> float:
        yError   : float = y_new - y_set
        Theta_set: float = m.arctan(yError)
        return Theta_set

    def _PIDTune(self, Theta_set, Theta_new) -> float:
        ThetaError_new: float  = Theta_new - Theta_set
        PTune         : float  = self.kP * ThetaError_new
        self.ITune    : float += self.kI * ThetaError * self.dt
        DTune         : float  = self.kD * (ThetaError_new * self.ThetaError) / self.dt
        TunedError    : float  = PTune + self.ITune + DTune
        return TunedError

    def _FindAlpha(self, TunedError) -> float:
        beta : float = self.DWR / self.m / self.dV_cap / self.dt
        alpha: float = TunedError * beta
        if alpha > 1 / beta:
            alpha = 1
        elif alpha < -1 / beta:
            alpha = -1
        return alpha

    def FindVoltages(self, y_new, Theta_new) -> dict[float]:
        Theta_set : float = self._SetTheta(y_new)
        TunedError: float = self._PIDTune(Theta_set, Theta_new)
        alpha     : float = self._FindAlpha(TunedError)
        V         : float = abs(alpha) * self.dV_cap
        if alpha >= 0:
            return {'Left Voltage': self.V_set, 'Right Voltage': V}
        else:
            return {'Left Voltage': V, 'Right Voltage': self.V_set}
    
def main() -> None:
    MotorControl = {'m': 3.8397, 'b': 2.0944}
    KinematicControl = 0.004
    SetVoltage = 5
    PIDConstants = {'kP': 1, 'kI': 0.5, 'kD': 0.5}
    SetPoint = 0
    SampleTime = 0.5
    InitialPosition = np.array([[0], [0.5], [0]])

    Controller = Control(
            SetPoint,
            InitialPosition[1].item(),
            SetVoltage,
            SampleTime,
            KinematicControl,
            **MotorControl,
            **PIDConstants
            )

    print(Controller)
    Controller.FindVoltages(0.5)

if __name__ == "__main__":
    main()
