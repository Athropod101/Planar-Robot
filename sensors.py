import numpy as np
from dataclasses import dataclass

@dataclass
class Sensor:
    Mean: float # rad/s
    Dev : float # %

    def __repr__(self):
        rep = (
                f'Mean             :  {float(self.Mean):4.2f} rad/s\n'
                f'Percent Deviation: {float(self.Dev):4.2f} %\n'
                )
        return rep

    def AddNoise(self, Omega) -> float:
        SDev = Omega*self.Dev/100
        NoisyOmega = Omega + np.random.normal(self.Mean, SDev)
        return NoisyOmega

'''Testing'''
def main() -> None:
    SensorData = {'Mean': 0, 'Dev': 50}
    Test = Sensor(**SensorData)
    print(Test)

    for i in range(5):
        Omega = i
        NoisyOmega = Test.AddNoise(Omega)
        print(f"Omega: {Omega} rad/s -> {NoisyOmega:1.4f} rad/s")

if __name__ == "__main__":
    main()
