import math as m
import numpy as np

class Control:
    def __init__(self, MotorControl, KinematicControl, SetVoltage, PIDConstants, SetPoint, SampleTime, InitialPosition):
        self.Vset: float = SetVoltage
        self.OmegaBar: float = self.Vset*MotorControl[0] - MotorControl[1]
        self.m = MotorControl[0]
        self.b = MotorControl[1]
        self.P: float = 1/(KinematicControl*self.OmegaBar**2)
        self.K: dict[float] = PIDConstants
        self.SetPoint: float = SetPoint
        self.dt: float = SampleTime
        self.Error = InitialPosition[1].item() - SetPoint
    
        # Post-Init
        self.ITune = 0

    def __repr__(self):
        rep = (
            f'Set Point            : y = {self.SetPoint} m\n'
            f'Set Voltage          : V = {self.Vset} V\n'
            f'Set Motor Speed      : w = {self.OmegaBar} rad/s\n'
            f'Proportional Constant: Kp =  {self.K['P']}\n'
            f'Integral Constant    : Ki = {self.K['I']} 1/s\n'
            f'Derivative Constant  : Kd = {self.K['D']} s\n'
            )
        return rep

    def _PIDTune(self, yNew) -> None:
        NewError = yNew - self.SetPoint
        self.ITune += self.K['I']*NewError*self.dt
        PTune = self.K['P']*NewError
        DTune = self.K['D']*(NewError - self.Error)/self.dt
        self.ErrorTuned = PTune + self.ITune + DTune
        self.Error = NewError

    def _FindAlpha(self) -> None:
        if self.ErrorTuned <= 0:
            self.alpha = m.sqrt(self.ErrorTuned*self.P + 1) if self.ErrorTuned >= -1/self.P else 0
        else:
            self.alpha = m.sqrt(1 - self.ErrorTuned*self.P) if self.ErrorTuned <= 1/self.P else 0
        
    def FindVoltages(self, yNew: float) -> list[float]:
        self._PIDTune(yNew)
        self._FindAlpha()
        V = (self.OmegaBar*self.alpha + self.b)/self.m
        print(
                f'Position   : {yNew}\n'
                f'Alpha      : {self.alpha}\n'
                f'Error      : {self.Error}\n'
                f'Tuned Error: {self.ErrorTuned}\n'
                )
        if self.ErrorTuned > 0:
            return [self.Vset, V]
        else:
            return [V, self.Vset]

def main() -> None:
    MotorControl = [3.8397, 2.0944]
    KinematicControl = 0.004
    SetVoltage = 5
    PIDConstants = {'P': 1, 'I': 0, 'D': 0}
    SetPoint = 0
    SampleTime = 0.5
    InitialPosition = np.array([[0], [0.5], [0]])

    Controller = Control(MotorControl, KinematicControl, SetVoltage, PIDConstants, SetPoint, SampleTime, InitialPosition)
    print(Controller.FindVoltages(-0.1))
    print(Controller.FindVoltages(0.1))
    print(Controller.FindVoltages(0))

if __name__ == "__main__":
    main()
