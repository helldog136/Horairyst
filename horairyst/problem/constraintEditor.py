
def getConstraintsFromFile(filename):
    res = []
    with open(filename, 'r') as file:
        inCst = False
        stepRes = {}
        for line in file:
            if inCst:
                if line == "##########":
                    inCst = False
                    res.append(stepRes)
                else:
                    stepRes["content"] += line  # TODO maybe add \n
            else:
                if line == "##########":
                    stepRes = {}
                    line = file.readline()
                    stepRes["constraint"] = line.split(":").strip()
                    line = file.readline()
                    stepRes["type"] = line.split(":").strip()
                    line = file.readline()
                    stepRes["content"] = ""
                    inCst = True
    return res


def getStrongConstraints():
    return getConstraintsFromFile("mods/strongConstraints.py")

def setStrongConstraints(json):
    return None


def getWeakConstraints():
    return getConstraintsFromFile("mods/weakConstraints.py")


def setWeakConstraints(json):
    return None
