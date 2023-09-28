#!/bin/python3
import os
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson_openscale import APIClient
from ibm_watson_openscale.supporting_classes.enums import DataSetTypes, TargetTypes
from ibm_watson_openscale.supporting_classes.payload_record import PayloadRecord


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

ibmcloudapikey = os.getenv("ibmcloudapikey")
SERVICE_INSTANCE_ID = os.getenv("SERVICE_INSTANCE_ID")
subscription_id = os.getenv("subscription_id")

# Load the machine learning model
model = joblib.load("scikit_model.pkl")

@app.route("/", methods=["GET"])
def vik():
    return "This REST API call predicts the demand response of a customer. \nUse POST /v2/predict with your payload!\nUse POST /v2/feedback_logging with your payload and response to load data into Watson OpenScales feedback_logging table!\nUse POST /v2/payload_logging with your payload to load data and response into Watson OpenScales payload_logging table!"

@app.route("/v2/greet", methods=["GET"])
def status():
    global model
    if model is None:
        return "Flask Code: Model was not loaded."
    else:
        return "Demand Response Model is loaded."

def predict(payload):
    global model
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
    return output

    
@app.route("/v2/predict", methods=["POST"])
def predict_demand_response():

    payload = request.get_json()
    output=predict(payload)
    return jsonify(output)

@app.route("/v2/authenticate", methods=["POST"])
def openscale_authentication():
    try:
        service_credentials = {
        "apikey": ibmcloudapikey,
        "url": "https://api.aiopenscale.cloud.ibm.com"
        }

        authenticator = IAMAuthenticator(
                apikey=service_credentials["apikey"],
                url="https://iam.cloud.ibm.com/identity/token"
            )

        wos_client = APIClient(authenticator=authenticator, service_instance_id=SERVICE_INSTANCE_ID, service_url=service_credentials["url"])
        return wos_client
    except:
        return "Watson OpenScale Client Error"



@app.route("/v2/feedback_logging", methods=["POST"])
def feedback_logging():
    payload = request.get_json()
    predictions=predict(payload)
    feedback_log_req={}
    feedback_log_req['fields']=payload['input_data'][0]['fields']+["DEMAND_RESPONSE"]+["_original_prediction","_original_probability","_debiased_prediction","_debiased_probability"]
    feedback_log_req['values']=[]
    for x in range(len(predictions['predictions'][0]['values'])):
         feedback_log_req['values'].append(payload['input_data'][0]['values'][x]+[int(predictions['predictions'][0]['values'][x][0])]+predictions['predictions'][0]['values'][x]+predictions['predictions'][0]['values'][x])

        
    
    try:
        wos_client = openscale_authentication()
        feedback_dataset_id = wos_client.data_sets.list(type=DataSetTypes.FEEDBACK, target_target_id=subscription_id, target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id


        wos_client.data_sets.store_records(
                data_set_id=feedback_dataset_id,
                request_body=[feedback_log_req],
                background_mode=False
        )
        return "Feedback Logging Successfull"

    except:
        return "Feedback Logging Failed, Please check your watson openscale instance and verify the inputs"



@app.route("/v2/predict_and_log", methods=["POST"])
def predict_and_log():
    payload = request.get_json()
    payload_scoring_request=payload['input_data'][0]
    payload_scoring_request['meta']={'fields':['referrer_gender'], 'values':[[i[8]] for i in payload['input_data'][0]['values']]}
    payload_scoring_response = predict(payload)
    predictions=payload_scoring_response
    feedback_log_req={}
    feedback_log_req['fields']=payload['input_data'][0]['fields']+["DEMAND_RESPONSE"]+["_original_prediction","_original_probability","_debiased_prediction","_debiased_probability"]
    feedback_log_req['values']=[]
    for x in range(len(predictions['predictions'][0]['values'])):
         feedback_log_req['values'].append(payload['input_data'][0]['values'][x]+[int(predictions['predictions'][0]['values'][x][0])]+predictions['predictions'][0]['values'][x]+predictions['predictions'][0]['values'][x])

    wos_client = openscale_authentication()
    payload_logging_data_set_id = wos_client.data_sets.list(type=DataSetTypes.PAYLOAD_LOGGING, target_target_id=subscription_id, target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id

    wos_client.data_sets.store_records(data_set_id=payload_logging_data_set_id, request_body=[PayloadRecord(request=payload_scoring_request, response=payload_scoring_response, response_time=460)])
    print("payload logging successful")
    feedback_dataset_id = wos_client.data_sets.list(type=DataSetTypes.FEEDBACK, target_target_id=subscription_id, target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id


    wos_client.data_sets.store_records(
            data_set_id=feedback_dataset_id,
            request_body=[feedback_log_req],
            background_mode=False
    )
    
    print("feedback logging successful")
    output={"response":"Payload Logging and Feedback logging Successful","model_prediction":payload_scoring_response}


    return jsonify(output)


def openscale_authentication_logging(credentials):
    try:
        service_credentials = {
        "apikey": credentials['ibmcloudapikey'],
        "url": "https://api.aiopenscale.cloud.ibm.com"
        }

        authenticator = IAMAuthenticator(
                apikey=service_credentials["apikey"],
                url="https://iam.cloud.ibm.com/identity/token"
            )

        wos_client = APIClient(authenticator=authenticator, service_instance_id=credentials['SERVICE_INSTANCE_ID'], service_url=service_credentials["url"])
        return wos_client
    except:
        return "Watson OpenScale Client Error"




@app.route("/v2/predict_and_logging", methods=["POST"])
def predict_and_logging():
    payload = request.get_json()
    payload_scoring_request=payload['input_data'][0]
    payload_scoring_request['meta']={'fields':['referrer_gender'], 'values':[[i[8]] for i in payload['input_data'][0]['values']]}
    payload_scoring_response = predict(payload)
    predictions=payload_scoring_response
    feedback_log_req={}
    feedback_log_req['fields']=payload['input_data'][0]['fields']+["DEMAND_RESPONSE"]+["_original_prediction","_original_probability","_debiased_prediction","_debiased_probability"]
    feedback_log_req['values']=[]
    for x in range(len(predictions['predictions'][0]['values'])):
         feedback_log_req['values'].append(payload['input_data'][0]['values'][x]+[int(predictions['predictions'][0]['values'][x][0])]+predictions['predictions'][0]['values'][x]+predictions['predictions'][0]['values'][x])

    wos_client = openscale_authentication_logging(payload['service_credentials'])
    payload_logging_data_set_id = wos_client.data_sets.list(type=DataSetTypes.PAYLOAD_LOGGING, target_target_id=payload['service_credentials']['subscription_id'], target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id

    wos_client.data_sets.store_records(data_set_id=payload_logging_data_set_id, request_body=[PayloadRecord(request=payload_scoring_request, response=payload_scoring_response, response_time=460)])
    print("payload logging successful")
    feedback_dataset_id = wos_client.data_sets.list(type=DataSetTypes.FEEDBACK, target_target_id=payload['service_credentials']['subscription_id'], target_target_type=TargetTypes.SUBSCRIPTION).result.data_sets[0].metadata.id


    wos_client.data_sets.store_records(
            data_set_id=feedback_dataset_id,
            request_body=[feedback_log_req],
            background_mode=False
    )
    
    print("feedback logging successful")
    output={"response":"Payload Logging and Feedback logging Successful","model_prediction":payload_scoring_response}


    return jsonify(output)
   


if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=7000)
