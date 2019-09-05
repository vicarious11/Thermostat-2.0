class TransportInterface:
    def get_setpoint(self):
        pass

    def get_offset(self):
        pass

    def get_observation(self, observationSource):
        pass

    def set_control(self, value, destination):
        print("{value} is sent to {destination}".format(value, destination))
