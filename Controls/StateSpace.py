'''
Purpose: To create a State Space abstract class and its nth-order subclasses.

These classes are instantiated with a matrix A, to determine stability and poles immediately. They will also incorporate public methods to compute transient responses for a given input B(t) * U(t).
'''

import numpy as np
from numpy.linalg import eig, inv
import scipy as sp
from scipy.linalg import expm
from math import pi as π
from typing import Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class StateSpace(ABC):
    A       : np.ndarray
    Order   : int           = field(init = False)
    Stable  : bool          = field(init = False)
    T_s     : float | None  = field(init = False)
    σ_d     : np.ndarray    = field(init = False)
    ω_d     : np.ndarray    = field(init = False)

    def __post_init__(self) -> None:
        self.Order = self.A.shape[0]
        self.Stable = self._CheckStability()
        self.T_s = None if not self.Stable else 4 / abs(min(self.σ_d))

    def _CheckStability(self) -> bool:
        # Importing Attributes
        A = self.A
        
        # Computing stability
        λ, _ = eig(A)
        self.σ_d = λ.real
        self.ω_d = λ.imag

        return True if (self.σ_d <= 0).any() else False

    def StepResponse(self, Xo: np.ndarray, B: np.ndarray, U: np.ndarray) -> np.ndarray:
        # Importing Attributes
        A = self.A
        N = self.Order

        if self.Stable:
            t_max = 1.5 * self.T_s
            i_max = 300
            δt = t_max / i_max

            # Computing the integral
            AiBU = inv(A) @ B @ U
            xt = np.empty((N, i_max), dtype = float)
            t = np.empty((1, i_max), dtype = float)
            for i in range(i_max):
                t[0, i] = δt * i
                XT = expm(A * t[0, i]) @ (Xo + AiBU) - AiBU
                xt[:, i] = XT.flatten()
        # NOTE missing code for unstable case here.
        return xt, t

@dataclass
class SOStateSpace(StateSpace):
    Underdamped: bool  = field(init = False)
    ζ          : float = field(init = False)
    ω_n        : float = field(init = False)
    T_p        : float = field(init = False)
    pOV        : float = field(init = False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.ω_d = np.sort(self.ω_d)
        self.Underdamped = True if (self.ω_d != 0).any() else False
        self.ζ = self._computeDampingRatio()
        self.ω_n = np.sqrt(self.σ_d[0]**2 + self.ω_d[0]**2) if self.Underdamped else np.np.sqrt(σ_d.prod())
        if self.Underdamped:
            self.T_p = π / abs(self.ω_d[0])
            self.pOV = 100 * np.exp(-self.ζ * π / np.sqrt(1 - self.ζ**2))

    def _computeDampingRatio(self) -> float:
        Underdamped = self.Underdamped
        σ_d = abs(self.σ_d)
        if Underdamped:
            ζ = np.sqrt(1 / (self.ω_d[0] / self.σ_d[0] + 1))
        else:
            ζ = sum(σ_d) / 2 / np.sqrt(σ_d.prod())

        return ζ

def main():
    import data_structures as ds
    Data = ds.MotorData()
    R, L, k, J, D = Data.R, Data.L, Data.k, Data.J, Data.D
    A = np.array([
        [-R/L, -k/L],
        [ k/J, -D/J],
        ])
    Motor = SOStateSpace(A)
    B = np.array([[1/L], [0]])
    U = np.array([[1]])
    Xo = np.zeros((2,1), dtype=float)
    xt, t = Motor.StepResponse(Xo, B, U)
    #print(Motor.T_p)
    T = (np.where(t >= Motor.T_p))
    print(T[1])
    print(xt[1][T[1][0]])

if __name__ == "__main__":
    main()
