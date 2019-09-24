class AB():
	def __init__(self, controlSettings, appSettings):
		self.maxModulation = controlSettings['maxModulation']
		self.minModulation = controlSettings['minModulation']
		self.modulationSpeed = controlSettings['modulationSpeed']
		self.timeToAchieveSetpoint = appSettings['timeToAchieveSetpoint']
		self.degreeOfFreedom = appSettings['degreeOfFreedom']
		self.setpoint = appSettings['setpoint']
		self.controllerDirection = controlSettings['controllerDirection']
		self.sampleTime = controlSettings['sampleTime']		
		
		self.lastInput = 0 
		self.numberOfCommands = self.compute_number_of_commands()
		self.iTerm = self.user_command_resolution()           #Add bias from user entered data
		self.output = self.iTerm
	
	def compute(self, Input):
		error = Input - self.setpoint
		print("Error -->")

		if self.numberOfCommands == 0:
			return self.maxModulation

		if self.output == self.maxModulation:
			self.numberOfCommands = self.numberOfCommands - 1
			print(self.numberOfCommands)
			return self.maxModulation

		self.reactiveTerm = calculate_reactive_term()
		self.diffrentialTerm = calculate_differetial_term()

		if self.controllerDirection == -1:
			self.reactiveTerm = -1 * self.reactiveTerm
			self.diffrentialTerm = -1 * self.diffrentialTerm
	
		self.iTerm += self.reactive * error

		delta = Input - self.lastInput

		self.output = self.iTerm - self.diffrentialTerm * delta

		self.capped_output()
		self.lastInput = Input
		self.numberOfCommands = self.numberOfCommands - 1
		print(self.numberOfCommands)
		return self.output
 

	def calculate_reactive_term(self):
		resoltionLeft = (self.maxModulation - self.output) / self.numberOfCommands
		reactToError = resolutionLeft * self.modulationSpeed
		return reactToError

	def calculate_differetial_term(self):
		return (self.reactiveTerm / self.degreeOfFreedom)

	def set_controller_direction(self, direction):
		self.controllerDirection = direction
	
	def compute_number_of_commands(self):
		return round(self.timeToAchieveSetpoint/self.sampleTime)

	def capped_output(self):
		if self.output > self.maxModulation:
			self.output = self.maxModulation
		elif self.output < self.minModulation: 
			self.output = self.minModulation

	def user_command_resolution(self):
		resolution = ((self.maxModulation - self.minModulation) / self.degreeOfFreedom)
		commandResolution = resolution * self.modulationSpeed + self.minModulation 
		return commandResolution

