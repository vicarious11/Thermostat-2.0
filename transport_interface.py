class TransportInterface:
    def __init__(self):
        self.setpoint = 25
        self.offset = 0.5

    def send(self, message, destination):
        print(f"{message} --->>> {destination}")
