from horairyst.problem.constraint import Constraint, newConstraint


@newConstraint
class Constraint1(Constraint):
    def getConstraint(self, problem):
        pass

@newConstraint
class Constraint2(Constraint):
    def getConstraint(self, problem):
        pass
