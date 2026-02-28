import numpy as np
from dataclasses import dataclass
from motor import Motor
from data_structures import SensorData, MotorData

@dataclass
class Sensor:
    Data: SensorData
    Motor: Motor

    def AddNoise(self) -> None:
        μ, σ_mult = self.Data.μ, self.Data.σ_mult
        for key, ω in self.Motor.ω.items():
            σ = ω * σ_mult / 100 # It's a percentile what else do you want?
            self.Motor.ω[key] = ω + np.random.normal(μ, σ)

'''Testing'''
def main() -> None:
    sensordata = SensorData(0, 5)
    print(f"Mean : {sensordata.μ}\nSTDev: {sensordata.σ_mult}")
    motordata = Motor(MotorData())
    test = Sensor(sensordata, motordata)
    test.Motor.WriteVoltage({"Left": 5, "Right": 4})

    for i in range(5):
        ω = {k: f"{v:.2f}" for k, v in test.Motor.ω.items()}
        print(f"Omega: {ω} rad/s")
        test.AddNoise()

if __name__ == "__main__":
    main()
