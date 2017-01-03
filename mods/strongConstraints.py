from horairyst.problem.constraint import strongConstraint, testConstraint, Constraint
from horairyst.problem.problem import Problem


@strongConstraint
class StudentScheduledOnlyOnce(Constraint):
    def getConstraint(self, problem):
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


@strongConstraint
class DirectorNotInTwoDistinctSessionsAtSameTime(Constraint):
    def getConstraint(self, problem):
        # sum_i yijl <= 1
        res = ""
        for j in range(len(problem.Y[0])):
            for l in range(len(problem.Y[0][0])):
                for i in range(len(problem.Y)):
                    res += problem.prettyPrintVar("y", i, j, l) + " + "
                res = res[:-3]
                res += " <= 1\n"
        return res


@strongConstraint
class NoTwoStudentsInSameSlot(Constraint):
    def getConstraint(self, problem):
        # sum_k xijk <= 1
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res += problem.prettyPrintVar("x", i, j, k) + " + "
                res = res[:-3]
                res += " <= 1\n"
        return res


@strongConstraint
class DirectorPresentIOIAssignedToStudent(Constraint):
    def getConstraint(self, problem):
        # yijl >= xijk * Ckl
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    for l in range(len(problem.Y[i][j])):
                        res += problem.prettyPrintVar("y", i, j, l)
                        res += (" - " + problem.prettyPrintVar("x", i, j,  k) if problem.C[k][l] == 1 else "")
                        res += " >= 0\n"
        return res
