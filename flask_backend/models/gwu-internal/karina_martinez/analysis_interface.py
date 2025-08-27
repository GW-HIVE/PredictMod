from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import json
import tomli
import os
import logging
import uuid

from pathlib import Path

from Diabetes_glycomic import Diabetes_Glycomic_Handler
from ccRCC_glycoproteomic import ccRCC_ClassifierHandler

# TODO: Documentation

import numpy as np
import pandas as pd

MODELS_DIR = "./"

DETAIL_LOOKUP = {
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic/",
    "Diabetes-Glycomic": "Diabetes_glycomic/",
}

DOWNLOAD_LOOKUP = {
    "ccRCC-Glycoproteomic": "ccRCC_glycoproteomic/example_input.csv",
    "Diabetes-Glycomic": "Diabetes_glycomic/example_input.csv",
}

HANDLERS = {
    "ccRCC-Glycoproteomic": ccRCC_ClassifierHandler(),
    "Diabetes-Glycomic": Diabetes_Glycomic_Handler(),
}

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.logger.setLevel(logging.DEBUG)

with open(".env", "rb") as config_p:
    config = tomli.load(config_p)

FLASK_MODE = config["mode"]

if FLASK_MODE == "dev":
    SHARED_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "user_data"
    app.logger.debug(f"\n---> Shared dir: {SHARED_DIR}\n")
else:
    SHARED_DIR = "/user_data"

@app.route("/model-details", methods=["GET"])
def model_details():
    query = request.args.get("q", None)
    app.logger.debug(f"Found detail request arg: {query}")
    if query not in DETAIL_LOOKUP.keys():
        return jsonify({"details": f"## _Model details for {query} are coming soon!_"})
    try:
        details_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query], "README.md")
        metadata_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query], "metadata.json")
        with open(details_path, "r") as fp:
            raw_markdown = fp.read()
        with open(metadata_path, "r") as fp:
            metadata = json.load(fp)
        return jsonify({"details": raw_markdown, "metadata": metadata})
    except Exception as e:
        app.logger.critical(f"---> Exception {e} <---")
        app.logger.critical(f"Query: {query}")
        app.logger.critical(f"File path: {details_path}")
        app.logger.critical(f"Current path: {os.getcwd()}")
        app.logger.critical("-" * 60)
        return jsonify({"error": "Flask error. See logs"})


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
    file_name = request.args.get("file_name", None)
    user = request.args.get("user", None)

    if file_name is None:
        return jsonify({"error": "No file path or user found in request"})
    file_path = ""
    file_extension = ""
    if file_name == "example":
        file_path = os.path.join(MODELS_DIR, DOWNLOAD_LOOKUP[target])
        file_extension = file_path.split(".")[-1]
    else:
        file_path = os.path.join(SHARED_DIR, f"{user}/{file_name}")
        file_extension = file_name.split(".")[1]
    # app.logger.debug(f"---> Reading data from {file_path} (found file extension {file_extension})")

    # file_extension = file_name.split(".")[1]
    if file_extension == "csv":
        data = pd.read_csv(file_path)
    elif file_extension == "xlsx" or file_extension == "xls":
        data = pd.read_excel(file_path)
    elif file_extension == "tsv":
        data = pd.read_csv(file_path, sep="\t")

    if target not in HANDLERS.keys():
        app.logger.debug("*" * 40)
        app.logger.debug(f"Target: {target}")
        app.logger.debug(f"Keys: {[k for k in HANDLERS.keys()]}")
        app.logger.debug("*" * 40)
        return jsonify({"error": "Illegal upload target error"})
    else:
        return jsonify(HANDLERS[target].make_prediction(data))
