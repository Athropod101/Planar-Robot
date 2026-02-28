import etc.data_structures as ds
import Systems.robot as r
import Systems.motor as m
import numpy as np
from dataclasses import dataclass, field

@dataclass
class Kinematics:
    Sim: ds.SimulationData
    Robot: r.Robot
    Position: ds.Position

    def _FindOmega(self) -> float:
        return self.Robot.β * (self.Robot.Motor.ω["Right"] - self.Robot.Motor.ω["Left"])

    def _FindTheta(self, ω: float) -> float:
        θ = self.Position.θ + ω * self.Sim.δt
        self.Position.θ = np.arctan2(np.sin(θ), np.cos(θ))
        return self.Position.θ

    def _FindVelocities(self, θ: float) -> tuple[float]:
        Vx = self.Robot.Vel_set * np.cos(θ)
        Vy = self.Robot.Vel_set * np.sin(θ)
        return Vx, Vy

    def _FindPosition(self, Vx: float, Vy: float) -> tuple[float]:
        self.Position.x += Vx * self.Sim.δt
        self.Position.y += Vy * self.Sim.δt
        return self.Position.x, self.Position.y

    def FindKinematics(self) -> tuple[ds.Position]:
        ω = self._FindOmega()
        θ = self._FindTheta(ω)
        Vx, Vy = self._FindVelocities(θ)
        x, y = self._FindPosition(Vx, Vy)
        return ds.Position(θ, x, y), ds.Position(ω, Vx, Vy)

def main() -> None:
    Sim = ds.SimulationData()
    Robot = r.Robot(m.Motor(ds.MotorData()), ds.BodyData(), ds.ControllerData())
    Position = ds.Position()

    Robot.Motor.WriteVoltage({"Left": 4, "Right": 5})
    kinematics = Kinematics(Sim, Robot, Position)

    while True:
        R, V = kinematics.FindKinematics()
        print("Position")
        print(R.Vector)
        print("Velocity")
        print(V.Vector)
        if input() == "exit": break
    pass

if __name__ == "__main__":
    main()
