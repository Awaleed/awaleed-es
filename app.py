# app.py
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
    return "<h1>Welcome to our server !!</h1>"


@app.route('/clause', methods=['GET'])
def clause():
    file = None
    with open(clauseBaseFile, "r") as file:
        file = json.load(file)
    return jsonify(file)


@app.route('/think', methods=['POST'])
def think():
    data = request.get_json()
    result = inferenceEngine.inferenceResolve(
        data['q'], data['v'], data['m'])
    return result


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
