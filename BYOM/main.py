#!/bin/python3
from flask import Flask, jsonify, request
import pandas as pd
import joblib
import pickle
import os

# load model
app = Flask(__name__)
model = None

@app.before_first_request
def init():
    """
    Load model else crash, deployment will not start
    """
    global model
    model = pickle.load(open ('/mnt/models/scikit_model.pkl','rb')) # All the model files will be read from /mnt/models
    return None

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
    cols=[]
    for i in range(0,3):
        columns=model.named_steps['preprocessor'].transformers_[i][2]
        cols = cols+columns
    df=pd.DataFrame(payload['Input'],columns=payload['Headers'])
    df_score=df[cols].copy()
    result=model.predict_proba(df_score)
    output = {'results': result[0].tolist()[0]}
    return jsonify(output)


if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=3000)