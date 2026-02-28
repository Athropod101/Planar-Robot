from sensors import Sensor
from motor import Motor
from control import Control
from kinematics import Kinematics
from plots import Plot
import numpy as np
import time
import math as m
from ErrorPlots import ErrorPlots
import matplotlib.pyplot as plt
import matplotlib

SampleTime = 0.001

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

InitialPosition = {
    'Theta': 0,
    'x'    : 0,
    'y'    : 5
    }

SensorData = {
    'Mean': 0,# rad/s
    'Dev': 0  # Multiplier
    }

PIDConstants = {
    'kP': 1,
    'kI': 0,
    'kD': 0
    }

SetVoltage = 6
SetPoint = 0

Tolerance = 0.01
MaxIter = 1e6

''' USER EDITING NOT INTENDED BELOW THIS LINE'''

RobotMotion = Kinematics(SampleTime, **RobotData, **InitialPosition)

LeftMotor = Motor(**MotorData)
RightMotor = Motor(**MotorData)

Sensor = Sensor(**SensorData)

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
y_val = NewPos['y']
u_val = NewPos['Theta']
V = Controller.FindVoltages(y_val, u_val)

t         : list[float] = []
X         : list[float] = []
Y         : list[float] = []
U         : list[float] = []
yE        : list[float] = []
uE        : list[float] = []
OMEGA     : list[float] = []
OMEGALEFT : list[float] = []
OMEGARIGHT: list[float] = []
VLEFT     : list[float] = []
VRIGHT    : list[float] = []
while m.sqrt(Controller.yError**2 + Controller.ThetaError**2) > Tolerance:
    if i > MaxIter:
        break

    '''Motor Data'''
    LeftOmega = LeftMotor.WriteVoltage(V['Left Voltage'])
    RightOmega = RightMotor.WriteVoltage(V['Right Voltage'])

    '''Sensor Data'''
    NoisyLeft = Sensor.AddNoise(LeftOmega)
    NoisyRight = Sensor.AddNoise(RightOmega)

    '''Kinematic Data'''
    RobotMotion.FindKinematics(NoisyLeft, NoisyRight)

    '''Logging Data'''
    t.append(i*SampleTime)
    X.append(RobotMotion.x)
    Y.append(RobotMotion.y)
    U.append(RobotMotion.Theta)
    yE.append(Controller.yError)
    uE.append(Controller.ThetaError)
    OMEGA.append(RobotMotion.Omega * 30 / m.pi)
    OMEGALEFT.append(NoisyLeft * 30 / m.pi)
    OMEGARIGHT.append(NoisyRight * 30 / m.pi)
    VLEFT.append(V['Left Voltage'])
    VRIGHT.append(V['Right Voltage'])

    '''Logging ErrorPlot Data'''
    uEPID.append(Controller.TunedError)
    uEP.append(Controller.PError)
    uEI.append(Controller.IError)
    uED.append(Controller.DError)
    theta_set.append(Controller.Theta_set)


    '''Setup Next Iteration'''
    #time.sleep(SampleTime)
    i += 1

    '''Control Data'''
    V = Controller.FindVoltages(RobotMotion.y, RobotMotion.Theta)

print(
    f"The robot converged on the set point after:\n"
    f"{i} iterations.\n"
    f"{i*SampleTime} seconds. \n"
    )

SetOmega = LeftMotor.WriteVoltage(SetVoltage, rpm = True)
#Plot = Plot(t, X, Y, U, yE, uE, OMEGA, OMEGALEFT, OMEGARIGHT, VLEFT, VRIGHT, SetPoint, SetVoltage, SetOmega, LeftMotor.MinVoltage)
#Plot.Build()
