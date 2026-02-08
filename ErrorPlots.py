import matplotlib.pyplot as plt
from dataclasses import dataclass, field

@dataclass
class ErrorPlots:
    Time: list[float] = field(default_factory = lambda: [0, 1])
    y: list[float] = field(default_factory = lambda: [0, 0.5])
    theta: list[float] = field(default_factory = lambda: [-0.5, 0])
    y_Error: dict[str, float] = field(default_factory = lambda:
            {"Net": [-0.5, 0.5], "PID": [-0.75, 0], "P": [-1, 0], "I": [-0.5, 0], "D": [.75, 0]})
    theta_Error: dict[str, float] = field(default_factory = lambda:
            {"Net": [-0.5, 0.5], "PID": [-0.75, 0], "P": [-1, 0], "I": [-0.5, 0], "D": [.75, 0]})
    y_set: float = 0
    theta_set: list[float] = field(default_factory = lambda: [0, 0.5])

    def __post_init__(self) -> None:
        ylabels = [
                "Position (m)",
                "Orientation (rad)",
                "Position Errors (m)",
                "Orientation Errors (rad)",
                ]
        suptitle = "Errors vs Time"
        color = ["Yellow", "Cyan"]
        errorcolor = ["Red", "Blue", "Orange", "Brown", "Purple"]
        legend = ["Net Error", "PID Error", "Proportional Error", "Integral Error", "Derivative Error"]
            
        self._BuildSubplot(suptitle)
        self._BuildAxes(ylabels)
        self._BuildDashLines()
        self._BuildPoseLines(color)
        self._BuildErrorLines(errorcolor)
        self._BuildErrorLegends(legend)
        plt.show()

    def _BuildSubplot(self, suptitle) -> None:
        self.fig, self.ax = plt.subplots(
                nrows = 2,
                ncols = 2,
                sharex = 'all',
                subplot_kw = {
                    'xlabel': 'Time (s)',
                    'xmargin': 0,
                    'xlim': [self.Time[0], self.Time[-1]],
                    },
                )
        self.fig.suptitle(suptitle)
        self.ax = self.ax.flat

    def _BuildAxes(self, ylabels) -> None:
        for i in range(4):
            self.ax[i].set_ylabel(ylabels[i])

    def _BuildPoseLines(self, color) -> None:
        ydata = [self.y, self.theta]
        PosePlot = [None] * 2
        for i in range(2):
            PosePlot[i] = self.ax[i].plot(self.Time, ydata[i], color = color[i])

    def _BuildErrorLines(self, errorcolor) -> None:
        Error = [self.y_Error, self.theta_Error]
        self.ErrorPlot = [[None] * 5,
                     [None] * 5]
        for i in range(2):
            for j, k in enumerate(Error[i].keys()):
                self.ErrorPlot[i][j], = self.ax[i + 2].plot(
                        self.Time, Error[i][k],
                        color = errorcolor[j],
                        )

    def _BuildErrorLegends(self, legend) -> None:
        for i in 2, 3:
            self.ax[i].legend(
                    handles = self.ErrorPlot[i - 2],
                    labels = legend,
                    fontsize = 'small',
                    loc = 'upper right',
                    )

    def _BuildDashLines(self) -> None:
        lineval = [
                self.y_set,
                self.theta_set,
                0,
                0,
                ]
        for i in range(4):
            if i != 1:
                self.ax[i].axhline(
                        y = lineval[i],
                        color = "black",
                        linestyle = '--',
                        alpha = 0.5,
                        zorder = 0,
                        linewidth = 0.5,
                        )
            else:
                self.ax[i].plot('Time', 'Error',
                        data = {'Time': self.Time, 'Error': lineval[i]}, 
                        color = "black",
                        linestyle = '--',
                        alpha = 0.5,
                        linewidth = 0.5,
                        )


def main() -> None:
    ErP = ErrorPlots()
    plt.show()

if __name__ == "__main__":
    main()
