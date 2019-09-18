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
            temperature = None

        # : minimum position
        elif self.ahuStatus == False:
            observationCode = 0
            temperature = None

        # : emergency position
        elif (self.ahuStatus is None) or (self.temperature is None):
            observationCode = -1
            temperature = None
        else:
            observationCode = 1
            temperature = self.temperature

        self.previousAhuStatus = self.ahuStatus
        return observationCode, temperature
