from horairyst.problem.problem import Problem
from horairyst.problem import constraint


def parse(filename):
    f = open(filename, "r")
    S, P, E, R, C, roles = [], [], [], [], [], []
    # pass the 5 first lines
    for i in range(5):
        f.readline()
    # extract Sessions (locals)
    for local in f.readline().split(","):
        S.append(local.strip())
    # extract periods (hours)
    for hour in f.readline().split(","):
        P.append(hour.strip())
    c = []
    #Skip LRS line
    f.readline()
    # extract Students, Directors and compute association matrix
    prefix = "L:"
    for l in f:
        if l[0] != "#" and len(l.strip()) > 1:
            if l[:8].lower() == ("memoires"):
                prefix = "M:"
                continue
            tmp = []
            l = l.split(",")
            E.append(prefix+l[0].strip())
            for k in range(1, 4):
                teacher = l[k].strip()
                if teacher != "":
                    if teacher not in R:
                        R.append(teacher)
                    tmp.append((R.index(l[k].strip()), "D"))

            for k in range(4, len(l)):
                teacher = l[k].strip()
                if teacher != "":
                    if teacher not in R:
                        R.append(teacher)
                    tmp.append((R.index(l[k].strip()), "R"))
            c.append(tmp)
    print(c)
    for l in c:
        l_clean = list(map((lambda m: m[0]), l))
        tmp = []
        tmp_roles = []
        for i in range(len(R)):
            if i in l_clean:
                tmp.append(1)
                tmp_roles.append(l[l_clean.index(i)][1])
            else:
                tmp.append(0)
                tmp_roles.append("")
        C.append(tmp)
        roles.append(tmp_roles)

    print(S, P, E, R, C, roles)
    return Problem(S, P, E, R, C, roles, constraint.getStrongConstraints(), constraint.getWeakConstraints())


def getHandledExtensions():
    return [".csv"]
