from control import Control
from interface_config import ConfigInterface
from observation import Observation


class Thermal_0_0_1:
    defaultState = {
        "offset": "default",
        "currentIterations": 0,
        "timerCrossed": 0,
        "cycle": 0,
        "previousAhuStatus": 0,
        "curve": {
            "increasing": {
                "iTerm": "default",
                "numberOfCommands": "default",
                "lastInput": "default"
            },
            "decreasing": {
                "iTerm": "default",
                "numberOfCommands": "default",
                "lastInput": "default"
            }
        }
    }

    def __init__(self, appConfig, state=None):
        """
        Args:
            state(dict) : previous state
            {
                "offset": "default",
                "currentIterations": 0,
                "timerCrossed": 0,
                "cycle": 0,
                "previousAhuStatus": 0,
                "curve": {
                    "increasing": {
                        "iTerm": "default",
                        "numberOfCommands": "default",
                        "lastInput": "default"
                    },
                    "decreasing": {
                        "iTerm": "default",
                        "numberOfCommands": "default",
                        "lastInput": "default"
                    }
                }
            }
            appSettings(dict) : settings to run thermostat app
            {
                "setpoint" : "25",
                "minOffset" : 0.25,
                "maxOffset" : 0.5,
                "timeToAchieve" : 0.9,
                "appMode" : "cooling",
            }
            actionSettings(dict) : settings of an actionable
            {
                "name" : "actuator",
                "emergencyPosition" : 75,
                "minimumPosition" : 10,
                "minModulation" : 60,
                "maxModulation" : 85,
                "modulationSpeed" : 2,
                "sampleTime" : 2
            }

        """
        if state == None:
            state = self.defaultState
        self.configInterface = ConfigInterface(appConfig)
        self.appSettings = self.configInterface.appSettings
        self.actionSettings = self.configInterface.actionSettings
        self.state = state
        self.observation = Observation(self.state)
        self.cycleStartExpression = self.configInterface.expressions[
            "cycleStartExpression"]
        self.cycleEndExpression = self.configInterface.expressions[
            "cycleEndExpression"]
        self.newOffsetExpression = self.configInterface.expressions[
            "newOffsetExpression"]
        self.maxIterations = self.appSettings[
            "timeToAchieve"] // self.actionSettings["sampleTime"]
        self.control = Control(self.configInterface, self.actionSettings)
        if self.state["offset"] == "default":
            self.state["offset"] = self.appSettings["maxOffset"]

    def make_default_curve_state(self):
        for curve in self.control.curves:
            self.state["curve"][curve.name]["iTerm"] = "default"
            self.state["curve"][curve.name]["numberOfCommands"] = "default"
            self.state["curve"][curve.name]["lastInput"] = "default"

    def set_setpoint(self, update=False):
        if update == True:
            self.state["offset"] = self.appSettings["maxOffset"]
        self.state["currentIterations"] = 0
        self.state["timerCrossed"] = 0
        for curveName, curve in self.control.curves.items():
            self.update_default_curve_state()
            curve.init_computing(self.appSettings, self.state)

    def set_output(self, level):
        controlValuesAtDiffLevels = {
            "minimum": self.control.minimumPosition,
            "maximum": 100,
            "emergency": self.control.emergency
        }
        output = controlValuesAtDiffLevels[level]
        output = round(self.control.map_to_real_value(output))
        return output

    def generate_new_offset(self, observation):
        setpoint = self.state["setpoint"]
        minOffset = self.appSettings["minOffset"]
        maxOffset = self.appSettings["maxOffset"]
        for expr, newOffset in self.newOffsetExpression.items():
            if eval(expr):
                return eval(newOffset)

    def automate_offset(self, curveName, observation):
        if (self.state["currentIterations"] >= self.maxIterations) and \
           curveName == "increasing":
            # : send alert
            self.state["offset"] = self.appSettings["minOffset"]
            self.state["timerCrossed"] = 1
            self.output = self.set_output("maximum")
            return
        elif (self.state["currentIterations"] >= self.maxIterations) and \
                curveName == "decreasing":
            self.state["offset"] = self.generate_new_offset(observation)
            self.set_setpoint()
            self.state["cycle"] = 0
            self.output = self.set_output("minimum")
            return

    def cycle_end(self, observation):
        offset = self.appSettings["offset"]
        setpoint = self.appSettings["setpoint"]
        return eval(self.cycleEndExpression)

    def cycle_start(self, observation):
        offset = self.appSettings["offset"]
        setpoint = self.appSettings["setpoint"]
        return eval(self.cycleStartExpression)

    def handle_cycle_trigger(self, observationCode, observation):
        if self.state["cycle"] == 0 and not self.cycle_start(observation):
            self.output = self.set_output("minimum")
        if self.state["cycle"] == 1 and (observationCode == 1
                                         and self.cycle_end(observation)):
            self.state["cycle"] = 0
            self.output = self.set_output("minimum")
            return
        elif self.state["cycle"] == 0 and (observationCode == 1
                                           and self.cycle_start(observation)):
            self.state["cycle"] = 1
            self.set_setpoint()
            return

    def save_last_output_in_decreasing_curve(self, control, curve, output):
        if curve.name == "increasing":
            self.state["decreasing"]["iTerm"] = output

    def execute(self, observation):
        temperature = observation["temp"]
        ahuStatus = observation["ahuStatus"]

        curve = None
        observationCode, temperature = \
            self.observation.verify_observation(temperature, ahuStatus)
        self.handle_cycle_trigger(observationCode, temperature)
        if observationCode == -2:
            self.set_setpoint()
        elif observationCode == 0:
            self.state["cycle"] = 0
            self.output = self.set_output("minimum")
        elif observationCode == -1:
            self.state["cycle"] = 0
            self.output = self.output("emergency")
        elif observationCode == 1:
            if self.state["cycle"] == 1 and not self.state["timerCrossed"]:
                self.state["currentIterations"] += 1
                curve = self.control.which_curve_right_now(
                    temperature, self.state["setpoint"], self.state["offset"])
                output = curve.output(temperature, self.state["setpoint"],
                                      self.state["offset"])
                self.save_last_output_in_decreasing_curve(
                    self.control, curve, output)
                output = round(self.control.map_to_real_value(output))
                self.output = output
            if curve:
                self.automate_offset(curve.name, temperature)
        return self.output, self.state
