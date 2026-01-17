from dataclasses import dataclass

@dataclass
class Motor:
    Torque: float
    Resistance: float
    MotorConst: float

    b = Torque*Resistance/MotorConst**2
    m = 1/MotorConst

    def FindOmega(self, Voltage: float) -> float:
        return Voltage*self.m - self.b

    def FindVoltage(self, Omega: float) -> float:
        return (Omega + self.b)/self.m
