class Observation:
    def __init__(self, interface, observationSettings):
        self.transportInterface = interface["transport"]
        self.configInterface = interface["config"]
        self.temperatureSource = self.observationSettings["temperature"][
            "formula"]
        self.ahuObservationSource = self.observationSettings["ahu"][
            "stateExpression"]
        self.ahuStatus = None
        self.temperature = None

    def get_verify_observation(self):
        self.ahuStatus = self.transportInterface.get_observation(
            self.ahuObservationSource)
        self.temperature = self.transportInterface.get_observation(
            self.temperatureSource)

        # : minimum position
        if self.ahuStatus == False:
            observationCode = 0
            temperature = None

        # : emergency position
        elif (self.ahuStatus is None) or (self.temperature is None):
            observationCode = -1
            temperature = None
        else:
            observationCode = 1
            temperature = self.temperature

        return observationCode, temperature
