
def getConstraintsFromFile(filename):
    res = []
    with open(filename, 'r') as file:
        inCst = False
        stepRes = {}
        for line in file:
            if inCst:
                if line.strip() == "##########":
                    inCst = False
                    res.append(stepRes)
                else:
                    stepRes["content"] += line  # TODO maybe add \n
            else:
                if line.strip() == "##########":
                    stepRes = {}
                    line = file.readline()
                    print(line)
                    stepRes["constraint"] = line.split(":")[1].strip()
                    line = file.readline()
                    stepRes["type"] = line.split(":")[1].strip()
                    line = file.readline()
                    stepRes["content"] = ""
                    inCst = True
    return res


def setConstraintsFromJson(filename, json):
    with open(filename, 'w') as file:
        res = "from horairyst.problem.constraint import *\n\n"
        for cst in json:
            print(">>>"+str(cst))
            res += "##########\n"
            res += "# constraint:" + cst["constraint"] + "\n"
            res += "# type:" + cst["type"] + "\n"
            res += "##########\n"
            res += cst["content"] + "\n"
        file.write(res)


def getStrongConstraints():
    return getConstraintsFromFile("mods/strongConstraints.py")


def setStrongConstraints(json):
    return setConstraintsFromJson("mods/strongConstraints2.py", json)


def getWeakConstraints():
    return getConstraintsFromFile("mods/weakConstraints.py")


def setWeakConstraints(json):
    return setConstraintsFromJson("mods/weakConstraints2.py", json)
