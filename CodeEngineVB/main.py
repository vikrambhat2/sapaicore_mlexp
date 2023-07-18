#!/bin/python3
import requests
from flask import Flask, jsonify, request
import os
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
# load model
app = Flask(__name__)


@app.before_first_request
def init():
    return "Main page for Vikram Bhat"

@app.route("/v2/greet", methods=["GET"])
def status():
    return "Model is loaded."
    
@app.route("/v2/predict", methods=["POST"])
def predict():
    global model
    test_input = request.get_json()
    cols=[]
    for i in range(0,3):
        columns=model.named_steps['preprocessor'].transformers_[i][2]
        cols = cols+columns
    df=pd.DataFrame(payload['Input'],columns=payload['Headers'])
    df_score=df[cols].copy()
    result=model.predict_proba(df_score)
    output = {'results': result[0].tolist()[0]}
    return jsonify(output)
    
    

    ai_core_client = AICoreV2Client(
    # `AI_API_URL`
       base_url = "https://api.ai.prod.us-east-1.aws.ml.hana.ondemand.com" + "/v2", # The present SAP AI Core API version is 2
    # `URL`
       auth_url=  "https://ibm-subaccount-us-ro95qjau.authentication.us10.hana.ondemand.com" + "/oauth/token",
    # `clientid`
      client_id = "sb-1fb7b146-d102-4323-a136-4406df71d9bd!b175080|aicore!b164",
    # `clientsecret`
      client_secret = "e059b60a-275e-4c61-8754-ea0431602a04$YhJ1xNLXI4mE1_fMLK9GPR1-8dkigv2DLyKwQlX6r6w="
    )

    deployment_url = "https://api.ai.prod.us-east-1.aws.ml.hana.ondemand.com/v2/inference/deployments/db1da51d03258bed"

    test_input = request.get_json()
    
    endpoint = f"{deployment_url}/v2/predict" # endpoint implemented in serving engine
    headers = {"Authorization": ai_core_client.rest_client.get_token(),
               'ai-resource-group': "default",
               "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=test_input)

    return response.json()

    
    
    
    


if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=5000)