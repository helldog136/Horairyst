from horairyst.problem.problem import Problem
from abc import ABCMeta, abstractclassmethod

strongConstraints = None
weakConstraints = None


def getStrongConstraints():
    global strongConstraints
    return strongConstraints


def strongConstraint(const):
    global strongConstraints
    if strongConstraints is None:
        strongConstraints = const()
    else:
        strongConstraints.addConstraint(const())


def getWeakConstraints():
    global weakConstraints
    return weakConstraints


def weakConstraint(const):
    global weakConstraints
    if weakConstraints is None:
        weakConstraints = const()
    else:
        weakConstraints.addConstraint(const())


def testConstraint(const, pb=None, xit=True):
    if pb is None:
        S = ["18b6", "0a07"]
        P = ["08h30", "09h00", "09h30", "10h00", "10h30", "11h00"]
        E = ["Sacha Touille", "Alain Terieur", "Alex Terieur"]
        R = ["J. Wijsen", "H. Melot", "V. Bruyere", "A. Buys"]
        C = [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1]]
        roles = [[0, "D", "R", 0], ["D", 0, "R", 0], ["D", "R", 0, "D"]]
        pb = Problem(S, P, E, R, C, roles, const(), const())
    print("Testing your Constraint:", const.__name__, "with:")
    print("S:", pb.S, "(size: ", len(pb.S), ")")
    print("P:", pb.P, "(size: ", len(pb.P), ")")
    print("E:", pb.E, "(size: ", len(pb.E), ")")
    print("R:", pb.R, "(size: ", len(pb.R), ")")
    print("C:", pb.C, "(size: ", len(pb.C), ")")
    print("|X|:", len(pb.X), "x", len(pb.X[0]), "x", len(pb.X[0][0]))
    print("|Y|:", len(pb.Y), "x", len(pb.Y[0]), "x", len(pb.Y[0][0]))
    print("-" * 80)
    # print(
    c = const()  # )
    c.computeConstraint(pb)
    c.getConstraint()
    if xit:
        exit(0)


class Constraint(metaclass=ABCMeta):
    def __init__(self):
        self.nextConstraint = None
        self.computedHash = 0

    def addConstraint(self, _nextConstraint):
        """
        constraints are stored as linked lists
        :param _nextConstraint: the next constraint in the list
        :return: nothing
        """
        if self.nextConstraint is None:
            self.nextConstraint = _nextConstraint
        else:
            self.nextConstraint.addConstraint(_nextConstraint)

    def getConstraints(self, problem, ret=None):
        if ret is None:
            ret = []
        if self.computedHash != hash(problem):
            self.computedHash = hash(problem)
            self.computeConstraint(problem)
        cst = self.getConstraint()
        if cst is not None:
            ret.append(cst)
        if self.nextConstraint is not None:
            self.nextConstraint.getConstraints(problem, ret)
        return ret

    @abstractclassmethod
    def computeConstraint(self, problem):
        """
        used to call a computation of all the coefficients and variables to build the constraint on the specific problem
        :param problem: the problem to build the constraint
        :return: nothing but self.coefficients, self.variables and eventually self.goals have been updated
        """
        pass

    @abstractclassmethod
    def getConstraint(self, problem):
        """
        :return: the string representing the constraint 
        """
        pass


class WeakConstraint(Constraint, metaclass=ABCMeta):
    def __init__(self):
        super(WeakConstraint, self).__init__()
        self.coefficients = []
        self.variables = []

    def addTerm(self, coefficient, variable):
        self.coefficients.append(coefficient)
        self.variables.append(variable)

    @abstractclassmethod
    def computeConstraint(self, problem):
        pass

    @abstractclassmethod
    def getMaxValue(self, problem):
        return 0

    @abstractclassmethod
    def getMinValue(self, problem):
        return 0

    def getConstraint(self, problem):
        if len(self.coefficients) > 0 and len(self.coefficients) == len(self.variables):
            self.normalize(problem)
            weight = self.getWeight()
            res = ""
            res += self.coefficients[0] + " " + self.variables[0]
            for i in range(1, len(self.coefficients)):
                res += (" + " if weight * self.coefficients[i] >= 0 else " ")
                res += str(weight * self.coefficients[i]) + " " + self.variables[i]
            return res
        elif len(self.coefficients) != len(self.variables):
            raise ValueError("Coefficients does not have the same size as variables " +
                             "(" + str(len(self.coefficients)) + "," + str(len(self.variables)) + ")")
        else:
            return ""

    def normalize(self, problem):
        minv = self.getMinValue(problem)
        maxv = self.getMaxValue(problem)
        modifer = lambda x: 0
        if maxv != minv:
            modifer = lambda x: (x + (0 - minv)) / (maxv - minv)
        for i in range(len(self.coefficients)):
            self.coefficients[i] = modifer(self.coefficients[i])

    def getWeight(self):
        return 1


class StrongConstraint(Constraint, metaclass=ABCMeta): #TODO unifinished
    def __init__(self):
        super(StrongConstraint, self).__init__()
        self.coefficients = []
        self.variables = []

    def addTerm(self, coefficient, variable):
        self.coefficients.append(coefficient)
        self.variables.append(variable)

    @abstractclassmethod
    def computeConstraint(self, problem):
        pass

    @abstractclassmethod
    def getMaxValue(self, problem):
        return 0

    @abstractclassmethod
    def getMinValue(self, problem):
        return 0

    def getConstraint(self, problem):
        if len(self.coefficients) > 0 and len(self.coefficients) == len(self.variables):
            self.normalize(problem)
            weight = self.getWeight()
            res = ""
            res += self.coefficients[0] + " " + self.variables[0]
            for i in range(1, len(self.coefficients)):
                res += " + " + str(weight * self.coefficients[i]) + " " + self.variables[i]
            return res
        elif len(self.coefficients) != len(self.variables):
            raise ValueError("Coefficients does not have the same size as variables " +
                             "(" + str(len(self.coefficients)) + "," + str(len(self.variables)) + ")")
        else:
            return ""

    def checkValidities(self, X, Y, S, P, E, R, C, ret=None):
        if ret is None:
            ret = [True, []]
        tp = self.checkValidity(X, Y, S, P, E, R, C)
        tmp = tp[0], tp[1], self.__class__.__name__
        if tmp is not None:
            ret[0] = ret[0] and tmp[0]
            ret[1].append(tmp)

        if self.nextConstraint is not None:
            self.nextConstraint.checkValidities(X, Y, S, P, E, R, C, ret)
        return ret

    @abstractclassmethod
    def checkValidity(self, X, Y, S, P, E, R, C):
        return True, []
