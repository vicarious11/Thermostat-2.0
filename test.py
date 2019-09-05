import ab

Input = 29

controlSettings = {"maxModulation": 95, "minModulation": 60,"modulationSpeed": 1,"controllerDirection": 1, "sampleTime": 2}
appSettings = {"timeToAchieveSetpoint": 60,"degreeOfFreedom": 5,"setpoint": 25}
abObject = ab.AB(controlSettings,appSettings)
count = 50
while (count):	
	output = abObject.compute(Input)
	Input = Input - 0.3
	print(output)
	count = count - 1
