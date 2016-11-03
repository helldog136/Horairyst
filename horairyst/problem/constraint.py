from horairyst.problem.problem import Problem


def getConstraints():
    global constraints
    return constraints

def testConstraint(const):
    S = ["18b6"]
    P = ["08h30", "09h00", "09h30", "10h00", "10h30", "11h00"]
    E = ["Sacha Touille", "Alain Terieur", "Alex Terieur"]
    R = ["J. Wijsen", "H. Melot", "V. Bruyere", "A. Buys"]
    C = [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1]]
    print("Testing your Constraint:", const.__name__, "with:")
    print("S:", S)
    print("P:", P)
    print("E:", E)
    print("R:", R)
    print("C:", C)
    print("-"*80)
    print(const().getConstraint(Problem(S, P, E, R, C, const())))
    exit(0)

def newConstraint(const):
    global constraints
    if constraints is None:
        constraints = const()
    else:
        constraints.addConstraint(const())


from abc import ABC, abstractclassmethod
class Constraint(ABC):
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

constraints = None
