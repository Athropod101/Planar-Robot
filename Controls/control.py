import math as m
from dataclasses import dataclass

@dataclass
class Control:
    y_set: float
    V_set: float
    dt   : float
    DWR  : float
    kP   : float
    kI   : float
    kD   : float
    m    : float
    V_max: float
    V_min: float
    
    def __post_init__(self):
        self.Theta_set : float = 0
        self.IError    : float = 0
        self.ThetaError: float = 0
        self.dV_cap    : float = self.V_set - self.V_min
        self.beta      : float = self.DWR / self.m / self.dV_cap / self.dt
        if self.V_set > self.V_max:
            print(
                    f"Target voltage ({self.V_set} V) exceeds maximum allowable voltage ({self.V_max} V).\n"
                    f"Setting target voltage to maximum allowable voltage (V_set = {self.V_max} V).\n"
                    )
            self.V_set = self.V_max
            self.dV_cap = self.V_max - self.V_min

    def _SetTheta(self, y_new) -> float:
        self.yError   : float = y_new - self.y_set
        #Theta_set: float = m.atan(-self.yError)
        Theta_set: float = m.tanh(-self.yError) * m.pi / 2
        self.Theta_set = Theta_set
        if __name__ == "__main__":
            print(
                    f"Position Error    : {float(self.yError):5.2f} m"
                    )
        return Theta_set

    def _PIDTune(self, Theta_set, Theta_new) -> float:
        ThetaError_new: float  = Theta_new - Theta_set
        self.PError        : float  = self.kP * ThetaError_new
        self.IError           += self.kI * ThetaError_new * self.dt
        self.DError        : float  = self.kD * (ThetaError_new - self.ThetaError) / self.dt
        self.TunedError    : float  = self.PError + self.IError + self.DError
        self.ThetaError = ThetaError_new

        return self.TunedError

    def _FindAlpha(self, TunedError) -> float:
        beta : float = self.beta
        alpha: float = TunedError * beta
        if alpha > 1:
            alpha = 1
        elif alpha < -1:
            alpha = -1
        return alpha

    def FindVoltages(self, y_new, Theta_new) -> dict[float]:
        Theta_set : float = self._SetTheta(y_new)
        TunedError: float = self._PIDTune(Theta_set, Theta_new)
        alpha     : float = self._FindAlpha(TunedError)
        V         : float = self.V_set - abs(alpha) * self.dV_cap
        if alpha > 0:
            return {'Left Voltage': self.V_set, 'Right Voltage': V}
        elif alpha < 0:
            return {'Left Voltage': V, 'Right Voltage': self.V_set}
        else:
            return {'Left Voltage': self.V_set, 'Right Voltage': self.V_set}
    
def main() -> None:
    y_set = 0
    V_set = 5
    dt = 0.1
    PIDConstants = {'kP': 1, 'kI': 0, 'kD': 0}
    DWR = 0.1 / (2 * 0.02)
    MotorData = {'m': 3.8402, 'V_max': 6, 'V_min': 3}

    y = ([0] * 3) + ([0.1] * 3) + ([-0.1] * 3)
    u = ([0, 0.1, -0.1]) * 3
    Test = Control(y_set, V_set, dt, DWR, **PIDConstants, **MotorData)
    for i in range(9):
        y_val = y[i]
        u_val = u[i]
        Test.IError = 0
        print(f"\033[2J\033[H") # Clears the whole print screen!
        print("==========TEST DATA===========")
        print(f"Position          : {float(y_val):5.2f} m")
        print(f"Orientation       : {float(u_val):5.2f} rad")
        print("==============================")
        print(Test)
        print(Test.FindVoltages(y_val, u_val))

        input("Press Enter to continue")

if __name__ == "__main__":
    main()
