class AB():
	def __init__(self, paramConfig):
		self.actionableMax = paramConfig['actionableMax']
		self.actionableMin = paramConfig['actionableMin']
		self.controlSpeed = paramConfig['controlSpeed']
		self.timeToAchieveSetpoint = paramConfig['timeToAchieveSetpoint']
		self.degreeOfFreedom = paramConfig['degreeOfFreedom']
		self.setpoint = paramConfig['setpoint']
		self.controllerDirection = paramConfig['controllerDirection']
		self.sampleTime = paramConfig['sampleTime']
		
		self.lastInput = 0 
		self.minimumError = 0.01	
		self.nitroBoost = 1

		self.numberOfCommands = self.computeNumberOfCommands()
		self.iTerm = self.userCommandResolution()
		self.output = self.iTerm
	
	def compute(self, Input):
		error = self.setpoint - Input	
		print("Error -->")
		print(error)

		if self.numberOfCommands == 0:
			return self.actionableMax

		if self.output == self.actionableMax:
			self.numberOfCommands = self.numberOfCommands - 1
			print(self.numberOfCommands)
			return self.actionableMax

		if error == 0:
			self.A = self.iTerm / self.minimumError
			self.B = self.mappingFunction(self.A)
		else:
			self.A = self.iTerm / error
			self.B = self.mappingFunction(self.A)

		if self.controllerDirection == 0:
			self.A *= -1
			self.B *= -1

		self.iTerm += self.B * error

		delta = Input - self.lastInput

		if self.lastInput == 0:
			self.output = self.iTerm 
		else:
			self.output = self.iTerm + self.B * delta

		self.cappedOutput()
		self.lastInput = Input
		self.numberOfCommands = self.numberOfCommands - 1
		print(self.numberOfCommands)
		return self.output
 

	def mappingFunction(self, A):
		dampingFactor = self.numberOfCommands * (self.actionableMax - self.output)
		computedB = (self.A / dampingFactor) * self.nitroBoost
		return computedB

	def setControllerDirection(self, direction):
		self.controllerDirection = direction
	
	def computeNumberOfCommands(self):
		return round(self.timeToAchieveSetpoint/self.sampleTime)

	def cappedOutput(self):
		if self.output > self.actionableMax:
			self.output = self.actionableMax
		elif self.output < self.actionableMin: 
			self.output = self.actionableMin

	def userCommandResolution(self):
		resolution = ((self.actionableMax - self.actionableMin) / self.degreeOfFreedom)
		commandResolution = resolution * self.controlSpeed + self.actionableMin
		return commandResolution

