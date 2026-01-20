# Assumptions
1. Robot Dynamics already taken into account as part of the input. This assumption simplifies:
    * Defining motor parameters to voltage and angular velocity ranges as well.
    * Defining error as a percentile deviation and a standard deviation. 
2. The robot begins at:
    * $x = 0$
    * $y = y_{o}$
    * $\theta  = \theta_{o}$
3. The error noise processed by sensor.py accounts for all extraneous variables in addition to motor uncertainties. 
1. Sensor noise can be approximated as gausian noise with a given mean and a standard deviation proportional to the robot's current velocity.
1. Torque on the motor is constant.

# Appendix
This portion of README.md contains documentation for each file of the program. It need not be read to understand how to run the program. 


|File Name|Description|
|:---:|:---:|
|control.py|Sets up and operates the control system for the robot|
|data_structures.py|Interprets established parameters to define the key data structures of the robot.|
|kinematics.py|Generates the kinematic data for the robot from sensor inputs.|
|manim.py|Animates the robot's kinematics.|
|motor.py|Receives voltage input and outputs the motor's speeds.|
|plots.py|Generates plots for all of the robot's data.|
|sensors.py|Reads the motor's angular velocities and incorporates gausean noise to them to simulate realistic data.|
|simulator.py|Main code. Parameters are set up here, and all outputs are displayed here.|

Modeline vim: tabstop=4
