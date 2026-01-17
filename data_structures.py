from dataclasses import dataclass

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
