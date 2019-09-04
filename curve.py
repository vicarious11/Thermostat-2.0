import ABController


class Curve:
    def __init__(self, interface, triggerExpr, controlSettings, appSettings):
        self.configInterface = interface["config"]
        self.triggerExpression = triggerExpr
        self.computingEngine = self._init_computing(controlSettings,
                                                    appSettings)

    def _init_computing(self, controlSettings, appSettings):
        return ABController(controlSettings, appSettings)

    def output(self, observation, setpoint, offset):
        return self.computingEngine.compute(observation)
