import etc.data_structures as ds
import Systems as sys
import Simulation as sim
import numpy as np
from Plotting import plots
from Plotting import Primitives
from Plotting import Animation
import matplotlib.pyplot as plt

def main(yamlfile) -> int:
    # NOTE: Replace this segment with yaml reading later
    MotorData = ds.MotorData()
    ControllerData = ds.ControllerData()
    SensorData = ds.SensorData()
    BodyData = ds.BodyData()
    SimulationData = ds.SimulationData()
    Position = ds.Position()

    # System Initailization
    Motor = sys.motor.Motor(MotorData)
    Sensor = sys.sensors.Sensor(SensorData, Motor)
    Robot = sys.robot.Robot(Motor, BodyData, ControllerData)

    frac = Motor.System.T_s / SimulationData.δt * 100
    if frac > 10000:
        print(
                f"WARNING: Motor response time fraction is {frac:.2f}% > 10.00% !!! Simulation will be innacurate.\n"
                f"If you would like to continue the simulation anyway, write \"continue\".\nOtherwise, the simulation will be aborted.")
        if input() != "continue": return 1
        else: print("Continuing simulation...")

    # Simulation Initialization
    Controller = sim.control.Control(Robot, ControllerData, SimulationData, Position)
    Motion = sim.kinematics.Kinematics(SimulationData, Robot, Position)
    State = sim.state.State(SimulationData, Robot, Motor, Controller)
    
    while (Controller.Error > SimulationData.TOL) and (State.i[-1] < SimulationData.i_max):
        V = Controller.FindVoltages()
        Motor.WriteVoltage(V)
        Sensor.AddNoise()
        R, R_dot = Motion.FindKinematics()
        Controller.FindError()
        Speed = {side: BodyData.r * w for side, w in Motor.ω.items()}
        State.log(R, [Controller.y_e, Controller.θ_e], V, Speed)

    if State.i[-1] == SimulationData.i_max: print(f"ERROR: Simulation did not converge within {SimulationData.i_max} iterations.")

    anim = Animation.MosaicAnimation(State.t, ControllerData.y_set)
    anim.BuildMap(State.x, State.y)
    anim.BuildMarker(State.θ)
    anim.BuildErrors(State.y_e, State.θ_e)
    anim.BuildSpeeds(State.Speed_left, State.Speed_right, [Robot.Speed(MotorData.V_min), Robot.Speed(ControllerData.V_set)])
    anim.BuildVolts(State.V_left, State.V_right, [MotorData.V_min, MotorData.V_max])

    animation = anim.Animate()
    plt.show()

if __name__ == "__main__":
    main([])
