from wrapped_mqtt import MqttCustom


class TransportInterface:
    def __init__(self):
        with open("./sim_data.txt") as f:
            data = f.readlines()
        self.tempData = (tempAhu.split("\n")[0].split(",")[0]
                         for tempAhu in data)
        self.kwData = (tempAhu.split("\n")[0].split(",")[1]
                       for tempAhu in data)
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
            temp = next(self.tempData)
            if temp == "None":
                return None
            else:
                return float(temp)
        if "KW" in observationSource:
            return eval(next(self.kwData))

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
