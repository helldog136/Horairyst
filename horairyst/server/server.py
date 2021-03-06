from flask import Flask, request, Response
from flask_cors import CORS, cross_origin, logging


from horairyst.parsers import csvParser
from horairyst.parsers import xlsParser

from horairyst.solvers import scip

from horairyst.problem.problem import Problem
from horairyst.problem import constraintEditor

import json

from horairyst.solvers.scip import InfeasibleError


def server():
    from werkzeug.utils import secure_filename

    UPLOAD_FOLDER = '/tmp'
    ALLOWED_EXTENSIONS = {'csv', 'xls'}

    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    logging.getLogger('flask_cors').level = logging.DEBUG

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/file', methods=['POST', 'OPTIONS'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return Response(status=403, response="Missing File in Request")
            file = request.files['file']
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save("/tmp/" + filename)

                finalfile = "/tmp/" + filename
                ext = "." + finalfile.split(".")[-1]

                problem = None
                if ext in csvParser.getHandledExtensions():
                    problem = csvParser.parse(finalfile)
                elif ext in xlsParser.getHandledExtensions():
                    problem = xlsParser.parse(finalfile)

                if problem is None:
                    print("Unknown file format:", finalfile.split(".")[-1])
                    return Response(status=403, response="Wrong file format")

                try:
                    scip.solve(problem)
                    problem.displaySolution()
                    print(problem.getCompleteJson())
                    return Response(response=json.dumps(problem.getCompleteJson()), status=200)
                except InfeasibleError:
                    return Response(status=200, response=json.dumps({"status": "infeasible"}))
            else:
                return Response(status=403, response="Wrong file format")
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/checkMatrix', methods=['POST', 'OPTIONS'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def check_schedule():
        if request.method == 'POST':
            jsonReq = request.get_json()
            print(jsonReq)
            print(jsonReq['matrix'])
            pb = Problem.fromJsonMatrix(jsonReq)
            return Response(status=200, response=json.dumps(pb.getCompleteJson()))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/reoptimize', methods=['POST', 'OPTIONS'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def reoptimize_schedule():
        if request.method == 'POST':
            jsonReq = request.get_json()
            print(jsonReq)
            print(jsonReq['matrix'])
            pb = Problem.fromJsonMatrix(jsonReq)
            print(pb.getCompleteJson())
            try:
                scip.solve(pb)
                pb.displaySolution()
                print(pb.getCompleteJson())
                return Response(status=200, response=json.dumps(pb.getCompleteJson()))
            except InfeasibleError:
                return Response(status=200, response=json.dumps({}))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/strongconstraints', methods=['OPTIONS', 'POST', 'GET'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def change_strong_constraints():
        if request.method == 'POST':
            constraintEditor.setStrongConstraints(request.get_json())
            return Response(status=200, response="OK")
        elif request.method == 'GET':
            return Response(status=200, response=json.dumps(constraintEditor.getStrongConstraints()))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/weakconstraints', methods=['OPTIONS', 'POST', 'GET'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def change_weak_constraints():
        if request.method == 'POST':
            constraintEditor.setWeakConstraints(request.get_json())
            return Response(status=200, response="OK")
        elif request.method == 'GET':
            return Response(status=200, response=json.dumps(constraintEditor.getWeakConstraints()))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/sampleinput', methods=['OPTIONS', 'GET'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def get_sample_input():
        if request.method == 'GET':
            file = open("sampleInput.csv", 'r')
            res = ""
            for line in file:
                res += line + ("\n" if not line.endswith("\n") else "")
            return Response(status=200, response=str(res))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/reloadMods', methods=['GET'])
    # @cross_origin(origin="http://horairyst.deweireld.be")
    def reload_mods():
        if request.method == 'GET':
            import main
            main.importMods()
            return Response(status=200, response="OK")
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    app.run(port=4242, host="0.0.0.0")
