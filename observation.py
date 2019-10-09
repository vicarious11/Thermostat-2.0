class Observation:
    def __init__(self, state):
        self.state = state

    def verify_observation(self, ahuStatus, temperature):
        # : ahuStatus from false to true
        if self.state["previousAhuStatus"] == 0 and ahuStatus == True:
            observationCode = -2

        # : minimum position
        elif ahuStatus == False:
            observationCode = 0

        # : emergency position
        elif (ahuStatus is None) or (temperature is None):
            observationCode = -1
        else:
            observationCode = 1

        self.state["previousAhuStatus"] = int(ahuStatus)
        return observationCode, temperature
