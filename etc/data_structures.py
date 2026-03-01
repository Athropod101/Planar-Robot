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
    D    : float = 0.1520 # kgm2/s
    J    : float = 0.0010 # kgm2
    k    : float = 0.4500 # V/rad
    R    : float = 0.9470 # Ω
    L    : float = 0.0020 # Ωs
    V_min: float = 3.0000 # V
    V_max: float = 6.0000 # V

@dataclass
class BodyData:
    r: float = 0.05 # m
    l: float = 0.10 # m

@dataclass
class SensorData:
    μ     : float = 0 # rad/s
    σ_mult: float = 5 #

@dataclass
class ControllerData:
    y_set: float = 0   # m
    V_set: float = 6   # V
    kp   : float = 20  # -
    ki   : float = 1   # -
    kd   : float = 0.2 # -
    kt   : float = 15

@dataclass
class SimulationData:
    δt     : float = 0.02  # s
    i_max  : int   = 1e5   #
    Tol       : float = 0.1   #

    def __post_init__(self):
        self.t      = [0]
        self.i      = 0
        self.TOL    = self.Tol

@dataclass
class Position:
    θ: float = 0 # rad
    x: float = 0 # m
    y: float = 1 # m

    @property
    def Vector(self):
        return np.array([
            [self.θ],
            [self.x],
            [self.y]
            ])

    @property
    def Pose(self):
        return np.round(np.array([
            [cos(self.θ), -sin(self.θ), self.x],
            [sin(self.θ),  cos(self.θ), self.y],
            [0,            0,           1     ]
            ]), 2)
