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
