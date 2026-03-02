import etc.data_structures as ds
from math import pi as π
import Systems.robot as r
import Systems.motor as m
import numpy as np
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Control:
    Robot: r.Robot
    Data: ds.ControllerData
    Sim: ds.SimulationData
    Position: ds.Position


    def __post_init__(self):
        self.FindError()
        if self.Data.V_set > self.Robot.Motor.Data.V_max:
            print(
                    f"Target voltage ({self.V_set} V) exceeds maximum allowable voltage ({self.V_max} V).\n"
                    f"Setting target voltage to maximum allowable voltage (V_set = {self.V_max} V).\n"
                    )
            self.V_set = self.V_max
        self.PID = self._PIDMake()

    def _PIDMake(self) -> Callable:
        V_set = self.Data.V_set
        V_min = self.Robot.Motor.Data.V_min
        θ_e_prev = self.θ_e
        Vei = 0
        kp, ki, kd = self.Data.kp, self.Data.ki, self.Data.kd
        δt = self.Sim.δt
        def PIDTune(θ_e: float) -> float:
            nonlocal Vei, θ_e_prev
            if θ_e * θ_e_prev <= 0: Vei = 0
            Vep = kp * θ_e
            Vei += ki * θ_e * δt
            Ved = kd * (θ_e - θ_e_prev) / δt
            θ_e_prev = θ_e # Logging last orientation error

            V_new = V_set - abs(Vep + Vei + Ved)
            V_new = V_new if V_new > V_min else V_min
            return V_new
        return PIDTune

    def FindVoltages(self) -> dict[float]:
        V_set = self.Data.V_set
        y = self.Position.y
        θ = self.Position.θ
        y_e = self.y_e
        θ_e = self.θ_e
        if θ_e <= 0:
            V = {"Right": self.PID(θ_e), "Left": V_set}
        else:
            V = {"Right": V_set, "Left": self.PID(θ_e)}
        return V

    def FindError(self) -> None:
        self.y_e = self.Data.y_set - self.Position.y 
        self.θ_e =  π / 2 * np.tanh(self.Data.kt *self.y_e) - self.Position.θ
        self.Error = np.sqrt(self.y_e**2 + self.θ_e**2)
    
def main() -> None:
    CD = ds.ControllerData()
    Robot = r.Robot(m.Motor(ds.MotorData()), ds.BodyData(), CD)
    Controller = Control(Robot, CD, ds.SimulationData(), ds.Position())
    print(Controller.FindVoltages())


if __name__ == "__main__":
    main()
