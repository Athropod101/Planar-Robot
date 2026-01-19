class Motor:
    def __init__(self, MotorData):
        self.Torque = MotorData["Torque"]
        self.Resistance = MotorData["Resistance"]
        self.MotorConst = MotorData["MotorConst"]

    def __post_init__(self):
        b: float = Torque*Resistance/MotorConst**2
        m: float = 1/MotorConst

    def FindOmega(self, Voltage: float) -> float:
        return Voltage*self.m - self.b

    def FindVoltage(self, Omega: float) -> float:
        return (Omega + self.b)/self.m
