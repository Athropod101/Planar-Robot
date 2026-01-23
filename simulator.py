from sensors import Sensor
from motor import Motor
from control import Control
from kinematics import Kinematics
import numpy as np
import time
import math as m

SampleTime = 0.1

MotorData = {
    'Torque'    : 0.15,     # Nm
    'Resistance': 0.9470,# Ohm
    'MotorConst': 0.2604, # V/rad
    'MaxVoltage': 6,        # V
    'MinVoltage': 3         # V
    }

RobotData = {
    'WheelRadius' : 0.02, # m
    'Differential': 0.1  # m
    }

InitialPosition = np.array([
    [0],
    [9],
    [0]
    ])

SensorData = {
    'Mean': 0, # rad/s
    'Dev': 0.0 # percentage
    }

PIDConstants = {
    'kP': 1,
    'kI': 0.5,
    'kD': 0.5
    }

SetVoltage = 5
SetPoint = 0

RobotMotion = Kinematics(RobotData, InitialPosition, SampleTime)

LeftMotor = Motor(**MotorData)
RightMotor = Motor(**MotorData)

Sensor = Sensor(**SensorData)

# Controller = Control(LeftMotor.MotorControl, RobotMotion.KinematicControl, SetVoltage, PIDConstants, SetPoint, SampleTime, InitialPosition)

Controller = Control(
        SetPoint,
        SetVoltage,
        SampleTime,
        RobotMotion.DWR,
        **PIDConstants,
        **LeftMotor.MotorControl,
        )

NewPos = InitialPosition
i = 0
y_val = NewPos[1].item()
u_val = NewPos[0].item()
V = Controller.FindVoltages(y_val, u_val)
while abs(Controller.yError + Controller.ThetaError) > 0.01:
    '''Error Data'''
    print(
            f"[ C O N T R O L ]\n"
            f"Set Point    : {float(Controller.y_set):5.2f} m\n"
            f"y-Error      : {float(Controller.yError):5.2f} m\n"
            f"Theta-Error  : {float(Controller.ThetaError):5.2f} rad\n"
            f"Error Sum    : {float(Controller.yError + Controller.ThetaError):5.2f}\n"
            f"Left Voltage : {float(V['Left Voltage']):5.2f} V\n"
            f"Right Voltage: {float(V['Right Voltage']):5.2f} V\n"
            )
    
    '''Motor Data'''
    LeftOmega = LeftMotor.WriteVoltage(V['Left Voltage'])
    RightOmega = RightMotor.WriteVoltage(V['Right Voltage'])

    print(
            f"[ M O T O R ]\n"
            f"Left Omega   : {float(LeftOmega):5.2f} rad/s\n"
            f"Right Omega  : {float(RightOmega):5.2f} rad/s\n"
            )

    '''Sensor Data'''
    NoisyLeft = Sensor.AddNoise(LeftOmega)
    NoisyRight = Sensor.AddNoise(RightOmega)

    print(
            f"[ S E N S O R ]\n"
            f"Left Omega   : {float(NoisyLeft):5.2f} rad/s\n"
            f"Right Omega  : {float(NoisyRight):5.2f} rad/s\n"
            )

    '''Kinematic Data'''
    RobotMotion.FindKinematics(NoisyLeft, NoisyRight)

    print(
            f"[ K I N E M A T I C S ]\n"
            f"Omega        : {float(RobotMotion.Omega):5.2f} rad/s\n"
            f"Speed        : {float(m.sqrt(RobotMotion.Vx**2 + RobotMotion.Vy**2)):5.2f} m/s\n"
            f"Position (y) : {float(RobotMotion.y):5.2f} m\n"
            f"Orientation  : {float(RobotMotion.Theta):5.2f} rad\n"
            )

    time.sleep(1)
    print("===[NEXT ITERATION]===")

    '''Control Data'''
    V = Controller.FindVoltages(RobotMotion.y, RobotMotion.Theta)



print(
    f"The robot converged on the set point after:\n"
    f"{i} iterations.\n"
    f"{i*SampleTime} seconds. \n"
    )
