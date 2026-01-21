from sensors import Sensor
from motor import Motor
from control import Control
from kinematics import Kinematics
import numpy as np
import time

SampleTime = 0.1

MotorData = {
    'Torque'    : 0.15,     # Nm
    'Resistance': 0.9470,# Ohm
    'MotorConst': 0.2604, # V/rad
    'MaxVoltage': 6,        # V
    'MinVoltage': 3         # V
    }

RobotData = {
    'WheelRadius' : 0.05, # m
    'Differential': 0.1  # m
    }

InitialPosition = np.array([
    [0],
    [10],
    [0]
    ])

SensorData = {
    'NoiseMean': 0, # rad/s
    'NoiseDev': 0.1 # percentage
    }

PIDConstants = {
    'P': 1.5,
    'I': 0.5,
    'D': 0.5
    }

SetVoltage = 5
SetPoint = 0

RobotMotion = Kinematics(RobotData, InitialPosition, SampleTime)

LeftMotor = Motor(MotorData)
RightMotor = Motor(MotorData)

Sensor = Sensor(SensorData)

Controller = Control(LeftMotor.MotorControl, RobotMotion.KinematicControl, SetVoltage, PIDConstants, SetPoint, SampleTime, InitialPosition)

NewPos = InitialPosition
i = 0
while Controller.Error > 0.0001:
    V = Controller.FindVoltages(NewPos[1].item())
    IdealLeftOmega = LeftMotor.WriteVoltage(V[0])
    IdealRightOmega = RightMotor.WriteVoltage(V[1])
    LeftOmega = Sensor.AddNoise(IdealLeftOmega)
    RightOmega = Sensor.AddNoise(IdealRightOmega)
    RobotMotion.FindKinematics(LeftOmega, RightOmega)
    NewPos = RobotMotion.ReturnPositionVector()
    NewPos = NewPos.PositionVector
    NewPose = RobotMotion.ReturnPose()

    print("\r" f'Error: {Controller.Error} m\n', end="")
    print("\r" "=============================\n", end="")
    time.sleep(SampleTime)
    i += 1

print(
    f"The robot converged on the set point after:\n"
    f"{i} iterations.\n"
    f"{i*SampleTime} seconds. \n"
    )
