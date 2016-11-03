from flask import Flask, request


class Server(object):
    def __init__(self, port=8042):
        self.port = port

        self.app = Flask(__name__)
        self.app.run(port=port)

        @self.app.route('/po')
        def post():
            if 'name' in request.args:
                return "hello" + request.args['name']
            else:
                return "prout"
