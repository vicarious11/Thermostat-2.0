from ab import ABController


class Curve:
    def __init__(self, name, configInterface, curveConfig, actionSettings,
                 state):
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
            curveConfig(dict) : settings of curve
            {
                "name":"increasing",
                "triggerExpr" : "<<expression>>",
                "continueExpr" : "<<expression>>"
            }
        """
        self.name = name
        self.state = state
        self.configInterface = configInterface
        self.endOfComputation = None
        self.triggerExpression = curveConfig["triggerExpr"]
        self.continueExpression = curveConfig["continueExpr"]
        self.actionSettings = actionSettings

    def init_computing(self, appSettings):
        self.computingEngine = ABController(self.actionSettings, appSettings,
                                            self.state["curve"][self.name])

    def output(self, observation):
        return self.computingEngine.compute(observation)
