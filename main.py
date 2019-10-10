import time
from stateless import Thermal_0_0_1
from interface_config import ConfigInterface


def get_simulation_data():
    with open("./sim_data.txt") as f:
        data = f.readlines()
    tempData = (tempAhu.split("\n")[0].split(",")[0] for tempAhu in data)
    kwData = (tempAhu.split("\n")[0].split(",")[1] for tempAhu in data)
    return tempData, kwData


def main():
    tempData, kwData = get_simulation_data()
    state = None
    while 1:
        actuator = Thermal_0_0_1("actuatorRecipe.json", state)
        temp = eval(next(tempData))
        ahuStatus = eval(next(kwData))
        output, state = actuator.execute({
            "temp": temp,
            "ahuStatus": ahuStatus
        })
        print("temp --> {}  ahu --> {}".format(temp, ahuStatus))
        print("actuator output --> ", output)
        time.sleep(1)


main()
