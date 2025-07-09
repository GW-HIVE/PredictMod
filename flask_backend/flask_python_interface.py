from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import JSON

import json
import tomli
import os
import logging
import uuid

from pathlib import Path

from model_handlers import (
    MDClone_EHRTreeHandler,
    MGTreeHandler,
    Diabetes_EHR_Handler,
    Epilepsy_Microbiome_Handler,
    EC_EHR_Keto_ModelHandler,
    OCMethylationPredictor,
    OCRNASeqPredictor,
    MDClone_Exercise_Classifier,
    MDCloneSemaglutideHandler,
    PrediabetesProteomicsHandler,
    Track2Better_Handler,
)

# TODO: Documentation

import numpy as np
import pandas as pd

MODELS_DIR = "models"

DETAIL_LOOKUP = {
    "MDClone-Diet-Counseling": "MDClone_Diet_Counseling_v1.1/",
    "MG-Exercise": "MG_Exercise_v1.1/",
    "Diabetes_EHR": "Diabetes_EHR_v1/",
    "Epilepsy_classifier": "Epilepsy_microbiome_v1/",
    "Predictmod_EHR_Keto": "PredictMod_EHR_Keto_v1.0/",
    "Ovarian-Cancer-Methylation": "ovarian_cancer_methylation/",
    "Ovarian-Cancer-RNAseq": "ovarian_rnaseq/",
    "MDClone-Exercise": "mdclone_exercise/",
    "MDClone-Semaglutide": "mdclone_semaglutide/",
    "Prediabetes-Proteomics": "prediabetes_proteomics/",
    "Predictmod_Track2Better": "Predictmod_Track2Better/", 
}

DOWNLOAD_LOOKUP = {
    "MDClone-Diet-Counseling": "MDClone_Diet_Counseling_v1.1/MDClone_unknown3.csv",
    "MG-Exercise": "MG_Exercise_v1.1/unknown_response.csv",
    "Diabetes_EHR": "Diabetes_EHR_v1/single_patient_input.xlsx",
    "Epilepsy_classifier": "Epilepsy_microbiome_v1/single_patient_sample.xlsx",
    "Predictmod_EHR_Keto": "PredictMod_EHR_Keto_v1.0/svm_sample.csv",
    "Ovarian-Cancer-Methylation": "ovarian_cancer_methylation/Ovarian-Cancer-Methylation.csv",
    "Ovarian-Cancer-RNAseq": "ovarian_rnaseq/ovarian_RNAseq_single_patient.xlsx",
    "MDClone-Exercise": "mdclone_exercise/single_patient_mdclone_exercise.csv",
    "MDClone-Semaglutide": "mdclone_semaglutide/Single_patient_semaglutide.csv",
    "Prediabetes-Proteomics": "prediabetes_proteomics/prediabetes_proteomics_single_patient.csv",
    "Predictmod_Track2Better": "Predictmod_Track2Better/test_set.csv", 
}

HANDLERS = {
    "MDClone-Diet-Counseling": MDClone_EHRTreeHandler(),
    "MG-Exercise": MGTreeHandler(),
    "Diabetes_EHR": Diabetes_EHR_Handler(),
    "Epilepsy_classifier": Epilepsy_Microbiome_Handler(),
    "Predictmod_EHR_Keto": EC_EHR_Keto_ModelHandler(),
    "Ovarian-Cancer-Methylation": OCMethylationPredictor(),
    "Ovarian-Cancer-RNAseq": OCRNASeqPredictor(),
    "MDClone-Exercise": MDClone_Exercise_Classifier(),
    "MDClone-Semaglutide": MDCloneSemaglutideHandler(),
    "Prediabetes-Proteomics": PrediabetesProteomicsHandler(),
    "Predictmod_Track2Better": Track2Better_Handler(), 
}


# class Base(DeclarativeBase):
#     pass


# db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///predictmod.db"

# db.init_app(app)

app.logger.setLevel(logging.DEBUG)


# class UploadedSample(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(unique=False)
#     file_path: Mapped[str] = mapped_column(unique=True)
#     # md5sum: Mapped[str] = mapped_column()


# with app.app_context():
#     db.create_all()

with open(".env", "rb") as config_p:
    config = tomli.load(config_p)

FLASK_MODE = config["mode"]

if FLASK_MODE == "dev":
    SHARED_DIR = Path(__file__).resolve().parent.parent / "user_data"
else:
    SHARED_DIR = "/user_data"


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
    readme_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query], "README.md")
    metadata_path = os.path.join(MODELS_DIR, DETAIL_LOOKUP[query], "metadata.json")
    with open(readme_path, "r") as fp:
        raw_markdown = fp.read()
    try:
        with open(metadata_path, "r") as fp:
            metadata = json.load(fp)
    except:
        return jsonify({"details": raw_markdown})
    return jsonify({"details": raw_markdown, "metadata": metadata})


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
    file_name = request.args.get("file_name", None)
    user = request.args.get("user", None)
    file_path = os.path.join(SHARED_DIR, f"{user}/{file_name}")

    if file_name is None or user is None:
        return jsonify({"error": "No file path or user found in request"})
    app.logger.debug(f"---> Reading data from {file_path}")

    file_extension = file_name.split(".")[1]
    if file_extension == "csv":
        data = pd.read_csv(file_path)
    elif file_extension == "xlsx" or file_extension == "xls":
        data = pd.read_excel(file_path)
    elif file_extension == "tsv":
        data = pd.read_csv(file_path, sep="\t")

    # XXX
    # return jsonify({"status": "output complete"})
    if target not in HANDLERS.keys():
        # if FLASK_MODE == "dev":
        #     return jsonify(
        #         {
        #             "error": f"Flask mode is {FLASK_MODE}; uploads to {target} aren't supported"
        #         }
        #     )
        app.logger.debug("*" * 40)
        app.logger.debug(f"Target: {target}")
        app.logger.debug(f"Keys: {[k for k in HANDLERS.keys()]}")
        app.logger.debug("*" * 40)
        return jsonify({"error": f"Illegal upload target error: Missing handler for {target}"})
    else:
        # raw_data = request.get_json()
        return jsonify(HANDLERS[target].make_prediction(data))
