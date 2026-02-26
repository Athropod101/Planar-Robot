from dataclasses import dataclass, field
import numpy as np
from matplotlib import pyplot as plt

@dataclass
class MosaicMotor:
    t: np.array
    x: np.array
    σ: np.array
    ω: np.array
    LeftTable: dict
    RightTable: dict
    Suptitle: str
    xTitle: str
    xLabel: str

    def __post_init__(self):
        fig, ax = plt.subplot_mosaic([
            ['x(t)', 'Poles'],
            ['Left', 'Right']],
            layout = "constrained")
        fig.suptitle(Suptitle, fontsize = 16, fontweight = "bold")
