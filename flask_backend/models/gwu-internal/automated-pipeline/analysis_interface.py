from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON

import json
import os
import logging
import pickle
import tomli
import uuid

from pipeline import Pipeline

# TODO: Documentation

import numpy as np
import pandas as pd

from pathlib import Path

MODELS_DIR = "./"

with open(".env", "rb") as config_p:
    config = tomli.load(config_p)

FLASK_MODE = config["mode"]

if FLASK_MODE == "dev":
    SHARED_DIR = (
        Path(__file__).resolve().parent.parent.parent.parent.parent / "user_data"
    )
else:
    SHARED_DIR = "/user_data"

DETAIL_LOOKUP = {
    "Pipeline": "TBD",
}

DOWNLOAD_LOOKUP = {
    "Pipeline": "TBD",
}

HANDLERS = {
    "pipeline": Pipeline(),
}


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

app.logger.setLevel(logging.DEBUG)


class CustomModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    file_path: Mapped[str] = mapped_column(unique=True)
    model_bco: Mapped[str] = mapped_column(unique=False)
    training_results: Mapped[JSON] = mapped_column(type_=JSON, unique=False)


with app.app_context():
    db.create_all()


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


@app.route("/delete", methods=["POST"])
def delete_models():
    target_models = request.json
    app.logger.debug(f"Received model IDs to delete: {target_models}")

    CustomModel.query.filter(CustomModel.id.in_(target_models)).delete()
    db.session.commit()

    return jsonify({"deleted": target_models})


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

    if "new_sample" in request.args.keys():
        # This is a new sample, pickles need to be ingested from disk & used
        # app.logger.debug("Upload: Handling a new sample! URL args were:")
        # for k, v in request.args.items():
        #     app.logger.debug(f"---> {k}: {v}")

        request_data = request.get_json()
        # data = pd.DataFrame(request_data["data"][1:])
        # data.columns = request_data["data"][0]
        # app.logger.debug(f"Got a data frame: {data}")

        label_column = request_data["label"]
        # app.logger.debug(f"Found label column: {label_column}")
        label_data = data[label_column]
        data = data.drop(columns=[label_column])
        drop_columns = request_data["drop"]
        if type(drop_columns) is str:
            drop_columns = [drop_columns]
        app.logger.debug(f"Found drop column(s): {drop_columns}")
        try:
            data = data.drop(columns=drop_columns)
        except KeyError as ke:
            # Columns weren't found, ignore
            app.logger.error(f"Error dropping columns: {ke}. Ignoring and continuing")
            pass

        models_to_get = tuple(request_data["models"])
        app.logger.debug(f"---> Getting models by ID {models_to_get}")
        models = CustomModel.query.filter(CustomModel.id.in_(models_to_get)).all()

        # Models were trained on signature "label_data, raw_data". Drop columns were dropped prior to training

        results = []

        for m in models:
            # app.logger.debug(f"Found model with filepath {m.file_path}")
            # Unpickle the model
            with open(m.file_path, "rb") as pickle_pointer:
                model = pickle.load(pickle_pointer)
            # Make a prediction, collect results
            prediction = model.sample_prediction(data)
            training_results = m.training_results
            if "Accuracy" in training_results.keys():
                prediction["Accuracy"] = training_results["Accuracy"]
            if "Confusion Matrix" in training_results.keys():
                prediction["Confusion Matrix"] = training_results["Confusion Matrix"]
            if "Help URL" in training_results.keys():
                prediction["Help URL"] = training_results["Help URL"]
            results.append(
                {
                    "Method": m.name,
                    **prediction,
                }
            )
        return jsonify(results)

    # Training on a new set, not using a new sample
    label_column = request.args.get("label", None)
    drop_columns = request.args.get("drop", None)
    user = request.args.get("user", None)
    if target not in HANDLERS.keys():
        app.logger.debug("*" * 40)
        app.logger.debug(f"Target: {target}")
        app.logger.debug(f"Keys: {[k for k in HANDLERS.keys()]}")
        app.logger.debug("*" * 40)
        return jsonify({"error": "Illegal upload target error"})
    else:
        app.logger.debug(f"Found target: {target}")
        app.logger.debug(f"Found label column: {label_column}")
        app.logger.debug(f"Found drop columns: {drop_columns}")

        combined_results = HANDLERS[target].train_models(
            data, label_column, drop_columns
        )

        pickled_models = combined_results["pickles"]
        results = combined_results["results"]

        family_dir_name = uuid.uuid4()
        family_dir_path = os.path.join(
            os.path.abspath(f"./instance/{user}/{family_dir_name}")
        )
        if not os.path.exists(family_dir_path):
            os.makedirs(family_dir_path)

        for m, r in zip(pickled_models, results):
            app.logger.debug(f"---> Model keys {m.keys()}")
            # app.logger.debug(f"Got results {results}")
            model_path = os.path.join(family_dir_path, m["name"])
            model = CustomModel(
                name=m["name"], file_path=model_path, training_results=r
            )
            # Create the model and save it to the database
            db.session.add(model)
            # Save new models
            db.session.commit()
            db.session.refresh(model)
            # Prepare return information for the
            app.logger.debug(f"---> Created a model; resulting model id is {model.id}")
            r["flask_id"] = model.id
            r["name"] = m["name"]
            # Save the pickled model to the indicated file_path
            with open(model_path, "wb") as pickle_path:
                pickle_path.write(m["encoded_object"])

        return jsonify(results)
