import math as m
import numpy as np
from dataclasses import dataclass

@dataclass
class Control:
    y_set: float
    y_o  : float
    V_set: float
    dt   : float
    p    : float
    m    : float
    b    : float
    kP   : float
    kI   : float
    kD   : float

    def __post_init__(self):
        self.OmegaBar = self.V_set*self.m - self.b
        self.P = 1/(self.p*self.OmegaBar**2)
        self.Error = self.y_o - self.y_set
        self.ITune = 0

    def __repr__(self):
        rep = (
                f"Set Point            : y  = {self.y_set:4.2f} m\n"
                f"Set Voltage          : V  = {self.V_set:4.2f} V\n"
                f"Set Motor Speed      : w  = {int(self.OmegaBar*30/m.pi):4d} rpm\n"
                f"Proportional Constant: kp = {self.kP:4.2f}\n"
                f"Integral Constant    : ki = {self.kI:4.2f} 1/s\n"
                f"Derivative Constant  : kd = {self.kD:4.2f} s\n"
                f"Kinematic Constant   : p  = {self.p:.4f}\n"
                f"Plant Constant       : P  = {self.P:.4f}\n"
                )
        return rep

    def _PIDTune(self, yNew) -> None:
        NewError = yNew - self.y_set
        PTune = self.kP*NewError
        self.ITune += self.kI*NewError*self.kI
        DTune = self.kD*(NewError - self.Error)/self.dt
        self.ErrorTuned = PTune + self.ITune + DTune
        self.Error = NewError

    def _FindAlpha(self) -> None:
        if self.ErrorTuned <= 0:
            self.alpha = m.sqrt(self.ErrorTuned*self.P + 1) if self.ErrorTuned >= -1/self.P else 0
        elif self.ErrorTuned >= 0:
            self.alpha = m.sqrt(1 - self.ErrorTuned*self.P) if self.ErrorTuned <= 1/self.P else 0
        else:
            print("Robot error has exceeded control range. Alpha is imaginary.")
        
    def FindVoltages(self, yNew: float) -> list[float]:
        self._PIDTune(yNew)
        self._FindAlpha()
        V = (self.OmegaBar*self.alpha + self.b)/self.m
        print(
                f'Position     : {yNew:1.2f} m\n'
                f'Error        : {self.Error:1.2f} m\n'
                f'Tuned Error  : {self.ErrorTuned:1.2f} m\n'
                f'Alpha        : {self.alpha:1.2f}'
                )
        if self.ErrorTuned > 0:
            print(
                    f"Left Voltage : {self.V_set:1.2f} V\n"
                    f"Right Voltage: {V:1.2f} V\n"
                    )
            return [self.V_set, V]
        else:
            print(
                    f"Left Voltage : {V} V\n"
                    f"Right Voltage: {self.V_set} V\n"
                    )
            return [V, self.V_set]

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
