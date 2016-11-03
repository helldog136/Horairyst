from horairyst.problem.constraint import newConstraint, testConstraint, Constraint


@newConstraint
class studentScheduledOnlyOnce(Constraint):
    def getConstraint(self, problem):
        res = []
        for k in range(len(problem.X[0][0])):
            res.append("")
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                # sum_ij xijk = 1
                for k in range(len(problem.X[i][j])):
                    res[k] += problem.prettyPrintVar("x", i, j, k)
                    res[k] += (" = 1\n" if (i, j) == (len(problem.X) - 1, len(problem.X[i]) - 1) else " + ")
        strng = ""
        for i in res:
            strng += i
        return strng


@newConstraint
class directorNotInTwoDistinctSessionsAtSameTime(Constraint):
    def getConstraint(self, problem):
        pass
