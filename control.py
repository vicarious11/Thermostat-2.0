from itertools import count
import time
from curve import Curve


class Control:
    def __init__(self, interface, controlParamInformation, controlSettings,
                 appSettings):
        """Constructor.

        Args:
            interface (dict): a collection of config and transport interfaces.
                {
                    "config" : `configInterface`,
                    "transport" : `transportInterface`
                }
            controlParamInformation (dict): store containing information of
                control parameter.
                {
                    "name" : "actuator",
                    "deviceid" : "123",
                    "param" : "changesetpoint"
                }
            controlSettings (dict): settings at which control parameter is
                modulated
                {
                    "emergencyPosition" : 80,
                    "minModulation" : 60,
                    "maxModulation" : 100,
                    "modulationSpeed" : 5,
                    "sampleTime" : 2,
                }
            appSettings (dict): settings at which thermostat is
                running
                {
                    "controllerDirection" : 1,
                    "timeToAchieveSetpoint" : 15,
                    "degreeOfFreedom" : 5,
                    "setpoint" : 25,
                    "offset" : 0.5
                }
        """
        self.name = controlParamInformation["name"]
        self.configInterface = interface["config"]
        self.transportInterface = interface["transport"]
        self.emergency = controlSettings["emergencyPosition"]
        self.minModulation = controlSettings["minModulation"]
        self.maxModulation = controlSettings["maxModulation"]
        self.modulationSpeed = controlSettings["modulationSpeed"]
        sampleTimeInSecs = controlSettings["sampleTime"] * 60
        self.curves = self._init_curves(interface, controlSettings,
                                        appSettings)
        initTime = int(time.time())
        self.timeSeriesForModulation = (initTime + (n + 1) * sampleTimeInSecs
                                        for n in count())

    def _init_curves(self, interface, controlSettings, appSettings):
        curvesConfig = self.configInterface.get_curves(self.name)
        return [
            Curve(interface, curveConfig["triggerExpr"], controlSettings,
                  appSettings) for _, curveConfig in curvesConfig.items()
        ]

    def isItTimeToModulate(self, currentEpochTime):
        myTime = next(self.timeSeriesForModulation)
        if abs(myTime - currentEpochTime) <= 2:
            return True
        return False

    def which_curve_right_now(self, observation, setpoint, offset):
        for curve in self.curves:
            if eval(curve.triggerExpression):
                return curve
        return None
