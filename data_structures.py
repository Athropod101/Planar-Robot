from dataclasses import dataclass, field
import numpy as np
np.set_printoptions(formatter={'float': '{:.4f}'.format})
import math as m
from typing import TypedDict

SampleTime: float

class MotorData(TypedDict):
    Torque: float
    Resistance: float
    MotorConst: float
    MaxVoltage: float
    MinVoltage: float

class RobotData(TypedDict):
    WheelRadius: float
    Differential: float

class SensorData(TypedDict):
    NoiseMean: float
    NoiseDev: float

class PIDConstants(TypedDict):
    kP: float
    kI: float
    kD: float

class PositionVector:
    def __init__(self, Theta, x, y):
        self.PositionVector = np.array([[Theta], [x], [y]])

    def __repr__(self):
        return f"{self.PositionVector}"

# Pose Type
@dataclass
class Pose:
    Theta:  float = 0
    x:      float = 0
    y:      float = 0

    def __post_init__(self):
        self.Pose = np.array([
            [m.cos(self.Theta), -m.sin(self.Theta), self.x],
            [m.sin(self.Theta),  m.cos(self.Theta), self.y],
            [0,                  0,                 1     ]
            ])

    def __repr__(self):
        return f"{self.Pose}"

def main() -> None:
    TransformTest = Pose(m.pi/4, 0, 5)
    print(TransformTest)

if __name__ == "__main__":
    main()
