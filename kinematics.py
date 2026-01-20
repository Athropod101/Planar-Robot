import data_structures as ds
mport numpy as np
import scipy as sc
import math as m

class Kinematics:
    def __init__(self, RobotData, InitialPosition, SampleTime):
        self.WheelRadius  = RobotData["WheelRadius"]
        self.Differential = RobotData["Differential"]
        self.SampleTime   = SampleTime
        
        self.Theta        = InitialPosition[0].item()
        self.y            = InitialPosition[1].item()

    def __post_init__(self):
        self.x:     float = 0
        self.Omega: float = 0
        self.Vy:    float = 0
        self.Vx:    float = 0
        self.KinematicControl: float = (self.WheelRadius*self.SampleTime)**2/self.Differential

    '''
    These methods are not meant to be executed individually but rather executed by the FindPosistion() method.
    These sub-methods are defined individually to help organize the code.
    '''
    def FindOmega(self, LeftOmega: float, RightOmega: float) -> None:
        self.Omega = 2*self.WheelRadius/self.Differential*(RightOmega - LeftOmega)

    def FindTheta(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindOmega(LeftOmega, RightOmega)
        DelTheta = self.Omega*self.SampleTime
        self.Theta = self.Theta + DelTheta

    def FindVelocities(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindTheta(LeftOmega, RightOmega)
        self.Vx = (RightOmega + LeftOmega)*self.WheelRadius/2*m.cos(self.Theta)
        self.Vy = self.Vx*m.tan(self.Theta)

    '''
    These are the methods that should actually be used by simulation.py.
    '''
    def FindKinematics(self, LeftOmega: float, RightOmega: float) -> None:
        self.FindVelocities(LeftOmega, RightOmega)
        self.x = self.Vx*self.SampleTime
        self.y = self.Vy*self.SampleTime

    def ReturnPositionVector(self) -> ds.PositionVector:
        return ds.PositionVector(self.Theta, self.y, self.x)

    def ReturnPose(self) -> ds.Pose:
        return ds.Pose(self.Theta, self.y, self.x)
    
def main() -> None:
    RobotData = {"WheelRadius" : 0.02, "Differential" : 0.1}
    InitialPosition = np.array([[0], [0], [0]])
    SampleTime = 1

    # Test at no Velocity Differential
    OL = 2
    OR = 2

    KinSample = Kinematics(RobotData, InitialPosition, SampleTime)
    KinSample.FindKinematics(OL, OR)
    print(KinSample.ReturnPositionVector())
    print(KinSample.ReturnPose())

    # Test at positive Velocity Differential
    OL = 2
    OR = 2.5

    KinSample = Kinematics(RobotData, InitialPosition, SampleTime)
    KinSample.FindKinematics(OL, OR)
    print(KinSample.ReturnPositionVector())
    print(KinSample.ReturnPose())

    # Test at negative Velocity Differential
    OL = 3
    OR = 2

    KinSample = Kinematics(RobotData, InitialPosition, SampleTime)
    KinSample.FindKinematics(OL, OR)
    print(KinSample.ReturnPositionVector())
    print(KinSample.ReturnPose())

if __name__ == "__main__":
    main()
