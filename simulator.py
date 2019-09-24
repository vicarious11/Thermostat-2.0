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

    def build(self):
        for controlName, output in self.output.items():
            for timePoint, outputValue in output.items():
                plt.plot(timePoint, outputValue, label=controlName)
        for timePoint, observation in self.observation.items():
            plt.plot(timePoint, observation, label=observation)
        plt.xlabel('Time')
        plt.ylabel('Values of Parameters')
        plt.title('Simulation Of PID 2.0')
        plt.legend()
        plt.show()
