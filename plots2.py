import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from math import pi, degrees
import pandas as pd
import matplotlib.animation as ani

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

    def _update(self, frame):
        print(type(self.Map.lines))
        print(type(self.yEr))
        self.Path.set_xdata(self.X[:frame])
        self.Path.set_ydata(self.Y[:frame])
        self.Bot.set_xdata(self.X[:frame])
        self.Bot.set_ydata(self.Y[:frame])
        AxList = [self.yEr, self.uEr, self.OmeLeft, self.OmeRight, self.VolLeft, self.VolRight]
        AxYData = np.array([
            [self.yE],
            [self.uE],
            [self.OMEGALEFT],
            [self.OMEGARIGHT],
            [self.VLEFT],
            [self.VRIGHT]
            ])
        for i in range(len(AxList)):
            AxList[i].set_xdata(self.t[:frame])
            AxList[i].set_ydata(AxYData[i, :frame])
        return (AxList)


    def Build(self):
        fig = plt.figure(layout = "constrained", figsize = [10, 6])
        fig.suptitle("Robot Graphs")
        
        gs = GridSpec(3, 3, figure = fig)
        self.Map = fig.add_subplot(gs[0:3, 0:2])
        self.Err = fig.add_subplot(gs[0, 2])
        self.Ome = fig.add_subplot(gs[1, 2])
        self.Vol = fig.add_subplot(gs[2, 2])

        self.Map.plot(self.X[0], self.Y[0], color = 'black')
        self.Map.plot(self.X[0], self.Y[0], marker = (3, 0, (degrees(self.U[0]) + 4)), markersize = 15, linestyle = '-', color = 'cyan', mec = 'black')
        self.Path, self.Bot = self.Map.lines
        self.Err.plot(
                self.t[0], self.yE[0],
                self.t[0], self.uE[0]
                )
        self.yEr, self.uEr = self.Err.lines

        self.Ome.plot(
                self.t[0], self.OMEGALEFT[0],
                self.t[0], self.OMEGARIGHT[0]
                )
        self.OmeLeft, self.OmeRight = self.Ome.lines

        self.Vol.plot(
                self.t[0], self.VLEFT[0],
                self.t[0], self.VRIGHT[0]
                )
        self.VolLeft, self.VolRight = self.Vol.lines

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
                        self.Err, 
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
                        self.Ome,
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
                        self.Vol,
                        "Voltage vs Time",
                        "Voltage (V)",
                        VoltLabels,
                        yline = self.MinVoltage,
                        yticks = VoltTicks
                        )
        self._BuildAxis(
                        self.Map,
                        "Robot Position",
                        "y-Position (m)",
                        yline = self.SetPoint
                        )

        # Building Map
        self.Map.set_xlabel("x-Position (m)")
        self.Map.grid(False)
        self.Map.margins(x = 0.05)
        self.Map.set_xticks([self.X[0], self.X[-1]])
        self.Map.set_yticks([self.Y[0], self.SetPoint])

        print(fig.axes)
        Animation = ani.FuncAnimation(fig = fig, func = self._update, frames = len(self.X), interval = 30)

        plt.show()
        Animation.save('Plots.gif')


