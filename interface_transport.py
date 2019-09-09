from wrapped_mqtt import MqttCustom


class TransportInterface:
    def __init__(self):
        pass

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
            return 26
        if "KW" in observationSource:
            return True

    def set_control(self, value, destination):
        print("{value} is sent to {destination}".format(value, destination))
