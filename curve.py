from ab import ABController


class Curve:
    def __init__(self, name, interface, triggers, controlSettings,
                 appSettings):
        self.name = name
        self.triggered = False
        self.endOfComputation = None
        self.triggerExpression = triggers["triggerExpr"]
        self.continueExpression = triggers["continueExpr"]
        self.direction = triggers["direction"]
        self.controlSettings = controlSettings
        self.appSettings = appSettings

    def init_computing(self):
        self.controlSettings["controllerDirection"] = self.direction
        self.computingEngine = ABController(self.controlSettings,
                                            self.appSettings)

    def output(self, observation, setpoint, offset):
        return self.computingEngine.compute(observation)
