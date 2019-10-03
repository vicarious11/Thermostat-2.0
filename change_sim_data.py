with open("./temp_data.txt") as f:
    tmpData = f.readlines()

simData = []
for temp in tmpData:
    simData.append(temp.split("\n")[0] + ",True\n")

with open("./sim_data.txt", "w") as f:
    for line in simData:
        f.writelines(line)
