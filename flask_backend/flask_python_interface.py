from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import os
import time
import json
import logging
import pickle

import numpy as np
import pandas as pd
import io


class MGTreeHandler:
    def __init__(self):
        with open("pickled_mg_tree.pickle", "rb") as fp:
            self.pickled_tree = pickle.load(fp)
        fp.close()

    def make_prediction(self, data):
        prediction = self.pickled_tree.predict(data)[0]
        if prediction == "R":
            return "This patient is expected to respond to the intervention based on Metagenomic input"
        return "This patient is not expected to respond to the intervention based on Metagenomic input"


class EHRTreeHandler:
    def __init__(self):
        with open("pickled_ehr_tree.pickle", "rb") as fp:
            self.pickled_tree = pickle.load(fp)
        fp.close()

    def make_prediction(self, data):
        prediction = self.pickled_tree.predict(data)[0]
        if prediction == "R":
            return "This patient is expected to respond to the intervention based on EHR input"
        return "This patient is not expected to respond to the intervention based on EHR input"


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["DOWNLOAD_FOLDER"] = os.path.join(
    os.path.dirname(app.instance_path), "models"
)

app.logger.setLevel(logging.DEBUG)

metagenomic_predictor = MGTreeHandler()
ehr_predictor = EHRTreeHandler()


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


@app.route("/metagenomic-download", methods=["GET"])
@cross_origin()
def mg_download():
    try:
        app.logger.debug("MG: Received download request")
        app.logger.debug(f"MG: Upload dir is {app.config['DOWNLOAD_FOLDER']}")
        app.logger.debug("")
        app.logger.debug(
            f"\tSearching: {os.path.join(app.config['DOWNLOAD_FOLDER'], 'single_patient_data_1.xls')}"
        )
        app.logger.debug("")

        return send_from_directory(
            app.config["DOWNLOAD_FOLDER"],
            "single_patient_data_1.xls",
            as_attachment=True,
            mimetype="application/vnd.ms-excel",
        )
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
    if target == "mg":
        raw_data = request.get_json()
        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)
        df = df.drop(["Status"], axis=1)
        return jsonify({"result": metagenomic_predictor.make_prediction(df)})
    elif target == "ehr":
        raw_data = request.get_json()
        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)
        return jsonify({"result": ehr_predictor.make_prediction(df)})
    else:
        return jsonify({"error": "Illegal upload target error"}, status=404)


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

        return jsonify({"result": metagenomic_predictor.make_prediction(df)})

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

        return jsonify({"result": ehr_predictor.make_prediction(df)})

    except Exception as e:
        app.logger.debug(f"--->>> Exception!\n{e}")
        return jsonify({"error": f"Got an error!  ---> {e}"})
