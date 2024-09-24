from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import os
import logging

from Diabetes_glycomic import Diabetes_Glycomic_Handler
from ccRCC_glycoproteomic import ccRCC_ClassifierHandler

# TODO: Documentation

import numpy as np
import pandas as pd

MODELS_DIR = "models"

DETAIL_LOOKUP = {
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic_v1/README.md",
    "Diabetes-Glycomic": "Diabetes_glycomic_v1/README.md",
}

DOWNLOAD_LOOKUP = {
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic_v1/example_input.csv",
    "Diabetes-Glycomic": "Diabetes_glycomic_v1/example_input.csv",
}

HANDLERS = {
    "ccRCC-Glycoproteomic": ccRCC_ClassifierHandler(),
    "Diabetes-Glycomic": Diabetes_Glycomic_Handler(),
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
    try:
        details_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query])
        with open(details_path, "r") as fp:
            raw_markdown = fp.read()
        return jsonify({"details": raw_markdown})
    except Exception as e:
        app.logger.critical(f"---> Exception {e} <---")
        app.logger.critical(f"Query: {query}")
        app.logger.critical(f"File path: {details_path}")
        app.logger.critical("-" * 60)
        return jsonify({"error": "Flask error. See logs"}, status=500)


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
