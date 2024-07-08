from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import os
import time
import json
import logging
import pickle
import io

from model_handlers import (
    MDClone_EHRTreeHandler,
    MGTreeHandler,
    ccRCC_ClassifierHandler,
    Diabetes_EHR_Handler,
    Diabetes_Glycomic_Handler,
    Epilepsy_Microbiome_Handler,
)

# from base64 import b64encode

import numpy as np
import pandas as pd

# import matplotlib
# import matplotlib.pyplot as plt
# import shap

MODELS_DIR = "models"

DETAIL_LOOKUP = {
    "MDClone-Diet-Exercise": "MDClone_Diet_Counseling_v1.1/README.md",
    "MG-Exercise": "MG_Exercise_v1.1/README.md",
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic_v1/README.md",
    "Diabetes_EHR": "Diabetes_EHR_v1/README.md",
    "Diabetes-Glycomic": "Diabetes_glycomic_v1/README.md",
    "Epilepsy_classifier_1.1": "Epilepsy_microbiome_v1/README.md",
}

DOWNLOAD_LOOKUP = {
    "MDClone-Diet-Exercise": "MDClone_Diet_Counseling_v1.1/MDClone_unknown3.csv",
    "MG-Exercise": "MG_Exercise_v1.1/unknown_response.csv",
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic_v1/example_input.csv",
    "Diabetes_EHR": "Diabetes_EHR_v1/single_patient_input.xlsx",
    "Diabetes-Glycomic": "Diabetes_glycomic_v1/example_input.csv",
    "Epilepsy_classifier_1.1": "Epilepsy_microbiome_v1/single_patient_sample.xlsx",
}

HANDLERS = {
    "MDClone-Diet-Exercise": MDClone_EHRTreeHandler(),
    "MG-Exercise": MGTreeHandler(),
    "ccRCC-Glycoproteomic": ccRCC_ClassifierHandler(),
    "Diabetes_EHR": Diabetes_EHR_Handler(),
    "Diabetes-Glycomic": Diabetes_Glycomic_Handler(),
    "Epilepsy_classifier_1.1": Epilepsy_Microbiome_Handler(),
}

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.logger.setLevel(logging.DEBUG)


@app.route("/model-details", methods=["GET"])
def model_details():
    query = request.args.get("q", None)
    app.logger.debug(f"Found detail request arg: {query}")
    if query not in DETAIL_LOOKUP.keys():
        return jsonify({"details": f"## _Model details for {query} are coming soon!_"})
    details_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query])
    with open(details_path, "r") as fp:
        raw_markdown = fp.read()
    return jsonify({"details": raw_markdown})


@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("query", None)
    app.logger.debug(f"Found request arg: {query}")
    data = None
    if query == "model-test":
        data = [
            {"name": "Factor 1", "value": 42},
            {"name": "Factor 2", "value": 25},
            {"name": "Factor 3", "value": -12},
        ]
    return jsonify(data)


@app.route("/download", methods=["GET"])
@cross_origin()
def download():
    query = request.args.get("q", None)
    if not query or query not in DOWNLOAD_LOOKUP.keys():
        return Response(f"Error!")
    try:
        download_path = os.path.join(MODELS_DIR, DOWNLOAD_LOOKUP[query])
        extension = download_path.split(".")[-1]
        if extension == "xlsx":
            df = pd.read_excel(download_path)
        elif extension == "csv":
            df = pd.read_csv(download_path)
        elif extension == "tsv":
            df = pd.read_csv(download_path, sep="\t")
        else:
            return Response(f"Unsupported extension {extension}", status=500)
        return jsonify(df.to_json(orient="records"))
    except Exception as e:
        app.logger.debug(f"Exception: {e}")
        return Response(f"Error! {e}")


@app.route("/ping", methods=["GET"])
def ping():
    try:
        req = request
        return Response("PONG\n")
    except Exception as e:
        app.logger.debug(f"---> Exception!!\n{e}")
        return Response(f"ERROR: {e}")


@app.route("/upload", methods=["POST"])
def upload():
    target = request.args.get("q", None)
    if target not in HANDLERS.keys():
        app.logger.debug("*" * 40)
        app.logger.debug(f"Target: {target}")
        app.logger.debug(f"Keys: {[k for k in HANDLERS.keys()]}")
        app.logger.debug("*" * 40)
        return jsonify({"error": "Illegal upload target error"})
    else:
        raw_data = request.get_json()
        return jsonify(HANDLERS[target].make_prediction(raw_data))
    # if target == "mg":
    #     raw_data = request.get_json()
    #     headers, data = raw_data[0], np.array([raw_data[1]])
    #     df = pd.DataFrame(data, columns=headers)
    #     df = df.drop(["Status"], axis=1)
    #     return jsonify({"result": metagenomic_predictor.make_prediction(df)})
    # elif target == "ehr":
    #     raw_data = request.get_json()
    #     headers, data = raw_data[0], np.array([raw_data[1]])
    #     df = pd.DataFrame(data, columns=headers)
    #     return jsonify(mdclone_ehr_predictor.make_prediction(df))
    # else:
    #     return jsonify({"error": "Illegal upload target error"}, status=404)


@app.route("/mg-upload", methods=["POST"])
@cross_origin()
def mg_request():
    try:
        # XXX
        app.logger.debug(f"---> Collected request at >>> MG <<<")
        # app.logger.debug(f"---> Method is {request.method}")

        raw_data = request.get_json()

        app.logger.debug(raw_data)

        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)
        df = df.drop(["Status"], axis=1)
        # app.logger.debug(f"---> JSON Data:\n{df}")

        return jsonify(metagenomic_predictor.make_prediction(df))

    except Exception as e:
        app.logger.debug(f"--->>> Exception!\n{e}")
        return jsonify({"error": f"Got an error!\n\t{e}"})


@app.route("/ehr-upload", methods=["POST"])
@cross_origin()
def ehr_request():
    try:
        app.logger.debug(f"---> Collected request at >>> EHR <<<")
        raw_data = request.get_json()
        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)

        return jsonify({"result": mdclone_ehr_predictor.make_prediction(df)})

    except Exception as e:
        app.logger.debug(f"--->>> Exception!\n{e}")
        return jsonify({"error": f"Got an error!  ---> {e}"})
