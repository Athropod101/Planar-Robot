from matplotlib import pyplot as plt
import matplotlib.animation as ani
from dataclasses import dataclass
from Plotting.Primitives import *

@dataclass
class MosaicAnimation:
    t: list
    y_set: float

    def __post_init__(self):
        self.fig, self.ax = plt.subplot_mosaic([
            ['Map', 'Map', 'Errors'],
            ['Map', 'Map', 'Speeds'],
            ['Map', 'Map', 'Voltages']],
            layout = "constrained")
        self.fig.suptitle("Robot Runtime Animation", fontsize = 16, fontweight = "bold")
        self.Line = [None] * 8
        self.Pose = PoseText(self.ax['Map'], ds.Position(0, 0, 0))

    def BuildMap(self, x, y) -> None:
        self.Line[0] = MapFrame(self.ax['Map'], x, y, self.y_set)
        self.x, self.y = x, y

    def BuildMarker(self, θ) -> None:
        self.Line[1] = Marker(self.ax['Map'], θ[0], self.x[0], self.y[0])
        self.θ = θ

    def BuildErrors(self, y_e, θ_e) -> None:
        self.Line[2], self.Line[3] = DualPlotFrame(self.ax['Errors'], self.t, y_e, θ_e, 
                      Title = "Errors vs Time",
                      ylabel = "Error (m or rad)",
                      legendlabels = [' $y_{E}$',  '$\\theta_{E}$'],
                      )
        self.y_e, self.θ_e = y_e, θ_e

    def BuildSpeeds(self, V_left, V_right, Vlims) -> None:
        self.Line[4], self.Line[5] = DualPlotFrame(self.ax['Speeds'], self.t, V_left, V_right,
                      Title = "Wheel Speeds vs Time",
                      ylabel = "Wheel Speed (m/s)",
                      legendlabels = ['$V_{L}$', '$V_{R}$'],
                      bounds = Vlims,
                      )
        self.V_left, self.V_right = V_left, V_right

    def BuildVolts(self, Volt_left, Volt_right, Vlims) -> None:
        self.Line[6], self.Line[7] = DualPlotFrame(self.ax['Voltages'], self.t, Volt_left, Volt_right,
                      Title = "Voltages vs Time",
                      ylabel = "Voltage (V)",
                      legendlabels = [r'$V_{L}$', r'$V_{R}$'],
                      bounds = Vlims,
                      )
        self.Volt_left, self.Volt_right = Volt_left, Volt_right

    def _Update(self, frame):
        self.Line[0].set_ydata(self.y[:frame])
        self.Line[0].set_xdata(self.x[:frame])
        self.Line[0].set_color("black")

        self.Line[1].set_ydata([])
        self.Line[1].set_xdata([])
        self.Line[1], = self.ax['Map'].plot(
                self.x[frame],
                self.y[frame],
                marker = (3, 0, (degrees(self.θ[frame]) + 30)),
                markersize = 15,
                linestyle = '-',
                color = 'cyan',
                mec = 'black')

        ydata = (
                None,
                None,
                [self.y_e[:frame]],
                [self.θ_e[:frame]],
                [self.V_left[:frame]],
                [self.V_right[:frame]],
                [self.Volt_left[:frame]],
                [self.Volt_right[:frame]],
                )
        for i, null in enumerate(self.Line):
            if i > 1:
                self.Line[i].set_ydata(ydata[i])
                self.Line[i].set_xdata(self.t[:frame])

        self.Pose.set_text(ds.Position(self.θ[frame], self.x[frame], self.y[frame]).Pose)

    def Animate(self) -> ani.FuncAnimation:
        frames = len(self.t)
        interval = self.t[-1] / frames * 1000
        animation = ani.FuncAnimation(
                fig = self.fig,
                func = self._Update,
                frames = frames,
                interval = interval,
                )
        return animation
