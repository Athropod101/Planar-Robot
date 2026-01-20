from sensor import Sensor
from motor import Motor
from kinematics import Kinematics

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

SensorData = {
        'NoiseMean': 0 # rad/s
        'NoiseDev': 10 # percentage
        }


LeftMotor = Motor(MotorData)
RightMotor = Motor(MotorData)

LeftSensor = Sensor(SensorData)
RightSensor = Sensor(SensorData)
''' IMPORTANT: kinematics must be instantiated before sensor!'''
