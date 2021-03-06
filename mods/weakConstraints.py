from horairyst.problem.constraint import *

##########
# constraint:MinimizeHoles
# type:weak
##########

@weakConstraint
class MinimizeHoles(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def getWeight(self):
        return 1

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for k in range(len(problem.E)):
                    self.addTerm(-(j + 1), problem.prettyPrintVar("x", i, j, k))
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    self.addTerm(-(j + 1), problem.prettyPrintVar("y", i, j, l))



##########
##########
# constraint:ArriveLatestPossible
# type:weak
##########

@weakConstraint
class ArriveLatestPossible(WeakConstraint):
    @staticmethod
    def countAttendances(problem, l):
        x = 0
        for lst in problem.C:
            if lst[l] == 1:
                x += 1
        return x

    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def getWeight(self):
        return 1

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    for k in range(len(problem.E)):
                        if problem.C[k][l] == 1:
                            self.addTerm(-((j + 1) * (len(problem.E) - self.countAttendances(problem, l))),
                                         problem.prettyPrintVar("x", i, j, k))
                            self.addTerm(-((j + 1) * (len(problem.E) - self.countAttendances(problem, l))),
                                         problem.prettyPrintVar("y", i, j, l))


##########
##########
# constraint:MinimizeMoving
# type:weak
##########

@weakConstraint
class MinimizeMoving(WeakConstraint):
    @staticmethod
    def countAttendances(problem, l):
        x = 0
        for lst in problem.C:
            if lst[l] == 1:
                x += 1
        return x

    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def getWeight(self):
        return 0.1

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for l in range(len(problem.R)):
                    self.addTerm(10 * (i+1), problem.prettyPrintVar("y", i, j, l))


##########
##########
# constraint:LeastPossibleSessions
# type:weak
##########

@weakConstraint
class LeastPossibleSessions(WeakConstraint):
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def getWeight(self):
        return 1

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.P)):
                for k in range(len(problem.E)):
                    self.addTerm(i+1, problem.prettyPrintVar("x", i, j, k))


##########
##########
# constraint:LrsFirstThenMemoirs
# type:weak
##########

@weakConstraint
class LrsFirstThenMemoirs(WeakConstraint):
    def getMaxValue(self, problem):
        return 0

    def getMinValue(self, problem):
        return 0

    def getWeight(self):
        return 1

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


##########
