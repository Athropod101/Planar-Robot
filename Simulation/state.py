'''Simple class meant for logging all sim data per iteration. Isolated for cleaner code.'''
import etc.data_structures as ds
from dataclasses import dataclass
import Systems as sys
import Simulation as sim

@dataclass
class State:
    Data: ds.SimulationData
    Robot: sys.robot.Robot
    Motor: sys.motor.Motor
    Controller: sim.control.Control

    def __post_init__(self):
        self.θ = [self.Controller.Position.θ]
        self.y = [self.Controller.Position.y]
        self.y_e = [self.Controller.y_e]
        self.θ_e = [self.Controller.θ_e]
        self.x, self.V_left, self.V_right, self.Speed_left, self.Speed_right, self.t, self.i = ([0] for _ in range(7))
    def log(self, Position: ds.Position, Errors: list[float], Voltages: dict[float], Wheel_Speeds: dict[float]) -> None:
        self.i.append(self.i[-1] + 1)
        self.θ.append(Position.θ)
        self.x.append(Position.x)
        self.y.append(Position.y)
        self.y_e.append(Errors[0])
        self.θ_e.append(Errors[1])
        self.V_left.append(Voltages["Left"])
        self.V_right.append(Voltages["Right"])
        self.Speed_left.append(Wheel_Speeds["Left"])
        self.Speed_right.append(Wheel_Speeds["Right"])
        self.t.append(self.i[-1] * self.Data.δt)
