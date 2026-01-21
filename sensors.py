import numpy as np
class Sensor:
    def __init__(self, SensorData):
        self.NoiseMean = SensorData["NoiseMean"]
        self.NoiseDev = SensorData["NoiseDev"]

    def __repr__(self):
        rep = f'Mean: {self.NoiseMean}\nDev : {self.NoiseDev}'
        return rep

    def AddNoise(self, Omega) -> float:
        SDev = Omega*self.NoiseDev
        NoisyOmega = Omega + np.random.normal(self.NoiseMean, SDev)
        return NoisyOmega

''' Testing '''
def main() -> None:
    SensorData = {'NoiseMean': 0, 'NoiseDev': 0.5}
    Test = Sensor(SensorData)
    print(Test)

    for i in range(10):
        print(Test.AddNoise(1))

if __name__ == "__main__":
    main()
