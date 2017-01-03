from horairyst.problem.problem import Problem
from horairyst.problem import constraint


def parse(filename):
    f = open(filename, "r")
    S, P, E, R, C = [], [], [], [], []
    # extract Sessions (locals)
    for local in f.readline().split(","):
        S.append(local.strip())
    # extract periods (hours)
    for hour in f.readline().split(","):
        P.append(hour.strip())
    c = []
    # extract Students, Directors and compute association matrix
    for l in f:
        tmp = []
        l = l.split(",")
        E.append(l[0].strip())
        for k in range(1,len(l)):
            if l[k].strip() not in R:
                R.append(l[k].strip())
            tmp.append(R.index(l[k].strip()))
        c.append(tmp)
    for l in c:
        tmp = []
        for i in range(len(R)):
            if i in l:
                tmp.append(1)
            else:
                tmp.append(0)
        C.append(tmp)

    print(S, P, E, R, C)
    return Problem(S, P, E, R, C, constraint.getStrongConstraints(), constraint.getWeakConstraints())


def getHandledExtensions():
    return [".csv"]
