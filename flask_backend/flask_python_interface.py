from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

import os
import time
import json
import logging
import pickle
import io
from base64 import b64encode

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shap


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


class MDClone_EHRTreeHandler:
    def __init__(self):
        with open(
            "./models/MDClone_Diet_Counseling_v1.1/MDClone_DTCv1.2.pickle", "rb"
        ) as fp:
            pickled_tree = pickle.load(fp)
        fp.close()
        self.pickled_tree = pickled_tree
        self.explainer = shap.Explainer(pickled_tree)
        # For shipping images

    def make_prediction(self, data):
        prediction = self.pickled_tree.predict(data)[0]
        shap_values = self.explainer.shap_values(data)
        result = "expected" if prediction == "R" else "not expected"
        # To return an image
        shap.force_plot(
            self.explainer.expected_value[0],
            shap_values[0],
            data.iloc[0],
            matplotlib=True,
            show=False,
        )
        buf = io.BytesIO()
        # XXX?
        # width, height = plt.gcf().get_size_inches()
        # app.logger.debug(f"Image dimensions are {height} x {width}")
        # plt.gcf().set_size_inches(height * 2, width * 2)
        # app.logger.debug(
        #     "Image dimensions are NOW {0} x {1}".format(*(plt.gcf().get_size_inches()))
        # )
        plt.savefig(buf, format="png", bbox_inches="tight")
        b64_image = b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
        return {
            "result": f"This patient is {result} to respond to the intervention based on EHR input",
            "image": b64_image,
        }
        # To return JSONified information
        # fp = shap.force_plot(
        #     self.explainer.expected_value[0], shap_values[0], data.iloc[0]
        # )
        # return {
        #     "result": f"This patient is {result} to respond to the intervention based on EHR input",
        #     "plot": json.dumps(fp.data),
        # }


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

DOWNLOAD_FOLDER = os.path.abspath(os.path.join("./", "models"))
MG_EXAMPLE = os.path.join(DOWNLOAD_FOLDER, "MG_Exercise_v1.1/unknown_response.csv")

EHR_EXAMPLE = os.path.join(
    DOWNLOAD_FOLDER, "MDClone_Diet_Counseling_v1.1/MDClone_unknown3.csv"
)

DOWNLOAD_ENDPOINTS = {
    "mg": MG_EXAMPLE,
    "ehr": EHR_EXAMPLE,
}

app.logger.setLevel(logging.DEBUG)

metagenomic_predictor = MGTreeHandler()
mdclone_ehr_predictor = MDClone_EHRTreeHandler()


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
    if not query or query not in DOWNLOAD_ENDPOINTS.keys():
        return Response(f"Error!")
    try:
        download_path = DOWNLOAD_ENDPOINTS[query]
        extension = download_path.split(".")[-1]
        if extension == "xlsx":
            df = pd.read_excel(download_path)
        elif extension == "csv":
            df = pd.read_csv(download_path)
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
        return jsonify(mdclone_ehr_predictor.make_prediction(df))
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
