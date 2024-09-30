from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import tomli
import os
import logging

from model_handlers import (
    MDClone_EHRTreeHandler,
    MGTreeHandler,
    Diabetes_EHR_Handler,
    Epilepsy_Microbiome_Handler,
)

# TODO: Documentation

import numpy as np
import pandas as pd

MODELS_DIR = "models"

DETAIL_LOOKUP = {
    "MDClone-Diet-Counseling": "MDClone_Diet_Counseling_v1.1/README.md",
    "MG-Exercise": "MG_Exercise_v1.1/README.md",
    "Diabetes_EHR": "Diabetes_EHR_v1/README.md",
    "Epilepsy_classifier": "Epilepsy_microbiome_v1/README.md",
}

DOWNLOAD_LOOKUP = {
    "MDClone-Diet-Counseling": "MDClone_Diet_Counseling_v1.1/MDClone_unknown3.csv",
    "MG-Exercise": "MG_Exercise_v1.1/unknown_response.csv",
    "Diabetes_EHR": "Diabetes_EHR_v1/single_patient_input.xlsx",
    "Epilepsy_classifier": "Epilepsy_microbiome_v1/single_patient_sample.xlsx",
}

HANDLERS = {
    "MDClone-Diet-Counseling": MDClone_EHRTreeHandler(),
    "MG-Exercise": MGTreeHandler(),
    "Diabetes_EHR": Diabetes_EHR_Handler(),
    "Epilepsy_classifier": Epilepsy_Microbiome_Handler(),
}

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.logger.setLevel(logging.DEBUG)

with open(".env", "rb") as config_p:
    config = tomli.load(config_p)

FLASK_MODE = config["mode"]


@app.route("/model-details", methods=["GET"])
def model_details():
    query = request.args.get("q", None)
    app.logger.debug(f"Found detail request arg: {query}")
    if query not in DETAIL_LOOKUP.keys():
        if FLASK_MODE != "dev":
            return jsonify(
                {"details": f"## _Model details for {query} are coming soon!_"}
            )
        return jsonify(
            {
                "details": f"## Flask mode {FLASK_MODE} detected; models may be incorrectly shown as 'missing'"
            }
        )
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
    if not query:
        return jsonify({"error": f"Error! No query found"})
    try:
        if query not in DOWNLOAD_LOOKUP.keys():
            if FLASK_MODE != "dev":
                return jsonify(
                    {"error": f"Download for unknown model {query} not available"}
                )
            return jsonify(
                {
                    "error": f"Flask mode is {FLASK_MODE}; no downloads for {query} available"
                }
            )
        download_path = os.path.join(MODELS_DIR, DOWNLOAD_LOOKUP[query])
        extension = download_path.split(".")[-1]
        if extension == "xlsx":
            df = pd.read_excel(download_path)
        elif extension == "csv":
            df = pd.read_csv(download_path)
        elif extension == "tsv":
            df = pd.read_csv(download_path, sep="\t")
        else:
            return jsonify({"error": f"Unsupported extension {extension}"}, status=500)
        return jsonify(df.to_json(orient="records"))
    except Exception as e:
        app.logger.debug(f"Exception: {e}")
        return jsonify({"error": f"Flask exception: {e}"})


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
        if FLASK_MODE == "dev":
            return jsonify(
                {
                    "error": f"Flask mode is {FLASK_MODE}; uploads to {target} aren't supported"
                }
            )
        app.logger.debug("*" * 40)
        app.logger.debug(f"Target: {target}")
        app.logger.debug(f"Keys: {[k for k in HANDLERS.keys()]}")
        app.logger.debug("*" * 40)
        return jsonify({"error": "Illegal upload target error"})
    else:
        raw_data = request.get_json()
        return jsonify(HANDLERS[target].make_prediction(raw_data))
