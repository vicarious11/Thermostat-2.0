from observation import Observation
import time
from control import Control
from interface_config import ConfigInterface
from interface_transport import TransportInterface
from mqtt_callback_mechanism import CallbackMechanism


@CallbackMechanism.wrap_on_connect
def on_connect(client):
    client.subscribe("command/thermostat/setpoint")
    print("***********connected********")


@CallbackMechanism.wrap_on_disconnect
def on_disconnect(client):
    print("disconnected")


@CallbackMechanism.wrap_on_message
def on_message(topic, payload):
    print("message received ", topic, payload, sep="---")


class ApplicationFlow:
    def __init__(self, interface, appSettings):
        self.interface = interface
        self.configInterface = interface["config"]
        self.transportInterface = interface["transport"]
        self.callbackInterface = interface["callback"]
        self.appSettings = appSettings
        self.appSettings["offset"] = appSettings["maxOffset"]
        self.controlSettings = self.configInterface.get_all_control_settings()
        self.observationSettings = self.configInterface.get_observation()
        self.observation = Observation(interface, self.observationSettings)
        self.controls = [
            Control(self.interface, controlSetting["controlParamInfo"],
                    controlSetting["meta"], self.appSettings)
            for _, controlSetting in self.controlSettings.items()
        ]
        self.callbackInterface.register_callback(
            clientId="thermostat",
            condition="topic == 'command/thermostat/setpoint'",
            callbackFunc=self.set_setpoint)

    def set_setpoint(self, topic, payload):
        self.appSettings["setpoint"] = payload
        print(" setpoint set ")
        for control in self.controls:
            for curve in control.curves:
                curve.init_computing()

    def start_flow(self):
        while 1:
            if self.appSettings["setpoint"] is None:
                print("No setpoint yet")
            else:
                code, temperature = self.observation.get_verify_observation()
                currentTime = int(time.time())
                for control in self.controls:
                    if control.isItTimeToModulate(currentTime):
                        if code == 0:
                            print("minimum position")
                        elif code == -1:
                            print("emergencyPosition")
                        elif code == 1:
                            curve = control.which_curve_right_now(
                                temperature, self.appSettings["setpoint"],
                                self.appSettings["offset"])
                            output = curve.output(temperature,
                                                  self.appSettings["setpoint"],
                                                  self.appSettings["offset"])
                            print(control.name, round(output), sep="---")
            time.sleep(60)


def main():
    configInterface = ConfigInterface()
    transportInterface = TransportInterface.from_mqtt("thermostat", on_connect,
                                                      on_disconnect,
                                                      on_message)
    interface = {
        "config": configInterface,
        "transport": transportInterface,
        "callback": CallbackMechanism
    }
    appSettings = configInterface.get_all_app_settings()
    flow = ApplicationFlow(interface, appSettings)
    flow.start_flow()
