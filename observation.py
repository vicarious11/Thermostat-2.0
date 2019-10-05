class Observation:
    def __init__(self, interface, observationSettings):
        self.observationSettings = observationSettings
        self.transportInterface = interface["transport"]
        self.configInterface = interface["config"]
        self.temperatureSource = self.observationSettings["temperature"][
            "formula"]
        self.ahuObservationSource = self.observationSettings["ahu"][
            "stateExpression"]
        self.ahuStatus = None
        self.previousAhuStatus = None
        self.temperature = None

    def get_verify_observation(self):
        self.ahuStatus = self.transportInterface.get_observation(
            self.ahuObservationSource)
        self.temperature = self.transportInterface.get_observation(
            self.temperatureSource)
        # : ahuStatus from false to true
        if self.previousAhuStatus == False and self.ahuStatus == True:
            observationCode = -2

        # : minimum position
        elif self.ahuStatus == False:
            observationCode = 0

        # : emergency position
        elif (self.ahuStatus == None) or (self.temperature == None):
            observationCode = -1
        else:
            observationCode = 1

        self.previousAhuStatus = self.ahuStatus
        return observationCode, self.temperature
