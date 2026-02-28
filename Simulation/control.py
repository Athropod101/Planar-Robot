import etc.data_structures as ds
import Systems.robot as r
import Systems.motor as m
import numpy as np
from dataclasses import dataclass, field


@dataclass
class Control:
    Robot: r.Robot
    Data: ds.ControllerData
    Sim: ds.SimulationData
    Position: ds.Position

    θ_e_prev: float = field(init = False)
    Vei: float = field(init = False)

    def __post_init__(self):
        self.Vei = 0
        self.θ_e_prev = 0
        self.dV_cap    : float = self.Data.V_set - self.Robot.Motor.Data.V_min
        if self.Data.V_set > self.Robot.Motor.Data.V_max:
            print(
                    f"Target voltage ({self.V_set} V) exceeds maximum allowable voltage ({self.V_max} V).\n"
                    f"Setting target voltage to maximum allowable voltage (V_set = {self.V_max} V).\n"
                    )
            self.V_set = self.V_max
            self.dV_cap = self.V_max - self.V_min

    def _PIDTune(self, θ_e: float) -> float:
        kp, ki, kd = self.Data.kp, self.Data.ki, self.Data.kd
        δt = self.Sim.δt
        θ_e_prev = self.θ_e_prev
        Vep = kp * θ_e
        self.Vei += ki * θ_e * δt
        Ved = kd * (θ_e - θ_e_prev) / δt
        return Vep + self.Vei + Ved

    def _InterpretVoltageError(self, V_e: float) -> dict[float]:
        V_set = self.Data.V_set
        if V_e < 0:
            Vnew = V_set + V_e if V_set + V_e > self.dV_cap else self.dV_cap
            V = {"Left": V_set, "Right": Vnew}
        else:
            Vnew = V_set - V_e if V_set - V_e > self.dV_cap else self.dV_cap
            V = {"Left": Vnew, "Right": V_set}
        return V

    def FindVoltages(self) -> dict[float]:
        y = self.Position.y
        θ = self.Position.θ
        y_e = y - self.Data.y_set
        θ_e = θ - np.tanh(-y_e)
        V_e = self._PIDTune(θ_e)
        return self._InterpretVoltageError(V_e)
    
def main() -> None:
    CD = ds.ControllerData()
    Robot = r.Robot(m.Motor(ds.MotorData()), ds.BodyData(), CD)
    Controller = Control(Robot, CD, ds.SimulationData(), ds.Position())

    print(Controller.FindVoltages())

if __name__ == "__main__":
    main()
