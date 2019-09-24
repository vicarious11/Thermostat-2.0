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
            timeSeries = []
            controlOutput = []
        fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel('time (s)')
	ax1.set_ylabel('Controller Positions', color = color)   
	for timePoint, outputValue in output.items():
                timeSeries.append(timePoint)
                controlOutput.append(outputValue)
		ax1.plot(timeSeries, controlOutput, label=controlName)
		ax1.tick_params(axis='y', labelcolor = color)

        observationTimeSeries = [timePoint for timePoint in self.observation]
        observationValue = [output for _, output in self.observation.items()]
	ax2 = ax1.twinx()
	color = 'tab:blue'
        ax2.set_ylabel('Observation', color = color)
	ax2.plot(observationTimeSeries, observationValue, label="observation")
        ax2.tick_params(axis= 'y', labelcolor = color)
        plt.title('Simulation Of PID 2.0')
        plt.legend()
        plt.show()
