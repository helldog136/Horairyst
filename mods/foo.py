from horairyst.problem.constraint import Constraint, strongConstraint


@strongConstraint
class Constraint1(Constraint):
    def getConstraint(self, problem):
        return ""

@strongConstraint
class Constraint2(Constraint):
    def getConstraint(self, problem):
        return ""
