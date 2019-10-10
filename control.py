from itertools import count
import time
from curve import Curve


class Control:
    def __init__(self, configInterface, actionSettings, state):
        """Constructor.

        Args:
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
        self.name = actionSettings["name"]
        self.state = state
        self.configInterface = configInterface
        self.minimumPosition = actionSettings["minimumPosition"]
        self.emergency = actionSettings["emergencyPosition"]
        self.minModulation = actionSettings["minModulation"]
        self.maxModulation = actionSettings["maxModulation"]
        self.modulationSpeed = actionSettings["modulationSpeed"]
        self.percentToRealExpression = self.configInterface.expressions[
            "%torealvalue"]
        self.sampleTime = actionSettings["sampleTime"]
        self.curves = self._init_curves(actionSettings)

    def _init_curves(self, actionSettings):
        curvesConfig = self.configInterface.get_curves(self.name)
        return [
            Curve(name, self.configInterface, curvesConfig[name],
                  actionSettings, self.state)
            for name, curveConfig in curvesConfig.items()
        ]

    def which_curve_right_now(self, observation, setpoint, offset):
        # : curve expressions should not clash
        for curve in self.curves:
            if self.state["curve"][curve.name]["triggered"]:
                if curve.continueExpression == "None":
                    return curve
                elif eval(curve.continueExpression):
                    return curve
                else:
                    self.state["curve"][curve.name]["triggered"] = 0
            elif eval(curve.triggerExpression):
                self.state["curve"][curve.name]["triggered"] = 1
                return curve
        return None

    def map_to_real_value(self, percentage):
        return eval(self.percentToRealExpression)
