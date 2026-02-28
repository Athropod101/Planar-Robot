import etc.data_structures as ds
import Systems as sys
import Simulation as sim
import numpy as np
from Plotting import plots
from Plotting import Primitives
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
        R, R_dot = Motion.FindKinematics()
        Controller.FindError()
        State.log(R, [Controller.y_e, Controller.θ_e], V, Motor.ω)
        #print(State.i[-1])
        #input("")

    if State.i[-1] == SimulationData.i_max: print(f"ERROR: Simulation did not converge within {SimulationData.i_max} iterations.")

    Plot = plots.Plot(State.t, State.x, State.y, State.θ, State.y_e, State.θ_e, [], State.ω_left, State.ω_right, State.V_left, State.V_right, Controller.Data.y_set, Controller.Data.V_set, Motor.SetSpeed(Controller.Data.V_set), Motor.Data.V_min)
    testfig, ax = plt.subplots()
    #Primitives.DualPlotMargins(ax, State.t, State.y_e, State.θ_e, "Voltage", "Voltage", ["Left Voltage", "Right Voltage"])
    Line =Primitives.MapMargins(ax, State.x, State.y, ControllerData.y_set)
    Line.set_xdata(State.x)
    Line.set_ydata(State.y)
    plt.show()

if __name__ == "__main__":
    main([])
