from wrapped_mqtt import MqttCustom


class TransportInterface:
    def __init__(self):
        with open("./temp_data.txt") as f:
            tempData = f.readlines()
        self.tempData = (temp.split("\n")[0] for temp in tempData)
        self.previousControls = {}
        self.alertCount = 0

    @classmethod
    def from_mqtt(cls, clientId, on_connect_func_ref, on_disconnect_func_ref,
                  on_message_func_ref):
        selfObj = cls()
        selfObj.channel = MqttCustom(on_connect_func_ref,
                                     on_message_func_ref,
                                     on_disconnect_func_ref,
                                     credentials={"mqttclientid": clientId})
        return selfObj

    def get_setpoint(self):
        pass

    def get_offset(self):
        pass

    def get_observation(self, observationSource):
        if "temp" in observationSource:
            return float(next(self.tempData))
        if "KW" in observationSource:
            return True

    def set_control(self, value, destination):
        previousValue = self.previousControls.get(destination, None)
        if previousValue != value:
            print("{} is sent to {}".format(value, destination))
            self.previousControls[destination] = value
        else:
            pass

    def send_alert(self, alertType):
        if alertType == "timetoachieve":
            print("setpoint could not be met",
                  "please change the setpoint",
                  sep="\n\n")
        self.alertCount += 1
