# app.py
import flask
import json
from flask import Flask, request, jsonify
from engine.inference import Inference

app = Flask(__name__)

knowledgeBaseFile = "./data/knowledge.json"
clauseBaseFile = "./data/clause.json"

inferenceEngine = Inference()
inferenceEngine.startEngine(knowledgeBaseFile)


@app.route('/')
def index():
    return "<a href=\"https://assignments-67f1e.web.app\">Enter the system</a>"


@app.route('/clause', methods=['GET'])
def clause():
    file = None
    with open(clauseBaseFile, "r") as file:
        file = json.load(file)
    response = flask. jsonify(file)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/clause', methods=['PUT'])
def update_clause():
    data = request.get_json()
    file = None
    with open(clauseBaseFile, "w") as file:
        json.dump(data, file)
    return 'success'


@app.route('/knowledge', methods=['PUT'])
def update_knowledge():
    data = request.get_json()
    file = None
    with open(knowledgeBaseFile, "w") as file:
        json.dump(data, file)
    return 'success'


@app.route('/think', methods=['POST'])
def think():
    data = request.get_json()
    result = inferenceEngine.inferenceResolve(
        data['q'], data['v'], data['m'])
    return result


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
