'''
This class is responsible for computing the full robot system's dynamics. It exists OUTSIDE of the simulation loop, calculating loop constants and checking whether or not the system will stably converge. Its public outputs are:

    1. Constants: Computation of variables like γ for particular system analysis.
    2. Stability: Determination of whether or not the robot will actually converge during simulation. Instability will raise an error, ending the simulation early.
    3. Plots    : Setting up the plot mosaic for...
        a. The unit response of x, y, θ as well as the pole plot around small angles. 
        b. The unit response of the motor feedback system as well as the pole plot at the saturated error region.
'''

import numpy as np
from motor import Motor
from dataclasses import dataclass
import data_structures as ds
from math import pi as π

@dataclass
class Robot:
    Motor: Motor
    Body: ds.BodyData
    Control: ds.ControllerData

    def __post_init__(self):
        # Internal Attribute Declaration
        self.kt = -π/2
        self.ks = 1

        # Constant Computing
        self.β = 2 * self.Body.r / self.Body.l
        self.γ = self.Motor.α * self.β

        # Stability Computing
        self.A = _computeA()
        self.B = _computeB()

    def _computeA() -> np.array:
        Vset, ks
        return ([
