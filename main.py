from flask import Flask, request

from parsers import jsonParser, csvParser
import sys


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
        from solvers import scip
        scip.solve("/home/helldog136/Dropbox/School/MA2/Projet/scip/sampleProblem2.lp")

        #app.run(port=8080)
