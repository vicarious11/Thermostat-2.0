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

        self.reactiveTerm = self.calculate_reactive_constant()
        #   print(self.reactiveTerm)

        #     if self.controllerDirection == -1:                  # if application is in forward mode(APPLICATION = HEATING), set controller direction = -1
        #       	self.reactiveTerm = -1 * self.reactiveTerm

        #  print(self.reactiveTerm)

        self.iTerm += self.reactiveTerm * error
        # print("Integral Component")
        #	print(self.iTerm)

        if self.lastInput == 0:  #Might be false for very small cases where Input value read from the sensor is '0'
            self.lastInput = Input

        delta = Input - self.lastInput
        #print("Delta --->")
        # print(delta)

        self.output = self.iTerm - self.reactiveTerm * delta * self.degreeOfFreedom
        self.capped_output()
        self.lastInput = Input
        self.numberOfCommands = self.numberOfCommands - 1
        return self.output

    def calculate_reactive_constant(self):
        return ((self.maxModulation - self.output) /
                self.numberOfCommands) * self.modulationSpeed

    def set_controller_direction(self, direction):
        self.controllerDirection = direction

    def compute_number_of_commands(self):
        return round(self.timeToAchieveSetpoint / self.sampleTime)

    def capped_output(self):
        if self.output > self.maxModulation:
            self.output = self.maxModulation
        elif self.output < self.minModulation:
            self.output = self.minModulation

    def user_command_resolution(self):
        resolution = ((self.maxModulation - self.minModulation) /
                      self.degreeOfFreedom)
        commandResolution = resolution * self.modulationSpeed + \
            self.minModulation
        return commandResolution
