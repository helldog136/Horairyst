from flask import Flask, request, Response
from flask_cors import CORS, cross_origin, logging


from horairyst.parsers import jsonParser
from horairyst.parsers import csvParser
from horairyst.parsers import xlsParser

from horairyst.solvers import scip

from horairyst.problem.problem import Problem
from horairyst.problem import constraintEditor

import json


def server():
    from werkzeug.utils import secure_filename

    UPLOAD_FOLDER = '/tmp'
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'xls'}

    app = Flask(__name__)
    cors = CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    logging.getLogger('flask_cors').level = logging.DEBUG

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/file', methods=['POST', 'OPTIONS'])
    #@cross_origin(origin="http://localhost:3001")
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
                elif ext in jsonParser.getHandledExtensions():
                    problem = jsonParser.parse(finalfile)
                elif ext in xlsParser.getHandledExtensions():
                    problem = xlsParser.parse(finalfile)

                if problem is None:
                    print("Unknown file format:", finalfile.split(".")[-1])
                    return Response(status=403, response="Wrong file format")

                scip.solve(problem)
                problem.displaySolution()
                print(problem.getCompleteJson())
                return Response(response=json.dumps(problem.getCompleteJson()), status=200)
            else:
                return Response(status=403, response="Wrong file format")
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/checkMatrix', methods=['POST', 'OPTIONS'])
    # @cross_origin(origin="http://localhost:3001")
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
    # @cross_origin(origin="http://localhost:3001")
    def reoptimize_schedule():
        if request.method == 'POST':
            jsonReq = request.get_json()
            print(jsonReq)
            print(jsonReq['matrix'])
            pb = Problem.fromJsonMatrix(jsonReq)
            print(pb.getCompleteJson())
            scip.solve(pb)
            pb.displaySolution()
            print(pb.getCompleteJson())
            return Response(status=200, response=json.dumps(pb.getCompleteJson()))
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/strongconstraints', methods=['OPTIONS', 'POST', 'GET'])
    def change_strong_constraints():
        if request.method == 'POST':
            constraintEditor.setStrongConstraints(request.get_json())
            return Response(status=200, response="OK")
        elif request.method == 'GET':
            return Response(status=200, response=constraintEditor.getStrongConstraints())
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    @app.route('/weakconstraints', methods=['OPTIONS', 'POST', 'GET'])
    def change_weak_constraints():
        if request.method == 'POST':
            constraintEditor.setWeakConstraints(request.get_json())
            return Response(status=200, response="OK")
        elif request.method == 'GET':
            return Response(status=200, response=constraintEditor.getWeakConstraints())
        elif request.method == 'OPTIONS':
            return Response(status=200)
        return Response(status=400, response="Wrong method")

    app.run(port=4722, host="0.0.0.0")
