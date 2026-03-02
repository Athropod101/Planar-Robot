# Standard Library
import os
import shutil

# External Libraries
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import yaml
import ffmpeg

# Project Libraries
import etc.data_structures as ds
import Systems as sys
import Simulation as sim
from Plotting import plots
from Plotting import Primitives
from Plotting import Animation

def main() -> int:
    # Parsing config
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    TestName = config["Test Name"]
    Position = ds.Position(**config["Initial Position"])
    MotorData = ds.MotorData(**config["Motor Data"])
    ControllerData = ds.ControllerData(**config["Controller Data"])
    SensorData = ds.SensorData(**config["Sensor Data"])
    BodyData = ds.BodyData(**config["Body Data"])
    SimulationData = ds.SimulationData(**config["Simulation Data"])

    # System Initailization
    Motor = sys.motor.Motor(MotorData)
    Sensor = sys.sensors.Sensor(SensorData, Motor)
    Robot = sys.robot.Robot(Motor, BodyData, ControllerData)

    frac = Motor.System.T_s / SimulationData.δt * 100
    if frac > 15:
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

    # Checking robot voltages
    V_t = [u / Robot.γ for u in Robot.x_t_sat[1]]
    vifg, vax = plt.subplots()
    vax.plot(Robot.t_sat.squeeze(), V_t)
    print(Robot.γ)
    plt.show()

    # Saving Files
    os.makedirs(f"Results/{TestName}", exist_ok = True)
    shutil.copy("config.yaml", f"Results/{TestName}/config.yaml")
    figures = [Motor.Figure, Robot.Figure_sat, Robot.Figure_small]
    figTitles = ["Motor System Analysis", "Robot Saturated Error Analysis", "Robot Small Error Analysis"]

    for i in range(len(figures)):
        figures[i].savefig(f"Results/{TestName}/{figTitles[i]}.svg", bbox_inches = 'tight')

    fps = len(State.t) / State.t[-1]
    animation.save(f"Results/{TestName}/Animation.gif", writer='ffmpeg', fps = fps)


if __name__ == "__main__":
    main()
