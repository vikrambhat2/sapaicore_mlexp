#!/bin/python3
import requests
from flask import Flask, jsonify, request
import os
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
# load model
app = Flask(__name__)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@app.route("/", methods=["GET"])
def home():
    return "This application is deployed on IBM Cloud Engine. The application calls SAP AI Core endpoint to predict demand response "
        
@app.route("/v2/greet", methods=["GET"])
def status():
    if os.getenv("BASEURL"):
        return os.getenv("BASEURL")
    else:
        return "ENV not found"
    
@app.route("/v2/predict", methods=["POST"])
def predict():


    ai_core_client = AICoreV2Client(
    # `AI_API_URL`
       base_url = os.getenv("BASEURL"),
    # `URL`
       auth_url =  os.getenv("AUTHURL"),
    # `clientid`
      client_id = os.getenv("CLIENTID"),
    # `clientsecret`
      client_secret = os.getenv("CLIENTSECRET")
    )

    deployment_url = os.getenv("DEPLOYMENTURL")

    test_input = request.get_json()
    
    test_json={}
    test_json['Headers']=test_input['input_data'][0]['fields']
    test_json['Input']=test_input['input_data'][0]['values']
    
    endpoint = f"{deployment_url}/v2/predict" # endpoint implemented in serving engine
    headers = {"Authorization": ai_core_client.rest_client.get_token(),
               'ai-resource-group': "default",
               "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=test_json)
    response2=response.json()['predictions']
    response3={'predictions': [ {"fields": ['prediction','probability'], "values": [[response2[i]['prediction'], response2[i]['probability']] for i in range(len(response2))]}]}
    return response3  
    
    
    


if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=5000)