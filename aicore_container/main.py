from flask import Flask, jsonify, request
import pandas as pd
import joblib
import pickle
import subprocess
import sys


# load model
model = joblib.load("model/scikit_model.pkl")

app = Flask(__name__)
#port = int(os.getenv("PORT", 9009))

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