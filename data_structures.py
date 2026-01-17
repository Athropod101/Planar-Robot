from dataclasses import dataclass
import numpy as np
import math as m

SampleTime: tuple[float]

# Motor Data
Torque: float
Resistance: float
MotorConst: float

# Robot Data
WheelRadius: float
Differential: float

# Sensor Data
NoiseMean: float
NoiseSTDDev: float

# Pose Type
@dataclass
class Pose:
    Theta:  float = 0
    x:      float = 0
    y:      float = 0

    self.Pose = np.array[
            [m.cos(Theta) -m.sin(Theta) x],
            [m.sin(Theta)  m.cos(Theta) y],
            [0             0            1]
            ]
