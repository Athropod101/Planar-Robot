from sensor import Sensor
from motor import Motor
from kinematics import Kinematics

SampleTime = 0.1

MotorData = {
        'Torque'    : 0.15,     # Nm
        'Resistance': 0.0001139,# Ohm
        'MotorConst': 0.002856, # V/rad
        'MaxVoltage': 3,        # V
        'MinVoltage': 6         # V
        }

RobotData = {
        'WheelRadius' : 0.05 # m
        'Differential': 0.1  # m
        }

InitialPosition = np.array([
    [0],
    [0],
    [0]
    ]

SensorData = {
        'NoiseMean': 0 # rad/s
        'NoiseDev': 10 # percentage
        }

RobotMotion = Kinematics(RoboData, InitialPosition, SampleTime)

LeftMotor = Motor(MotorData)
RightMotor = Motor(MotorData)

LeftSensor = Sensor(SensorData)
RightSensor = Sensor(SensorData)
''' IMPORTANT: kinematics must be instantiated before sensor!'''
