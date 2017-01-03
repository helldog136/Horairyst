from horairyst.problem.constraint import weakConstraint, testConstraint, Constraint


@weakConstraint
class MinimizeHoles(Constraint):
    def getConstraint(self, problem):
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res += " -" + str(j+1) + " " + problem.prettyPrintVar("x", i, j, k)
        for i in range(len(problem.Y)):
            for j in range(len(problem.Y[i])):
                for l in range(len(problem.Y[i][j])):
                    res += " -" + str(j+1) + " " + problem.prettyPrintVar("y", i, j, l)
        res += ""
        return res

@weakConstraint
class arriveLatestPossible(Constraint):
    def getConstraint(self, problem):
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res += " -" + str(j + 1 + (len(problem.C[k]) - self.countOnes(problem.C[k])))\
                           + " " + problem.prettyPrintVar("x", i, j, k)
        for i in range(len(problem.Y)):
            for j in range(len(problem.Y[i])):
                for l in range(len(problem.Y[i][j])):
                        res += " -" + str(j + 1 + (len(problem.C[k]) - self.countOnes(problem.C[k])))\
                               + " " + problem.prettyPrintVar("y", i, j, l)
        res += ""
        return res

    def countOnes(self, l):
        i = 0
        for n in l :
            i+=1
        return i


@weakConstraint
class minimzeMoving(Constraint):
    def getConstraint(self, problem):
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    res += " -" + str(j + 1 + self.countOnes(problem.C[k]))\
                           + " " + problem.prettyPrintVar("x", i, j, k)
        for i in range(len(problem.Y)):
            for j in range(len(problem.Y[i])):
                for l in range(len(problem.Y[i][j])):
                    # for _ in range(j + 1 + self.countOnes(problem.C[l])):
                        res += " - " + problem.prettyPrintVar("y", i, j, l)
        res += ""
        return res

    def countOnes(self, l):
        i = 0
        for _ in l:
            i += 1
        return i


@weakConstraint
class leastPossibleSessions(Constraint):
    def getConstraint(self, problem):
        res = ""
        for i in range(len(problem.X)):
            for j in range(len(problem.X[i])):
                for k in range(len(problem.X[i][j])):
                    for _ in range(i+1):
                        res += problem.prettyPrintVar("x", i, j, k) + " + "
        return res
