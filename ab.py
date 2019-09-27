class ABController():
    def __init__(self, controlSettings, appSettings):
        self.maxModulation = controlSettings['maxModulation']
        self.minModulation = controlSettings['minModulation']
        self.modulationSpeed = controlSettings['modulationSpeed']
        self.timeToAchieveSetpoint = appSettings['timeToAchieveSetpoint']
        self.degreeOfFreedom = appSettings['degreeOfFreedom']
        self.setpoint = appSettings['setpoint']
        self.controllerDirection = appSettings['controllerDirection']
        self.sampleTime = controlSettings['sampleTime']

        self.lastInput = 0
        self.numberOfCommands = self.compute_number_of_commands()
        self.iTerm = self.user_command_resolution()
        self.output = self.iTerm

    def compute(self, Input):
        error = Input - self.setpoint

        if self.numberOfCommands == 0:
            return self.maxModulation

        if self.output == self.maxModulation:
            self.numberOfCommands = self.numberOfCommands - 1
            return self.maxModulation

        reactiveTerm = self.calculate_reactive_constant() * self.controllerDirection

        self.iTerm += reactiveTerm * error

        if self.lastInput == 0:
            self.lastInput = Input

        delta = Input - self.lastInput

        self.output = self.iTerm - reactiveTerm * delta
        self.capped_output()
        self.lastInput = Input
        self.numberOfCommands = self.numberOfCommands - 1
        return self.output

    def calculate_reactive_constant(self):
        return ((self.maxModulation - self.output) /
                self.numberOfCommands) * self.modulationSpeed

    def compute_number_of_commands(self):
        return round(self.timeToAchieveSetpoint / self.sampleTime)

    def capped_output(self):
        if self.output > self.maxModulation:
            self.output = self.maxModulation
        elif self.output < self.minModulation:
            self.output = self.minModulation

    def user_command_resolution(self):
        resolution = ((self.maxModulation - self.minModulation) / self.degreeOfFreedom)
        commandResolution = resolution * self.modulationSpeed + self.minModulation
        return commandResolution
