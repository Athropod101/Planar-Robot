import data_structures as ds
import math as m
from dataclasses import dataclass

@dataclass
class Kinematics:
    SampleTime  : float
    WheelRadius : float
    Differential: float
    Theta       : float
    x           : float
    y           : float

    def __post_init__(self):
        self.DWR: float = (self.Differential / 2 / self.WheelRadius)

    def _FindOmega(self, LeftOmega: float, RightOmega: float) -> None:
        self.Omega = 2 * self.WheelRadius / self.Differential * (RightOmega - LeftOmega)

    def _FindTheta(self, LeftOmega: float, RightOmega: float) -> None:
        self._FindOmega(LeftOmega, RightOmega)
        DelTheta = self.Omega * self.SampleTime
        self.Theta += DelTheta # % (2 * m.pi)
        self.Theta = m.atan2( m.sin(self.Theta) , m.cos(self.Theta) )

    def _FindVelocities(self, LeftOmega: float, RightOmega: float) -> None:
        self._FindTheta(LeftOmega, RightOmega)
        self.Vx = (RightOmega + LeftOmega) * self.WheelRadius / 2 * m.cos(self.Theta)
        self.Vy = self.Vx * m.tan(self.Theta)

    def FindKinematics(self, LeftOmega: float, RightOmega: float) -> dict[float]:
        self._FindVelocities(LeftOmega, RightOmega)
        self.x += self.Vx * self.SampleTime
        self.y += self.Vy * self.SampleTime
        return {'Theta': self.Theta, 'x': self.x, 'y': self.y}

def main() -> None:
    RobotData = {"WheelRadius" : 0.02, "Differential" : 0.1}
    InitialPosition = {'Theta': 0, 'x': 0, 'y': 0}
    SampleTime = 0.1

    # Test at no Velocity Differential
    OL = 2
    OR = 2

    KinSample = Kinematics(SampleTime, **RobotData, **InitialPosition)
    print(KinSample.FindKinematics(OL, OR))

    # Test at positive Velocity Differential
    OL = 1
    OR = 3

    KinSample = Kinematics(SampleTime, **RobotData, **InitialPosition)
    KinSample.FindKinematics(OL, OR)
    print(KinSample.FindKinematics(OL, OR))

    # Test at negative Velocity Differential
    OL = 3
    OR = 1

    KinSample = Kinematics(SampleTime, **RobotData, **InitialPosition)
    KinSample.FindKinematics(OL, OR)
    print(KinSample.FindKinematics(OL, OR))

if __name__ == "__main__":
    main()
