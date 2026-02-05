import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.animation as ani
from dataclasses import dataclass
import numpy as np
from math import degrees
from data_structures import Pose

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
        xdata = (
                self.x,
                self.y,
                )
        ydata = (
                self.y, self.y,
                self.yE, self.uE,
                self.OMEGALEFT, self.OMEGARIGHT,
                self.VLEFT, self.VRIGHT,
                )
        Axi = 0
        for i, null in enumerate(self.Lines):
            X = xdata[0] if i < 2 else xdata[1]
            Y = ydata[i]
            self.Lines[i], = Ax[int(Axi)].plot([], [])
            Axi += 1/2

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

    def _SetTicks(self, Ax):
        yticks = (
                sorted([0, self.y[0]]),
                sorted([0, self.yE[0]]),
                [min(self.OMEGALEFT + self.OMEGARIGHT), self.SetOmega],
                [self.MinVoltage, self.V_set],
                )
        xticks = (
                [self.x[0], self.x[-1]],
                [self.t[0], self.t[-1]],
                )
        for i, null in enumerate(Ax):
            Ax[i].set_yticks(yticks[i])
            Ax[i].tick_params('y', rotation = 90)
            Ax[i].set_xticks(xticks[i != 0])
            Ax[i].set_autoscale_on(True)
        Ax[0].set_xticks([self.x[0], self.x[-1]])

    def _SetTitles(self, Ax):
        titles = (
                "Robot Position",
                "Errors",
                "Angular Velocities (rpm)",
                "Voltages (V)",
                )
        for i, null in enumerate(Ax):
            Ax[i].set_title(titles[i])

    def _SetAxTitles(self, Ax):
        xtitles = (
                "x-Position (m)",
                "Time (s)",
                )
        ytitles = (
                "y-Position (m)",
                "Error",
                "Angular Velocity",
                "Voltage",
                )
        for i, null in enumerate(Ax):
            Ax[i].set_ylabel(ytitles[i])
            Ax[i].set_xlabel(xtitles[i != 0])

    def _SetLegends(self, Ax):
        legends = (
               [' $y_{E}$\n(m)','  $\\theta_{E}$\n(rad)'],
               [r'$\omega_{L}$', r'$\omega_{R}$'],
               [r'$V_{L}$', r'$V_{R}$'],
               )
        for i, null in enumerate(Ax):
            if i == 0: continue
            Ax[i].legend(
                    labels = legends[i - 1],
                    fontsize = 'small',
                    handlelength = 0.1,
                    loc = 'center right',
                    )

    def _SetMargins(self, Ax):
        '''This is manual code cause I'm tired of margins'''
        Ax[0].set_xlim(left = -0.25)
        if self.yE[0] < 0:
            ybot = self.yE[0]
            ytop = 0.25 * self.yE[0]
        else:
            ybot = -0.25 * self.yE[0]
            ytop = self.yE[0]
        Ax[1].set_ylim(bottom = ybot, top = ytop)
        Ax[3].set_ylim(top = self.V_set * 1.05)

    def _Update(self, frame):
        self.Lines[0].set_ydata(self.y[:frame])
        self.Lines[0].set_xdata(self.x[:frame])
        self.Lines[0].set_color("black")

        self.Lines[1].set_ydata([])
        self.Lines[1].set_xdata([])
        self.Lines[1], = self.Ax[0].plot(
                self.x[frame],
                self.y[frame],
                marker = (3, 0, (degrees(self.U[frame]) + 30)),
                markersize = 15,
                linestyle = '-',
                color = 'cyan',
                mec = 'black')

        ydata = (
                None,
                None,
                [self.yE[:frame]],
                [self.uE[:frame]],
                [self.OMEGALEFT[:frame]],
                [self.OMEGARIGHT[:frame]],
                [self.VLEFT[:frame]],
                [self.VRIGHT[:frame]],
                )
        for i, null in enumerate(self.Lines):
            if i > 1:
                self.Lines[i].set_ydata(ydata[i])
                self.Lines[i].set_xdata(self.t[:frame])

        NewPose = Pose(self.U[frame], self.x[frame], self.y[frame])
        self.Pose.set_text(NewPose.__repr__())

    def _PoseText(self, Ax):
        PoseArray = Pose(self.U[0], self.x[0], self.y[0])
        self.Pose = Ax[0].text(
                x = 0.975,
                y = 0.5,
                s = PoseArray.__repr__(),
                transform = Ax[0].transAxes,
                ha = 'right',
                va = 'center',
                )

        

    def Build(self):
        self._BuildFig()
        self._BuildGridSpec(self.fig)
        self._BuildAxes(self.fig, self.gs)
        self._BuildLines(self.Ax)
        self._BuildYLines(self.Ax)
        self._SetTicks(self.Ax)
        self._SetTitles(self.Ax)
        self._SetAxTitles(self.Ax)
        self._SetLegends(self.Ax)
        self._SetMargins(self.Ax)
        self._PoseText(self.Ax)

        anim = ani.FuncAnimation(
                fig = self.fig,
                func = self._Update,
                frames = len(self.t),
                )

        plt.show()
        anim.save('GIFs/Plot.gif', writer = 'pillow')
