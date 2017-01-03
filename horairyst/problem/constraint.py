from horairyst.problem.problem import Problem
from abc import ABCMeta, abstractclassmethod


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


def testConstraint(const, pb, xit=True):
    if pb is None:
        S = ["18b6", "0a07"]
        P = ["08h30", "09h00", "09h30", "10h00", "10h30", "11h00"]
        E = ["Sacha Touille", "Alain Terieur", "Alex Terieur"]
        R = ["J. Wijsen", "H. Melot", "V. Bruyere", "A. Buys"]
        C = [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1]]
        pb = Problem(S, P, E, R, C, const(), const())
    print("Testing your Constraint:", const.__name__, "with:")
    print("S:", pb.S, "(size: ", len(pb.S), ")")
    print("P:", pb.P, "(size: ", len(pb.P), ")")
    print("E:", pb.E, "(size: ", len(pb.E), ")")
    print("R:", pb.R, "(size: ", len(pb.R), ")")
    print("C:", pb.C, "(size: ", len(pb.C), ")")
    print("|X|:", len(pb.X), "x", len(pb.X[0]), "x", len(pb.X[0][0]))
    print("|Y|:", len(pb.Y), "x", len(pb.Y[0]), "x", len(pb.Y[0][0]))
    print("-"*80)
    print(const().getConstraint(pb))
    if xit:
        exit(0)


class Constraint(metaclass=ABCMeta):
    def __init__(self):
        self.nextConstraint = None

    def addConstraint(self, _nextConstraint):
        if self.nextConstraint is None:
            self.nextConstraint = _nextConstraint
        else:
            self.nextConstraint.addConstraint(_nextConstraint)

    def getAll(self, problem, ret=None):
        print(problem)
        if ret is None:
            ret = []
        cst = self.getConstraint(problem)
        if cst is not None:
            ret.append(cst)
        if self.nextConstraint is not None:
            self.nextConstraint.getAll(problem, ret)
        return ret

    @abstractclassmethod
    def getConstraint(self, problem):
        pass

strongConstraints = None
weakConstraints = None
