from simulator import Simulator
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
        self.sim = Simulator()
        self.interface = interface
        self.configInterface = interface["config"]
        self.transportInterface = interface["transport"]
        self.callbackInterface = interface["callback"]
        self.appSettings = appSettings
        self.appSettings["offset"] = self.appSettings["maxOffset"]
        self.controlSettings = self.configInterface.get_all_control_settings()
        self.observationSettings = self.configInterface.get_observation()
        self.observation = Observation(interface, self.observationSettings)
        self.cycleStartExpression = appSettings["cycleStartExpression"]
        self.cycleEndExpression = appSettings["cycleEndExpression"]
        self.newOffsetExpression = appSettings["newOffsetExpression"]
        self.cycle = 0
        self.timerCrossed = 0
        self.currentIterations = 0
        self.maxIterations = int(
            (appSettings["timeToAchieveSetpoint"] * 60) / 1)
        self.controls = [
            Control(self.interface, controlSetting["controlParamInfo"],
                    controlSetting["meta"], self.appSettings)
            for _, controlSetting in self.controlSettings.items()
        ]
        self.callbackInterface.register_callback(
            clientId="thermostat",
            condition="topic == 'command/thermostat/setpoint'",
            callbackFunc=self.set_setpoint)

    def set_setpoint(self, topic=None, payload=None):
        if topic != None:
            self.appSettings["offset"] = self.appSettings["maxOffset"]
        self.appSettings["setpoint"] = payload
        self.currentIterations = 0
        self.timerCrossed = 0
        print(" setpoint set ")
        for control in self.controls:
            for curve in control.curves:
                curve.init_computing()

    def automate_offset(self, curveName, temperature):
        if (self.currentIterations >= self.maxIterations) and \
           curveName == "increasing":
            self.execute_controls("maximum")
            self.transportInterface.send_alert("timetoachieve")
            self.appSettings["offset"] = self.appSettings["minOffset"]
            self.timerCrossed = 1
        elif self.currentIterations >= self.maxIterations and \
                curveName == "decreasing":
            self.execute_controls("minimum")
            self.appSettings["offset"] = self.generate_new_offset(temperature)
            self.set_setpoint(payload=self.appSettings["setpoint"])
            self.cycle = 0

    def generate_new_offset(self, observation):
        setpoint = self.appSettings["setpoint"]
        minOffset = self.appSettings["minOffset"]
        maxOffset = self.appSettings["maxOffset"]
        for expr, newOffset in self.newOffsetExpression.items():
            if eval(expr):
                return eval(newOffset)

    def cycle_end(self, observation):
        offset = self.appSettings["offset"]
        setpoint = self.appSettings["setpoint"]
        return eval(self.cycleEndExpression)

    def cycle_start(self, observation):
        offset = self.appSettings["offset"]
        setpoint = self.appSettings["setpoint"]
        return eval(self.cycleStartExpression)

    def execute_controls(self, level):
        for control in self.controls:
            controlValuesAtDiffLevels = {
                "minimum": control.minimumPosition,
                "maximum": 100,
                "emergency": control.emergency
            }
            output = controlValuesAtDiffLevels[level]
            output = control.map_to_real_value(output)
            self.transportInterface.set_control(round(output), control.name)
            self.sim.save_output(control.name, self.currentTime, round(output))

    def handle_cycle_trigger(self, observationCode, observation):
        if self.cycle == 0 and (observationCode == 1) and (
                not self.cycle_start(observation)):
            self.execute_controls("minimum")
        if self.cycle == 1 and (observationCode == 1
                                and self.cycle_end(observation)):
            self.cycle = 0
            self.execute_controls("minimum")
        elif self.cycle == 0 and (observationCode == 1
                                  and self.cycle_start(observation)):
            self.cycle = 1
            self.set_setpoint(payload=self.appSettings["setpoint"])

    def progress_controls_timer(self, currentTime):
        for control in self.controls:
            control.progress_timer(currentTime)

    def save_last_output_in_decreasing_curve(self, control, curve, output):
        if curve.name == "increasing":
            for curve in control.curves:
                if curve.name == "decreasing":
                    curve.computingEngine.iTerm = output

    def start_flow(self):
        while 1:
            self.currentTime = int(time.time())
            self.sim.save_time_x_axis(self.currentTime)
            self.progress_controls_timer(self.currentTime)
            curve = None
            if self.appSettings["setpoint"] is None:
                print("No setpoint yet")
            else:
                try:
                    observationCode, temperature = \
                        self.observation.get_verify_observation()
                except StopIteration:
                    self.sim.build()
                self.sim.save_observation(self.currentTime, temperature)
                print("current temp -->", temperature)
                self.handle_cycle_trigger(observationCode, temperature)
                if observationCode == -2:
                    self.set_setpoint(payload=self.appSettings["setpoint"])
                    print("thermostat reset")
                elif observationCode == 0:
                    self.execute_controls("minimum")
                    self.cycle = 0
                elif observationCode == -1:
                    self.execute_controls("emergency")
                    self.cycle = 0
                elif observationCode == 1:
                    if self.cycle == 1 and not self.timerCrossed:
                        self.currentIterations += 1
                        for control in self.controls:
                            if control.isItTimeToModulate(self.currentTime):
                                curve = control.which_curve_right_now(
                                    temperature, self.appSettings["setpoint"],
                                    self.appSettings["offset"])
                                output = curve.output(
                                    temperature, self.appSettings["setpoint"],
                                    self.appSettings["offset"])
                                self.save_last_output_in_decreasing_curve(
                                    control, curve, output)
                                output = control.map_to_real_value(output)
                                self.transportInterface.set_control(
                                    round(output), control.name)
                                self.sim.save_output(control.name,
                                                     self.currentTime,
                                                     round(output))
                    if curve:
                        self.automate_offset(curve.name, temperature)
            time.sleep(self.appSettings["minSampleTime"])


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


main()
