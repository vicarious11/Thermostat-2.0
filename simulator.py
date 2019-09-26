import matplotlib.pyplot as plt


class Simulator:
    def __init__(self):
        self.timeSeries = []

        # : {"actuator" : { 199222:89, 199223:90 }, "vfd" : []}
        self.output = {"vfd": {}, "actuator": {}}

        # : {1999092 : 25, 19999095 : 26}
        self.observation = {}

    def save_time_x_axis(self, point):
        self.timeSeries.append(point)

    def save_output(self, controlName, timePoint, output):
        self.output[controlName][timePoint] = output

    def save_observation(self, timePoint, observation):
        self.observation[timePoint] = observation

    def make_plottable_output(self):
        controlOutput = {}
        for controlName, output in self.output.items():
            controlOutput[controlName] = {}
            for timePoint in self.timeSeries:
                controlOutput[controlName][timePoint] = 0
            for timePoint, outputValue in output.items():
                controlOutput[controlName][timePoint] = outputValue
            for timePoint, outputValue in controlOutput[controlName].items():
                if outputValue != 0:
                    currentOutput = outputValue
                else:
                    try:
                        controlOutput[controlName][timePoint] = currentOutput
                    except UnboundLocalError:
                        controlOutput[controlName][timePoint] = 0
        return controlOutput

    def build(self):
        fig, ax1 = plt.subplots()
        color = {"actuator": "tab:red", "vfd": "tab:green"}
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('Controller Positions', color="tab:olive")
        ax1.tick_params(axis='y', labelcolor="tab:olive")
        controlOutput = self.make_plottable_output()

        for controlName, output in controlOutput.items():
            timeSeries = []
            outputForPlot = []
            for timePoint, outputValue in output.items():
                if outputValue != 0:
                    timeSeries.append(timePoint)
                    outputForPlot.append(outputValue)
            ax1.plot(timeSeries,
                     outputForPlot,
                     label=controlName,
                     color=color[controlName])
        plt.legend()

        observationTimeSeries = [timePoint for timePoint in self.observation]
        observationValue = [output for _, output in self.observation.items()]
        ax2 = ax1.twinx()
        ax2.set_ylabel('Observation', color="tab:olive")
        ax2.plot(observationTimeSeries, observationValue, label="observation")
        ax2.tick_params(axis='y', labelcolor="tab:olive")
        plt.title('Simulation Of PID 2.0')
        plt.legend()
        plt.show()
