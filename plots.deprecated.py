import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from math import pi, degrees
import pandas as pd

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

    # Control
    SetPoint  : float = 0
    V_set     : float = 6
    SetOmega  : float = 200*3.14/180

    # Motor
    MinVoltage : float = 3

    def _BuildAxis(self, Axes, title, ylabel, labels = '', yline = 0, yticks = [0, 1]):
        Axes.axhline(
                y = yline,
                color = 'k',
                linestyle = '--',
                alpha = 0.5
                )
        Axes.set_ylabel(ylabel)
        Axes.set_xlabel("Time (s)")
        Axes.set_title(title)
        Axes.grid(True)
        Axes.margins(x = 0, y = 0.1)
        Axes.set_yticks(yticks)
        Axes.tick_params('y', rotation = 90)
        #Axes.legend(labels) 
        if labels != '':
            Axes.legend(
                    labels, 
                    fontsize = 'small',
                    handlelength = 0.1,
                    )

    def Build(self):
        fig = plt.figure(layout = "constrained", figsize = [10, 6])
        fig.suptitle("Robot Graphs")
        
        gs = GridSpec(3, 3, figure = fig)
        Map = fig.add_subplot(gs[0:3, 0:2])
        Err = fig.add_subplot(gs[0, 2])
        Ome = fig.add_subplot(gs[1, 2])
        Vol = fig.add_subplot(gs[2, 2])

        Map.plot(self.X, self.Y, color = 'black')
        Map.plot(self.X[0], self.Y[0], marker = (3, 0, (degrees(self.U[0]) + 4)), markersize = 15, linestyle = '-', color = 'cyan', mec = 'black')
        Err.plot(
                self.t, self.yE,
                self.t, self.uE
                )
        Ome.plot(
                self.t, self.OMEGALEFT,
                self.t, self.OMEGARIGHT
                )
        Vol.plot(
                self.t, self.VLEFT,
                self.t, self.VRIGHT
                )

        # Building the Axes
        ErrorLabels = [
                ' $y_{E}$\n(m)',
                '  $\\theta_{E}$\n(rad)'
                ]
        if abs(min(self.yE)) > abs(max(self.yE)):
            ErrorTicks = [min(self.yE), 0]
        else:
            ErrorTicks = [0, max(self.yE)]
        self._BuildAxis(
                        Err, 
                        "Errors vs Time",
                        "Error",
                        ErrorLabels,
                        yticks = ErrorTicks
                        )

        OmegaLabels = [
                r'$\omega_{L}$',
                r'$\omega_{R}$'
                ]
        OmegaTicks = [min(self.OMEGALEFT + self.OMEGARIGHT), self.SetOmega]
        self._BuildAxis(
                        Ome,
                        "Angular Velocities vs Time",
                        "Angular Velocity (rpm)",
                        OmegaLabels,
                        yline = self.SetOmega,
                        yticks = OmegaTicks
                        )

        VoltLabels = [
                r'$V_{L}$',
                r'$V_{R}$'
                ]
        VoltTicks = [self.MinVoltage, self.V_set]
        self._BuildAxis(
                        Vol,
                        "Voltage vs Time",
                        "Voltage (V)",
                        VoltLabels,
                        yline = self.MinVoltage,
                        yticks = VoltTicks
                        )
        self._BuildAxis(
                        Map,
                        "Robot Position",
                        "y-Position (m)",
                        yline = self.SetPoint
                        )

        # Building Map
        Map.set_xlabel("x-Position (m)")
        Map.grid(False)
        Map.margins(x = 0.05)
        Map.set_xticks([self.X[0], self.X[-1]])
        Map.set_yticks([self.Y[0], self.SetPoint])


        plt.show()
        plt.savefig('Robot Data.svg')
