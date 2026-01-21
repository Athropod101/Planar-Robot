class Motor:
    def __init__(self, MotorData):
        self.Torque = MotorData["Torque"]
        self.Resistance = MotorData["Resistance"]
        self.MotorConst = MotorData["MotorConst"]
        self.MaxVoltage = MotorData["MaxVoltage"]
        self.MinVoltage = MotorData["MinVoltage"]

        # Post-Init
        self.b: float = self.Torque*self.Resistance/self.MotorConst**2
        self.m: float = 1/self.MotorConst
        self.MotorControl: list[float] = [self.m, self.b]

    def WriteVoltage(self, Voltage: float) -> float:
        V = Voltage if Voltage <= self.MaxVoltage else self.MaxVoltage
        Omega = (V*self.m - self.b) if Voltage >= self.MinVoltage else 0
        return Omega

def main() -> None:

    MotorData = {
            'Torque'    : 0.15,     # Nm
            'Resistance': 0.9470,# Ohm
            'MotorConst': 0.2604, # Vs/rad
            'MaxVoltage': 6,        # V
            'MinVoltage': 3         # V
            }

    MotorTest = Motor(MotorData)

    print(MotorTest.WriteVoltage(0)*30/3.14)
    print(MotorTest.WriteVoltage(2)*30/3.14)
    print(MotorTest.WriteVoltage(3)*30/3.14)
    print(MotorTest.WriteVoltage(5)*30/3.14)
    print(MotorTest.WriteVoltage(6)*30/3.14)
    print(MotorTest.WriteVoltage(7)*30/3.14)

if __name__ == "__main__":
    main()
