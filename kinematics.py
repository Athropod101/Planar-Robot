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
    Theta: list[float] = 0
    x = [0]                 #   x is assumed to start at 0 by assumption. 
    
    Omega: list[float] = []
    Vx: list[float] = []
    Vy: list[float] = []

    def FindOmega(self, LeftOmega: float, RightOmega: float) -> None:
        OmegaNew = 2*self.WheelRadius/self.Differential*(RightOmega - LeftOmega)
        self.Omega.append(OmegaNew)

    def FindTheta(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindOmega(LeftOmega, RightOmega)
        DelTheta = Omega[-1]*self.SampleTime
        self.Theta.append(Theta[-1] + DelTheta)

    def FindVx(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindTheta(LeftOmega, RightOmega)
        VxNew = (LeftOmega + RightOmega)*self.WheelRadius/2*m.cos(Theta[-1])
        self.Vx.append(VxNew)

    def FindVy(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindTheta(LeftOmega, RightOmega)
        Vy = (LeftOmega + RightOmega)*self.WheelRadius/2*m.sin(Theta[-1])
"""Debugging continues after here"""
    def FindX(self, LeftOmega: float, RightOmega: float) -> None:


    def FindDelY(self, LeftOmega: float, RightOmega: float) -> None:
        Vy = FindVy(LeftOmega, RightOmega)
