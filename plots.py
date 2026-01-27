import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.animation as ani
from dataclasses import dataclass
from math import pi, degrees

import matplotlib
matplotlib.use('kitcat')

@dataclass
class Plot:
    t         : list[float]
    x         : list[float]
    y         : list[float]
    U         : list[float]
    yE        : list[float]
    uE        : list[float]
    OMEGA     : list[float]
    OMEGALEFT : list[float]
    OMEGARIGHT: list[float]
    VLEFT     : list[float]
    VRIGHT    : list[float]

    # Control
    SetPoint  : float = 0
    V_set     : float = 6
    SetOmega  : float = 200

    # Motor
    MinVoltage : float = 3

    def _BuildFig(self):
        self.fig = plt.figure(
                layout = "constrained",
                figsize = [10, 6],
                )
        self.fig.suptitle("Robot Graphs")

    def _BuildGridSpec(self, fig):
        self.gs = GridSpec(3, 3, figure = fig)

    def _BuildAxes(self, fig, gs):
        Grids = (
                gs[:, :2],   # Map
                gs[0, 2],       # Error
                gs[1, 2],       # Omega
                gs[2, 2],       # Voltage
                )
        fig = fig
        self.Ax = [None] * len(Grids)
        for i, Grid in enumerate(Grids):
            self.Ax[i] = fig.add_subplot(Grid)

    def _BuildLines(self, Ax):
        self.Lines = [None] * 2 * len(Ax)
        Axi = 0
        for i, null in enumerate(self.Lines):
            self.Lines[i], = Ax[int(Axi)].plot([], [])
            Axi += 1/2
        self.Lines[0].color = "black"

    def _BuildYLines(self, Ax):
        ylines = (
                self.SetPoint,      # Map
                0,                  # Error
                self.SetOmega,      # Omega
                self.MinVoltage,    # Voltage
                )
        for i, null in enumerate(Ax):
            Ax[i].axhline(
                    y = ylines[i],
                    color = "black",
                    linestyle = '--',
                    alpha = 0.5,
                    zorder = 0,
                    )

    def _SetLims(self, Ax):
        pass

    def _SetTicks(self, Ax):
        pass

    def _SetTitles(self, Ax):
        pass

    def _SetYLabels(self, Ax):
        pass

    def _SetXLabels(self, Ax):
        pass

    def _Update(self, frame):
        pass

    def _SetMisc(self, Ax):
        pass




    def Build(self):
        self._BuildFig()
        self._BuildGridSpec(self.fig)
        self._BuildAxes(self.fig, self.gs)
        self._BuildLines(self.Ax)
        self._BuildYLines(self.Ax)

        plt.show()
