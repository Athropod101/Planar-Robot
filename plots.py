import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass

import matplotlib
matplotlib.use('kitcat')

@dataclass
class Plot:

    t         : list[float]
    X         : list[float]
    Y         : list[float]
    U         : list[float]
    yE        : list[float]
    uE        : list[float]
    OMEGA     : list[float]
    OMEGALEFT : list[float]
    OMEGARIGHT: list[float]
    VLEFT     : list[float]
    VRIGHT    : list[float]

    def _BuildAxis(self, Axes, title, ylabel):
        Y = 0 if ylabel != "Voltage (V)" else 3
        Axes.axhline(
                y = Y,
                color = 'k',
                linestyle = '--',
                alpha = 0.5
                )
        Axes.set_ylabel(ylabel)
        Axes.set_xlabel("Time (s)")
        Axes.set_title(title)
        Axes.grid(True)
        Axes.margins(x = 0, y = 0.1)

    def Build(self):
        fig = plt.figure(layout = "constrained")
        fig.suptitle("Robot Graphs")
        
        gs = GridSpec(3, 4, figure = fig)
        Map = fig.add_subplot(gs[0:2, 0:2])
        Err = fig.add_subplot(gs[0, 2:4])
        Ome = fig.add_subplot(gs[1, 2:4])
        Vol = fig.add_subplot(gs[2, 2:4])
        SRD = fig.add_subplot(gs[2, 0])
        DRD = fig.add_subplot(gs[2, 1])

        Map.plot(self.X, self.Y)
        Err.plot(
                self.t, self.yE,
                self.t, self.uE
                )
        Ome.plot(
                self.t, self.OMEGA,
                self.t, self.OMEGALEFT,
                self.t, self.OMEGARIGHT
                )
        Vol.plot(
                self.t, self.VLEFT,
                self.t, self.VRIGHT
                )

        # Building the Axes
        self._BuildAxis(Err, "Errors vs Time", "Error")
        self._BuildAxis(Ome, "Angular Velocities vs Time", "Angular Velocity (rpm)")
        self._BuildAxis(Vol, "Voltage vs Time", "Voltage (V)")
        self._BuildAxis(Map, "Robot Position", "y-Position (m)")

        # Building Map
        Map.set_xlabel("x-Position (m)")
        Map.grid(False)
        Map.margins(x = 0.05)
        Map.set_xticks([self.X[0], self.X[-1]])

        plt.show()
        plt.savefig('Robot Data.png')
