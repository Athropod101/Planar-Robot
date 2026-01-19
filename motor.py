class Motor:
    def __init__(self, MotorData):
        self.Torque = MotorData["Torque"]
        self.Resistance = MotorData["Resistance"]
        self.MotorConst = MotorData["MotorConst"]
        self.MaxVoltage = MotorData["MaxVoltage"]
        self.MinVoltage = MotorData["MinVoltage"]

    def __post_init__(self):
        b: float = Torque*Resistance/MotorConst**2
        m: float = 1/MotorConst

    def WriteVoltage(self, Voltage: float) -> float:
        V = Voltage if Voltage <= self.MaxVoltage else self.MaxVoltage
        Omega = (V*self.m - self.b) if Voltage >= self.MinVoltage else 0
        return Omega

    def FindVoltage(self, Omega: float) -> float:
        V = (Omega + self.b)/self.m
        return V

def main() -> None:
    
