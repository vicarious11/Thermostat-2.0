from ab import ABController


class Curve:
    def __init__(self, interface, triggers, controlSettings, appSettings):
        self.triggerExpression = triggers["triggerExpr"]
        self.endExpression = triggers["endExpr"]
        self.controlSettings = controlSettings
        self.appSettings = appSettings

    def init_computing(self):
        self.computingEngine = ABController(self.controlSettings,
                                            self.appSettings)

    def output(self, observation, setpoint, offset):
        if self.isItMyEnd(observation, setpoint, offset):
            return self.controlSettings["minimumPosition"]
        return self.computingEngine.compute(observation)

    def isItMyEnd(self, observation, setpoint, offset):
        if eval(self.endExpression):
            return 1
