# Introduction
This repository contains the program files for a simple differential robot control simulator for an exam for the Polytechnic University of Puerto Rico's Automated Systems and Robotics 1 (ME-3082) course. This README contains usage instructions and an overview of the exam; greater detail can be found in [the repository's Report file](Report.html).

## Purpose
The purpose of this repository is to demonstrate the student's competence in several fields of the Mechanical Engineering bachelor's Robotics and Industrial Automation specialization, such as:
* Python programming (Specific to Robotics 1)
* Object-oriented programming (Specific to Robotics 1)
* Kinematic analysis
* DC motor mathematical modeling
* Control system design
* Gausian noise generation and handling

Additionally, the exam is meant to teach the student the principles behind ROS2's communication between programs by forcing them to declare the data structures that will be handled between modules.

# Usage
The only file meant to be used is [simulator.py](simulator.py), which is the main module responsible for communicating with all the other modules of the repository. If desired, the user may edit the following parameters in [simulator.py](simulator.py):
1. Sample Time
1. Motor:
    * Torque
    * Resistance
    * Motor Constant
    * Minimum Voltage
    * Maximum Voltage
1. Robot Geometry:
    * Wheel Radius
    * Differential (distance between wheels)
1. Sensor:
    * Mean Wheel Angular Velocity Noise
    * Standard Deviation of Angular Velocity
        * This value is entered as a multiplier of the current angular velocity, to better simulate road noise.
1. Initial Position:
    * $\theta_{o}$
    * $x_{o}$
    * $y_{o}$
1. Control Data:
    * PID Constants
        * Proportional
        * Integral
        * Derivative
    * Set Voltage
    * Set Point (y-coordinate)
1. Error Tolerance
1. Maximum Iterations

Once the user has entered their desired parameters, they may run [simulator.py](simulator.py) to run the simulation. The console will output the number of iterations (and time) to convergence. Convergence is determined by the error magnitude of the y-error and the $\theta$-error. A successful simulation will converge around $y = y_{set}$ and $\theta = 0^{\circ}$.

## Plots
[simulator.py](simulator.py) will generate an animation of the simulation and save it as [Plots.gif](GIFs/Plots.gif) in the [GIFs](GIFs/) directory. The animation contains plots of the robot's x-y trajectory, its y- and $\theta$-errors, its wheel angular velocities, and its motor voltages. 

Additionally, some other simulation results are saved in the same directory. Details are found in the [Report](Report.html).

# Assumptions
1. Motor torque is constant.
3. The noise processed by [sensor.py](sensor.py) accounts for all extraneous variables in addition to usual sensor noise. 
1. Actual sensor noise in need of filtering is negligible.
1. Sensor noise can be approximated as gausian noise with a given mean and a standard deviation proportional to the robot's wheel angular velocities.

# Modules
A brief overview of the modules and their purposes is tabularized below.


|Module|Description|
|:---:|:---:|
|[control.py](control.py)|Generates voltage corrections from a given position error.|
|[data_structures.py](data_structures.py)|Defines the intended data structures for communication between modules.|
|[kinematics.py](kinematics.py)|Generates kinematic data from a given noisy angular velocity.|
|[motor.py](motor.py)|Generates an ideal angular velocity from a given voltage.|
|[plots.py](plots.py)|Generates animated plots of the robot's main data.|
|[sensors.py](sensors.py)|Reads the motor's angular velocities and incorporates gausean noise to them to simulate realistic data.|
|[simulator.py](simulator.py)|Main code. Parameters are set up here, and all outputs are displayed here.|

# Personal Thoughts
Toning down on the formalism, this was an incredibly fun learning experience. It was my first time with a full blown multi-file project (or second, if you count configuring NeoVim's plugins)! My programming experience before this was almost entirely MatLab and Excel. With MatLab I mostly stuck to one file for the whole thing, occasionally using more files for ease of reading, but individually running them. For Excel have only ever done cell programming--no VBA. With Python, I had to completely restructure my way of thinking about programming, and I can happily say I have a bunch of cool new skills to show off for it! 

For the record, I think MatLab is *really* cool--way cooler than the Godless land that is numpy. I *did not* enjoy having to work with numpy's arrays; in fact, I don't think I actually used numpy for this exam outside of maybe a niche function or two. I've grown to really like a lot of Python's syntax and built-ins, but working math here is miserable (more on that later).

Regarding the structure of the project, I'd heavily appreciate suggestions on how to improve my code. I'll say that I've gotten a lot better since version 0 thanks to a Heat Transfer 2 project that I decided to write Python code for. I've noticed Python has a lot of syntax conventions as well as libraries meant to help write more structured code. 

# Future Plans
This is a project I'd like to iterate future versions for. Now that I know how to go about it, I should be able to improve it way more quickly than I built it at first. First and foremost I'd like to implement my newfound knowledge from my Heat Transfer project to better structure this project
(especially data_structures; that module is kinda useless in its current state and not a good example of a communication protocol.)
As a sneak peak, my Robotics 1 final will be this same exam, but built with ROS2, so that'll naturally be implemented here.

Regarding visualization, I'm actually quite unhappy with how the plots turned out. I'd originally wanted to try a Manim animation, but time constraints led me back to Matplotlib due to its familiarity with MatLab's plotting (Matplotlib is super cool btw, unlike Numpy. It has really good documentation too.) I originally wanted to include a text display of the robot's specs and dynamically-changing data. Displaying this text in a pretty way turned out to be way too frustrating to pursue, so I settled for just the SE(2) pose slapped on top of the map. 
Additionally, the plotting structure is currently bugged for negative errors, so that needs to be fixed.

As for the biggest hope for this project, I'd like to write it in Julia. Maybe not all of it; perhaps some pieces of it are better suited for Python. However, I want to run all the math of this with Julia in order to learn that language. I just..genuinely abhor doing math in Python. It's clearly not built for it, and Numpy feels more like a bandaid than anything. I crave the seamlessness of MatLab math.
