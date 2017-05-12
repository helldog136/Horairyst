from horairyst.problem.constraint import weakConstraint, testConstraint, Constraint, WeakConstraint


# Ajouter des poids sur les contraintes

@weakConstraint
class MinimizeHoles(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for k in range(len(problem.E)):
                    self.addTerm(-(j + 1), problem.prettyPrintVar("x", i, j, k))
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    self.addTerm(-(j + 1), problem.prettyPrintVar("y", i, j, l))


def countAttendances(problem, l):
    x = 0
    for lst in problem.C:
        if lst[l] == 1:
            x += 1
    return x


@weakConstraint
class arriveLatestPossible(WeakConstraint):
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    for k in range(len(problem.E)):
                        if problem.C[k][l] == 1:
                            self.addTerm(-((j + 1) * (len(problem.E) - countAttendances(problem, l))),
                                         problem.prettyPrintVar("x", i, j, k))
                            self.addTerm(-((j + 1) * (len(problem.E) - countAttendances(problem, l))),
                                         problem.prettyPrintVar("y", i, j, l))


@weakConstraint
class minimizeMoving(WeakConstraint): #TODO rework
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    for k in range(len(problem.E)):
                        if problem.C[k][l] == 1:
                            self.addTerm(-((j + 1) * (countAttendances(problem, l))),
                                         problem.prettyPrintVar("x", i, j, k))
                            self.addTerm(-((j + 1) * (countAttendances(problem, l))),
                                         problem.prettyPrintVar("y", i, j, l))


@weakConstraint
class leastPossibleSessions(WeakConstraint):
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for k in range(len(problem.E)):
                    self.addTerm(i+1, problem.prettyPrintVar("x", i, j, k))
                for l in range(len(problem.R)):
                    self.addTerm(i+1, problem.prettyPrintVar("y", i, j, l))


@weakConstraint
class lrsFirstThenMemoirs(WeakConstraint):
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def computeConstraint(self, problem):
        for k in range(len(problem.E)):
            if problem.E[k][0] == "L":  # LRS
                for i in range(len(problem.S)):
                    for j in range(len(problem.P)):
                        self.addTerm(j+1, problem.prettyPrintVar("x", i, j, k))
            else:
                for i in range(len(problem.S)):
                    for j in range(len(problem.P)):
                        self.addTerm((len(problem.P) - (j + 1)), problem.prettyPrintVar("x", i, j, k))
