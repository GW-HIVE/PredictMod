from flask import Flask, request, Response, send_from_directory
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
        with open("pickled_tree.pickle", "rb") as fp:
            self.pickled_tree = pickle.load(fp)
        fp.close()

    def make_prediction(self, data):
        prediction = self.pickled_tree.predict(data)[0]
        if prediction == 'R':
            return "This patient is expected to respond to the intervention"
        return "This patient is not expected to respond to the intervention"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.path.dirname(app.instance_path), "downloads")

app.logger.setLevel(logging.DEBUG)

metagenomic_predictor = MGTreeHandler()

@app.route("/metagenomic-download", methods=["GET"])
@cross_origin()
def mg_download():
    try:
        app.logger.debug("MG: Received download request")
        app.logger.debug(f"MG: Upload dir is {app.config['DOWNLOAD_FOLDER']}")
        app.logger.debug("")
        app.logger.debug(f"\tSearching: {os.path.join(app.config['DOWNLOAD_FOLDER'], 'single_patient_data_1.xls')}")
        app.logger.debug("")
        
        return send_from_directory(
            app.config["DOWNLOAD_FOLDER"], 
            "single_patient_data_1.xls", 
            as_attachment=True,
            mimetype="application/vnd.ms-excel"
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


@app.route("/mg-upload", methods=["POST"])
@cross_origin()
def mg_request():
    try:
        # XXX
        # app.logger.debug(f"---> Collected request at >>> MG <<<")
        # app.logger.debug(f"---> Method is {request.method}")
        raw_data = json.loads(request.get_json()['json'])
        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)
        df = df.drop(["Status"], axis=1)
        # app.logger.debug(f"---> JSON Data:\n{df}")

        return metagenomic_predictor.make_prediction(df)

    except Exception as e:
        app.logger.debug(f"--->>> Exception!\n{e}")
        return Response(f"Got an error!\n\t{e}")

    return Response("Metagenomic Analysis: Analysis Loop Completed\n")


@app.route("/ehr-upload", methods=["POST"])
@cross_origin()
def request_received():
    try:
        # XXX
        # app.logger.debug(f"---> Collected request at >>> EHR <<<")
        json_package = json.loads(request.get_json()['json'])
        # TODO: Next steps!
    except Exception as e:
        return Response(f"Got an error!\n\t{e}")
    return Response("EHR: Python (Shim) Analysis Loop Completed\n")
