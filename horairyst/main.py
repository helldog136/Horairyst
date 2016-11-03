import sys

from flask import Flask, request

from horairyst.parsers import jsonParser
from horairyst.parsers import csvParser
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
    args = sys.argv
    if(len(args) > 1):
        # console mode
        print("Starting Horairyst in console mode...")
        args = check_args(args)
        print(jsonParser.parse("{}"))
        print(csvParser.parse("{}"))
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


        from horairyst.solvers import scip

        scip.solve("/home/helldog136/Dropbox/School/MA2/Projet/scip/test.lp")

        p = Problem(range(3), range(5), range(10), range(30), range(4), constraint.getConstraints())
        print(p.write())
        #app.run(port=8080)
