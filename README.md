# Version 1 of Planar Robot Simulator
The planar robot simulator has been heavily refactored to address some deficiencies if Version 0. The quick changelog is:

1. Added a config.yaml file as a frontend to the simulation; this is the only file the user needs to modify to tune the simulation to their liking.
2. Added pre-simulation code to verify system stability. Several plots will be generated to present the user the dynamic system data of the motor, the motor with feedback, and the differential robot.
3. The simulation will now warn the user if the motor's transient response is not negligible compared to the simulation step time.
4. The simulation gif is now a 1:1 time representation of the robot.
5. Plots, gifs, and configurations are saved in Results/

For more details, see the "V1 Presentation"/ directory. 
