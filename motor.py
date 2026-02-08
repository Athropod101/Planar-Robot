from dataclasses import dataclass, field
from math import pi as π
from data_structures import MotorData

class VoltageOverload(Exception):
    pass

@dataclass
class Motor:
    Data: MotorData = field(default_factory = lambda: MotorData())

    def __post_init__(self):
        self.Data.b: float = self.Data.T *self.Data.R / self.Data.k ** 2
        self.Data.m: float = 1 / self.Data.k

    def WriteVoltage(self, Voltages: dict[float], rpm: bool = False) -> dict[float]:
        b = self.Data.b
        m = self.Data.m
        V = [Voltages["Left"], Voltages["Right"]]
        V_max = self.Data.V_max
        V_min = self.Data.V_min
        CONV = 30 / π if rpm == True else 1

        for i, null in enumerate(V):
            V[i] = V[i] if V[i] >= V_min else b / m

        if max(V) > self.Data.V_max:
            raise VoltageOverload(
                    f"\nWARNING!!! Written voltage greater than maximum allowable motor voltage!\n\n"
                    f"Motor has been damaged. Shutting down simulation..."
                    )

        ω = list(map(lambda v: (m * v - b) * CONV, V))

        return dict(zip(["Left", "Right"], ω))


'''Testing'''
def main() -> None:
    TestMotor = Motor()
    print(TestMotor)

    def Display(Vl, Vr, RPM = False) -> None:
        ω = {k: round(v, 2) for k, v in TestMotor.WriteVoltage({"Left": Vl, "Right": Vr}, RPM).items()}
        print(ω)

    print("\nTesting Write Voltage:")
    Display(5, 5)
    print("\nTesting Below Minimum Voltage:")
    Display(2, 3)
    Display(3, 2)
    print("\nTesting RPM:")
    Display(5, 5, True)
    print("\nTesting Above Maximum Voltage:")
    Display(7, 3)

if __name__ == "__main__":
    main()
