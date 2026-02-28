import etc.data_structures as ds
import Systems as sys
import Simulation as sim

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
    Sensor = sys.sensors.Sensor(SensorData)
    Robot = sys.robot.Robot(Motor, BodyData, ControllerData)

    frac = Motor.T_s / SimulationData.δt * 100
    if frac > 10:
        print(
                f"WARNING: Motor response time fraction is {frac:.2f}% > 10.00% !!! Simulation will be innacurate."
                f"If you would like to continue the simulation anyway, write \"continue\", otherwise the simulation will be aborted.")
        if input() != "continue": return 1
        else: print("Continuing simulation...")

    # Simulation Initialization
    Controller = sim.control.Control(Robot, ControllerData, SimulationData, Position)
    Motion = sim.kinematics.Kinematics(SimulationData, Robot, Position)

    
