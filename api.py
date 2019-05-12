import flask
import json
from flask import render_template
import random as rd
from flask import request

app = flask.Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<path:fullurl>", methods=['GET', 'POST'])
def main(fullurl):
    height, width = [int(e) for e in fullurl.split('/')]
    jsonResponse = json.loads(request.data.decode('utf-8'))

    # print(request.data.get('image', ''))
    response = flask.jsonify({
        'number': rd.randint(0, 9),
        'height': height,
        'width': width,
        'image': jsonResponse['image']
        })
    return response



# from flask_cors import CORS, cross_origin
# CORS(app)
# @app.route("/<path:fullurl>", methods=['GET'])
# @cross_origin()
# def main(fullurl):
#
#     height, width, n = [int(e) for e in fullurl.split('/')]
#     svg = motif(height, width, n)
#     response = flask.jsonify({'svg': svg})
#     return response
