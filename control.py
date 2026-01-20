import math as m
import numpy as np

class Control:
    def __init__(self, MotorControl, KinematicControl, SetVoltage, PIDConstants, SetPoint, SampleTime)
        self.Vset: float = SetVoltage
        self.OmegaBar: float = Vset*MotorControl[0] - MotorControl[1]
        self.m = MotorControl[0]
        self.b = MotorControl[1]
        self.P: float = 1/(KinematicControl*self.OmegaBar**2)
        self.K: dict[float] = PIDConstants
        self.SetPoint: float = SetPoint
        self.dt: float = SampleTime
    
    def __post_init__(self):
        self.ITune = 0

    def __repr__(self):
        rep = f"Set Point            : y = {self.SetPoint}\n
                Set Voltage          : V = {self.Vset}\n
                Set Motor Speed      : w = {self.OmegaBar}\n
                Proportional Constant: Kp =  {self.K['P']}\n
                Integral Constant    : Ki = {self.K['I']}\n
                Derivative Constant  : Kd = {self.K['D']}\n
                "
        return rep

    def PIDTune(self, yNew) -> None:
        Error = yNew - self.SetPoint
        self.ITune = self.ITune + self.K['I']*self.Error*self.dt
        PTune = self.K['P']*self.Error
        DTune = self.K['D']*self.Error/self.dt
        self.ErrorTuned = PTune + self.ITune + DTune

    def FindAlpha(self, yNew) -> None:
        self.PIDTune(yNew)
        self.alpha = m.sqrt(self.ErrorTuned*self.P + 1)
        
    def FindVoltages(self, yNew) -> list[float]:
        self.FindAlpha(yNew)
        V = (self.OmegaBar*self.alpha + self.b)/self.m
        if self.alpha <= 1:
            return [Vset, V]
        else:
            return [V, Vset]

def main() -> None:

if __name__ == "__main__":
    main()
