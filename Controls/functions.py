import numpy as np
from numpy.linalg import eig, inv
import scipy as sp
from scipy.linalg import expm
from math import pi as π
from typing import Callable, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod

def IncorrectResponse(Exception):
    def __init__(self, message, code):
        self.code = code
        self.message = message
        super().__init__(message)

@dataclass
class SecondOrderStateSpace(ABC):
    A   : np.array

    ''' Public '''
    def SolveResponse(self, Xo: np.array, B: np.array, U: np.array, Response: str = "Unit") -> np.array:
        if      Response == "Unit": return self._UnitResponse(Xo, B, U)
        elif    Response == "Ramp": return self._RampResponse(Xo, B, U)
        else    : raise IncorrectResponse("Improper input response given for analysis. Simulator supports only \"Unit\" and \"Ramp\" responses.", 1)

    ''' Private '''
    def _UnitResponse(self, Xo: np.array, B: np.array, U: np.array) -> np.array:
        A, t = self.A, self.t
        AiBU = inv(A) @ B * U

        xt = np.empty([2, t.shape[0]])
        for i, _ in enumerate(t):
            XT = expm(A * t[i]) @ (Xo + AiBU) - AiBU
            xt[:, i] = XT.flatten()
        return xt

    def _RampResponse(self, Xo: np.array, B: np.array, U: float) -> np.array:
        A, t, δt = self.A, self.t, self.δt

        xt = np.empty([2, t.shape[0]])
        xt[:, 0] = Xo.squeeze()
        I = np.zeros((2,))
        beq = B[1][0]

        for i in range(0, t.shape[0] - 1):
            B[1][0] = beq(t[i])
            arg = ( A @ xt[:, i] + (B.squeeze() * U))
            I +=  arg.astype(float) * δt
            xt[:, i + 1] = I

        return xt

    def __post_init__(self):
        σ_d, ω_d    = self._FindPoles()
        ζ           = self._FindDampingRatio(σ_d, ω_d)
        ω_n         = self._FindNaturalFrequency(σ_d, ζ)
        T_s         = self._FindSettlingTime(σ_d)
        t, δt       = self._FindPlotRuntime(T_s)
        pOV         = self._FindOvershoot(ζ)
        T_p         = self._FindPeakTime(ω_d)


        self.t, self.δt = t, δt

    def _FindPoles(self) -> tuple[float] | tuple[np.array, float]:
        λ, _ = eig(self.A)
        σ_d = abs(λ.real)
        if σ_d[0] == σ_d[1]: σ_d = σ_d[0]
        ω_d = abs(λ.imag[0])
        return σ_d, ω_d

    def _FindDampingRatio(self, σ: Union[float, np.array], ω: float = 0) -> float:
        if ω > 0: return np.sqrt( 1 / (ω/σ + 1) )
        else: return (σ[0] + σ[1]) / 2 / np.sqrt(σ[0] * σ[1])

    def _FindNaturalFrequency(self, σ: Union[float, np.array], ζ: float) -> float:
        if not isinstance(σ, np.ndarray) : return σ/ζ
        else                    : return np.sqrt(σ[0] * σ[1])

    def _FindSettlingTime(self, σ: Union[float, np.array]) -> float:
        if isinstance(σ, np.ndarray): σ = min(σ)
        return 4/σ

    def _FindPlotRuntime(self, T_s: float) -> tuple[float, np.array]:
        δt = T_s / 300                          # Yeah, this is a magic number. Cry about it. I decide what the precision is.
        return np.arange(0, 1.5 * T_s, δt), δt  # Yes, there's another magic number here.

    def _FindOvershoot(self, ζ: float) -> float:
        if ζ < 1: return 100 * np.exp(-ζ * π / np.sqrt(1 - ζ**2))
        else: return 0

    def _FindPeakTime(self, ω: float) -> float | None:
        if ω > 0: return π / ω
        else    : return None

def main() -> None:

    import data_structures as ds
    from matplotlib import pyplot as plt
    
    MData = ds.MotorData()

    BData = ds.BodyData()


    γ = 2 * BData.r / BData.l * MData.k / (MData.D * MData.R + MData.k**2)
    kp = 5
    ki = 10
    #ki = kp ** 2 * γ / 4 - 0.1

    A = np.array([
        [0  ,  1     ],
        [-ki * γ, -kp * γ],
        ])

    Response = "Ramp"
    uo = 0
    U = -0.5
    wo = 0
    Xo = np.array([[uo], [wo]])
    B = np.array([ [0], [lambda t: γ * (ki * t + kp)] ])
    B[1][0] = B[1][0] if Response == "Ramp" else γ * ki

    System = SecondOrderStateSpace(A)
    xt = System.SolveResponse(Xo, B, U, Response)
    mask = xt[0] > - π / 2
    xt = xt[:, mask]
    System.t = System.t[mask]

    fig, ax = plt.subplot_mosaic([['Theta', 'Voltage']])
    ax['Theta'].plot(System.t, xt[0])
    ax['Voltage'].plot(System.t, xt[1])
    plt.show()


if __name__ == "__main__":
    main()
