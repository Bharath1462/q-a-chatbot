# serve.py
from flask import Flask, request, jsonify
from interface import model_fn, predict_fn

app = Flask(__name__)
model = model_fn("/opt/ml/model")

@app.route("/invocations", methods=["POST"])
def invoke():
    data = request.get_json()
    prediction = predict_fn(data, model)
    return jsonify(prediction)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

