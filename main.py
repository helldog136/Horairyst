import sys
import horairyst.server.server as server

from horairyst.parsers import jsonParser
from horairyst.parsers import csvParser
from horairyst.parsers import xlsParser
import horairyst.problem.constraint as constraint

import os


def importMods():
    #clear old imports
    constraint.clearConstraints()
    # Import mods
    for module in os.listdir("mods"):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__("mods", locals(), globals(), [module[:-3]])
    del module


def check_args(args): #TODO
    return args


if __name__ == "__main__":
    # import horairyst.problem.constraintEditor as constraintEditor
    # print(constraintEditor.getStrongConstraints())
    # constraintEditor.setStrongConstraints(constraintEditor.getStrongConstraints())
    # exit(0)
    from horairyst.solvers import scip
    importMods()
    args = sys.argv
    if(len(args) > 1):
        # console mode
        print("Starting Horairyst in console mode...")
        args = check_args(args)
        ext = "." + args[1].split(".")[-1]

        problem = None
        if ext in csvParser.getHandledExtensions():
            problem = csvParser.parse(args[1])
        elif ext in jsonParser.getHandledExtensions():
            problem = jsonParser.parse(args[1])
        elif ext in xlsParser.getHandledExtensions():
            problem = xlsParser.parse(args[1])

        if problem is None:
            print("Unknown file format:", args[1].split(".")[-1])
            sys.exit(-1)

        res = scip.solve(problem)
        problem.displaySolution()
        print(problem.getSolutionAsJSONMatrix())
        print(problem.checkValidity())
        problem.X[0][2][1] = 1
        problem.X[0][2][0] = 1
        print(problem.checkValidity())
    else:
        # server mode
        print("Starting Horairyst in server mode...")
        server.server()
