import sys

from flask import Flask, request

from horairyst.parsers import jsonParser
from horairyst.parsers import csvParser
from horairyst.parsers import xlsParser
from horairyst.problem.problem import Problem
from horairyst.problem import constraint

import os
for module in os.listdir("mods"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("mods", locals(), globals(), [module[:-3]])
del module


def check_args(args):
    return args


if __name__ == "__main__":
    from horairyst.solvers import scip
    args = sys.argv
    if(len(args) > 1):
        # console mode
        print("Starting Horairyst in console mode...")
        args = check_args(args)
        ext = "."+ args[1].split(".")[-1]

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
    else:
        # server mode
        print("Starting Horairyst in server mode...")

        app = Flask(__name__)


        @app.route('/po', methods=['POST'])
        def post():
            if 'name' in request.args:
                return "hello" + request.args['name']
            else:
                return "prout"



        #scip.solve("/home/helldog136/Dropbox/School/MA2/Projet/scip/test.lp")

        S = ["18b6", "0a07"]
        P = ["08h30", "09h00", "09h30", "10h00", "10h30", "11h00"]
        E = ["Sacha Touille", "Alain Terieur", "Alex Terieur"]
        R = ["J. Wijsen", "H. Melot", "V. Bruyere", "A. Buys"]
        C = [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1]]

        p = Problem(S, P, E, R, C, constraint.getStrongConstraints(), constraint.getWeakConstraints())
        #print(p.write())

        res = scip.solve(p)
        p.displaySolution(res)
        #app.run(port=8080)
