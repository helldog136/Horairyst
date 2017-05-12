from horairyst.problem.constraint import strongConstraint, testConstraint, StrongConstraint
from horairyst.problem.problem import Problem


@strongConstraint
class StudentScheduledOnlyOnce(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_ij xijk = 1
        res = []
        for k in range(len(problem.X[0][0])):
            res.append("")
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res[k] += problem.prettyPrintVar("x", i, j, k)
                    res[k] += (" = 1\n" if (i, j) == (len(problem.X) - 1, len(problem.X[i]) - 1) else " + ")
        strng = ""
        for i in res:
            strng += i
        return strng

    def checkValidity(self, X, Y, S, P, E, R, C):
        res = True
        wrongs = []
        for k in range(len(E)):
            ctr = 0
            lst = []
            for i in range(len(S)):
                for j in range(len(P)):
                    ctr += X[i][j][k]
                    if X[i][j][k] > 0:
                        lst.append((i,j))
            res = res and ctr == 1
            if not ctr == 1:
                for i, j in lst:
                    wrongs.append((i, j, k, -1))
        return (res, wrongs)


@strongConstraint
class DirectorNotInTwoDistinctSessionsAtSameTime(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_i yijl <= 1
        res = ""
        for j in range(len(problem.Y[0])):
            for l in range(len(problem.Y[0][0])):
                for i in range(len(problem.Y)):
                    res += problem.prettyPrintVar("y", i, j, l) + " + "
                res = res[:-3]
                res += " <= 1\n"
        return res

    def checkValidity(self, X, Y, S, P, E, R, C):
        res = True
        wrongs = []
        for j in range(len(P)):
            for l in range(len(R)):
                ctr = 0
                lst = []
                for i in range(len(S)):
                    ctr += Y[i][j][l]
                    if Y[i][j][l] > 0:
                        lst.append((i,j))
                res = res and ctr <= 1
                if not ctr <= 1:
                    for _i,_j in lst:
                        wrongs.append((_i, _j, -1, l))
        return (res, wrongs)


@strongConstraint
class NoTwoStudentsInSameSlot(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_k xijk <= 1
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res += problem.prettyPrintVar("x", i, j, k) + " + "
                res = res[:-3]
                res += " <= 1\n"
        return res

    def checkValidity(self, X, Y, S, P, E, R, C):
        res = True
        wrongs = []
        for i in range(len(S)):
            for j in range(len(P)):
                ctr = 0
                for k in range(len(E)):
                    ctr += X[i][j][k]
                res = res and ctr <= 1
                if not ctr <= 1:
                    wrongs.append((i, j, -1, -1))
        return (res, wrongs)


@strongConstraint
class DirectorPresentIOIAssignedToStudent(StrongConstraint):
    def computeConstraint(self, problem):
        # yijl >= xijk * Ckl --> yijl - xijk >= 0 if Ckl
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    for l in range(len(problem.Y[i][j])):
                        if problem.C[k][l] == 1:
                            res += problem.prettyPrintVar("y", i, j, l)
                            res += (" - " + problem.prettyPrintVar("x", i, j, k))
                            res += " >= 0\n"
        return res

    def checkValidity(self, X, Y, S, P, E, R, C):
        res = True
        wrongs = []
        for i in range(len(S)):
            for j in range(len(P)):
                for k in range(len(E)):
                    for l in range(len(R)):
                        if C[k][l] == 1:
                            res = res and (Y[i][j][l] - X[i][j][k]) >= 0
                            if not (Y[i][j][l] - X[i][j][k]) >= 0:
                                wrongs.append((i, j, k, l))
        return (res, wrongs)
