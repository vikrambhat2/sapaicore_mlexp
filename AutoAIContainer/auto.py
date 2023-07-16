#!/bin/python3
from flask import Flask, jsonify, request
import subprocess
import sys
subprocess.check_call([sys.executable,'-m', 'pip', 'install',  "autoai-libs==1.13.4"])

import joblib
import os
import json
import sklearn
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
#port = int(os.getenv("PORT", 9009))
model = joblib.load("autoai_scikit_model.pkl")
@app.route("/", methods=["GET"])
def vik():

    return "Hello from Vikram!"
    
    
@app.route("/v2/greet", methods=["GET"])
def status():
    global model
    if model is None:
        return "Flask Code: Model was not loaded."
    else:
        return "Model is loaded."
        

@app.route("/v2/predict", methods=["POST"])
def predict():
	
    global model
    payload = request.get_json()
    df=pd.DataFrame(payload)
    
    probs=model.predict_proba(df.values).tolist()
    preds=model.predict(df.values).tolist()
    res =[{'prediction':preds[i], 'probability':probs[i]} for i in range(len(preds))]
    output= {'predictions': res}

    return jsonify(output)


if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=7000)