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
        print("graph --> ")


sim = Simulator()
for i in range(100):
    sim.save_time_x_axis(i)
    sim.save_observation(i, i + 0.5)
    sim.save_output("actuator", i, i**2)
    sim.save_output("vfd", i, i**2.5)



x1 = []
x2 = []
x3 = []

for i in sim.output['vfd']:
	x1.append(sim.output['vfd'][i])

for i in sim.output['actuator']:
	x2.append(sim.output['actuator'][i])

for i in sim.observation:
	x3.append(sim.observation[i])
		
plt.plot(sim.timeSeries, x2, label = "actuatorOutput")
plt.plot(sim.timeSeries, x1, label = "vfdFeedback")
plt.plot(sim.timeSeries, x3, label = "observation")
plt.xlabel('Time in minutes')
plt.ylabel('Values of Parameters')
plt.title('Simulation Of PID 2.0')
plt.legend()
plt.show() 
