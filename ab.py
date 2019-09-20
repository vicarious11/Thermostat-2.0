class AB():
	def __init__(self, controlSettings):
		self.maxModulation = controlSettings['actionableMax']
		self.minModulation = controlSettings['actionableMin']
		self.modulationSpeed = controlSettings['controllSpeed']
		self.timeToAchieveSetpoint = controlSettings['timeToAchieveSetpoint']
		self.degreeOfFreedom = controlSettings['degreeOfFreedom']
		self.setpoint = controlSettings['setpoint']
		self.controllerDirection = controlSettings['controllerDirection']
		self.sampleTime = controlSettings['sampleTime']
		
		self.lastInput = 0 
		self.minimumError = 0.01	
		self.toggleSpeed = 1

		self.numberOfCommands = self.compute_number_of_commands()
		self.iTerm = self.user_command_resolution()
		self.output = self.iTerm
	
	def compute(self, Input):
		error = self.setpoint - Input	
		print("Error -->")
		print(error)

		if self.numberOfCommands == 0:
			return self.maxModulation

		if self.output == self.maxModulation:
			self.numberOfCommands = self.numberOfCommands - 1
			print(self.numberOfCommands)
			return self.maxModulation

		if error == 0:
			self.headStart = self.iTerm / self.minimumError
			self.correction = self.mapping_function(self.headStart)
		else:
			self.headStart = self.iTerm / error
			self.correction = self.mapping_function(self.headStart)

		if self.controllerDirection == 0:
			self.headStart *= -1
			self.correction *= -1

		self.iTerm += self.correction * error

		delta = Input - self.lastInput

		if self.lastInput == 0:
			self.output = self.iTerm 
		else:
			self.output = self.iTerm + self.correction * delta

		self.capped_output()
		self.lastInput = Input
		self.numberOfCommands = self.numberOfCommands - 1
		print(self.numberOfCommands)
		return self.output
 

	def mapping_function(self, headStart):
		dampingFactor = self.numberOfCommands * (self.maxModulation - self.output)
		computedB = (self.headStart / dampingFactor) * self.toggleSpeed
		return computedB

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

