#!/bin/python3
import os
import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load the machine learning model
model = joblib.load("auto-ai-pipeline.pickle")

@app.route("/", methods=["GET"])
def vik():
    return "This REST API call predicts the demand response of a customer. Use POST /v2/predict with your payload!"

@app.route("/v2/greet", methods=["GET"])
def status():
    global model
    if model is None:
        return "Flask Code: Model was not loaded."
    else:
        return "Demand Response Model is loaded."

@app.route("/v2/predict", methods=["POST"])
def predict():
    global model
    payload = request.get_json()
    payload = payload['input_data'][0]
    df = pd.DataFrame(payload['values'], columns=payload['fields'])
    
    probs = model.predict_proba(df.values).tolist()
    preds = model.predict(df.values).tolist()
    res = [{'prediction': preds[i], 'probability': probs[i]} for i in range(len(preds))]
    output = {
        'predictions': [{
            "fields": ['prediction', 'probability'],
            "values": [[res[i]['prediction'], res[i]['probability']] for i in range(len(res))]
        }]
    }

    return jsonify(output)

if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=7000)
