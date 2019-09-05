from ab import ABController


class Curve:
    def __init__(self, interface, triggerExpr, controlSettings, appSettings):
        self.triggerExpression = triggerExpr

    def init_computing(self, controlSettings, appSettings):
        return ABController(controlSettings, appSettings)

    def output(self, observation, setpoint, offset):
        return self.computingEngine.compute(observation)
