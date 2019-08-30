import ab

Input = 29

dct = {"actionableMax": 95, "actionableMin": 60,"controlSpeed": 1, "timeToAchieveSetpoint": 60,"degreeOfFreedom": 5,"setpoint": 25,"controllerDirection": 1, "sampleTime": 2}

abObject = ab.AB(dct)
count = 50
while (count):	
	output = abObject.compute(Input)
	Input = Input - 0.3
	print(output)
	count = count - 1
