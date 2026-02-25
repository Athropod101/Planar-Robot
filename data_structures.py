'''
data_structures.py is responsible for setting up the data objects that will be configured in simulator.py and later passed to the other modules during instantiation. 

Each class is structured such that it takes in arguments with human-readable names, but each attribute is given a mathematical mnemonic after initialization.

Furthermore, default values are given in this module to make isolated module-testing consistent. 
'''
from dataclasses import dataclass
import numpy as np
from numpy import sin, cos
from typing import Literal

@dataclass
class MotorData:
    Eq_Viscosity    : float = 0.0072 # kgm2/s
    Inertia         : float = 0.0010 # kgm2
    Motor_Constant  : float = 0.4604 # V/rad
    Resistance      : float = 0.9470 # Ω
    Inductance      : float = 0.0220 # Ωs
    Max_Voltage     : float = 6.0000 # V
    Min_Voltage     : float = 3.0000 # V

    def __post_init__(self):
        self.D      = self.Eq_Viscosity
        self.J      = self.Inertia
        self.k      = self.Motor_Constant
        self.R      = self.Resistance
        self.L      = self.Inductance
        self.V_max  = self.Max_Voltage
        self.V_min  = self.Min_Voltage

@dataclass
class BodyData:
    Wheel_Radius: float = 0.05 # m
    Differential: float = 0.10 # m
    Inertia     : float = 0.20 # kgm2
    Mass        : float = 0.50 # kg

    def __post_init__(self):
        self.r = self.Wheel_Radius
        self.l = self.Differential
        self.J = self.Inertia
        self.m = self.Mass

@dataclass
class SensorData:
    Mean                : float = 0 # rad/s
    Deviation_Multiplier: float = 0 #

    def __post_init__(self):
        self.μ      = self.Mean
        self.σ_mult = self.Deviation_Multiplier

@dataclass
class ControllerData:
    Set_Point               : float = 0 # m
    Set_Voltage             : float = 6 # V
    Proportional_Constant   : Literal["Default"] | float = "Default"

@dataclass
class SimulationData:
    Sample_Time     : float = 0.001 # s
    Max_Iterations  : int   = 1e5   #
    Tolerance       : float = 0.001 #

    def __post_init__(self):
        self.δt     = self.Sample_Time
        self.i      = self.Max_Iterations
        self.TOL    = self.Tolerance

@dataclass
class Position:
    θ: float = 0 # rad
    x: float = 0 # m
    y: float = 0 # m

    def __post_init__(self):
        self.Vector = np.array([
            [self.θ],
            [self.x],
            [self.y]
            ])
        self.Pose = np.array([
            [cos(self.θ), -sin(self.θ), self.x],
            [sin(self.θ),  cos(self.θ), self.y],
            [0,            0,           1     ]
            ])
