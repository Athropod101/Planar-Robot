from dataclasses import dataclass
from math import pi

@dataclass
class Motor:
    Torque     : float # Nm
    Resistance : float # Ohm
    MotorConst : float # Vs/rad
    MaxVoltage : float # V
    MinVoltage : float # V

    def __post_init__(self):
        self.b: float = self.Torque*self.Resistance/self.MotorConst**2
        self.m: float = 1/self.MotorConst
        self.dV_cap: float = self.MaxVoltage - self.MinVoltage
        self.MotorControl: dict[float] = {'m': self.m, 'V_max': self.MaxVoltage, 'V_min': self.MinVoltage}

    def __repr__(self) -> str:
        rep = (
                f"Slope      : {self.m:.4f} rad/Vs\n"
                f"Offset     : {self.b:.4f} rad/s\n"
                f"Max Voltage: {float(self.MaxVoltage):.4f} V\n"
                f"Min Voltage: {float(self.MinVoltage):.4f} V\n"
                )
        return rep

    def WriteVoltage(self, Voltage: float, rpm = False) -> float:
        V = Voltage if Voltage <= self.MaxVoltage else self.MaxVoltage
        Omega = (V*self.m - self.b) if Voltage >= self.MinVoltage else self.MinVoltage
        if rpm == True:
            Omega *= 30 / pi
        return Omega

'''Testing'''
def main() -> None:
    MotorData = {
            'Torque'    : 0.15,     # Nm
            'Resistance': 0.9470,# Ohm
            'MotorConst': 0.2604, # Vs/rad
            'MaxVoltage': 6,        # V
            'MinVoltage': 3         # V
            }

    MotorTest = Motor(**MotorData)

    print(MotorTest)
    print(f"{int(MotorTest.WriteVoltage(0)*30/3.14):3d} rpm")
    print(f"{int(MotorTest.WriteVoltage(2)*30/3.14):3d} rpm")
    print(f"{int(MotorTest.WriteVoltage(3)*30/3.14):3d} rpm")
    print(f"{int(MotorTest.WriteVoltage(5)*30/3.14):3d} rpm")
    print(f"{int(MotorTest.WriteVoltage(6)*30/3.14):3d} rpm")
    print(f"{int(MotorTest.WriteVoltage(7)*30/3.14):3d} rpm")

if __name__ == "__main__":
    main()
