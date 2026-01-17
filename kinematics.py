import numpy as np
import scipy as sc
import math as m
from dataclasses import dataclass

@dataclass
class Kinematics:
    WheelRadius: float
    Differential: float
    SampleTime: float

    y: list[float] = 0
    theta: list[float] = 0
    x = [0]                 #   x is assumed to start at 0 by assumption. 
    
    def FindOmega(self, LeftOmega: float, RightOmega: float) -> float:
        return 2*self.WheelRadius/self.Differential*(RightOmega - LeftOmega)

    def FindDeltaTheta(self, Omega: float, SampleTime: float) -> float:
        return Omega*SampleTime

    def 
