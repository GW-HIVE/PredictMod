from flask import Flask, request, Response

import os
import time
import logging
import pandas as pd
import pickle

ENGINE = False
try:
    import matlab.engine

    ENGINE = True
except Exception:
    pass


OPERATING_MODE = os.environ.get("OPERATING_MODE", "local")

if OPERATING_MODE == "local":
    PREDICTMOD_APPLICATION_PATH = os.path.expanduser(
        "~/gwu-src/predictmod-project/PredictMod/predictmod/"
    )
else:
    PREDICTMOD_APPLICATION_PATH = os.path.expanduser("~/gwu-src/PredictMod/predictmod/")

FILE_HOLDING = os.path.expanduser("~/tmp/")
EHR_ALLOWED_EXTENSIONS = {"xlsx", "xls"}
MG_ALLOWED_EXTENSIONS = {
    "csv",
}


class MetagenomicPredictor:
    def __init__(self, path):
        self.working_path = os.path.abspath(path)
        try:
            with open("pickled_tree.pickle", "rb") as fp:
                self.tree = pickle.load(fp)
            fp.close()
        except Exception as e:
            print(
                "Warning: Error loading pickle file. Metagenomic predictions disabled!"
                f"\nError was {e}"
            )
            self.tree = None

    def make_prediction(self, filename):
        if not self.tree:
            return f"Error: Metagenomic predictions have been disabled"
        sample = pd.read_csv(os.path.join(self.working_path, filename))
        sample = sample.drop(["Status"], axis=1)
        result = self.tree.predict(sample)
        if "N" in result:
            return "Non-responder"
        return "Responder"


class EHRMatlabPredictor:
    def __init__(self, path):
        if ENGINE:
            eng = matlab.engine.start_matlab()
            eng.cd(PREDICTMOD_APPLICATION_PATH, nargout=0)
            # eng.load("Synth_data_trained_net.mat")
            eng.addpath(PREDICTMOD_APPLICATION_PATH)
            eng.cd(path, nargout=0)
            # self.nets = [eng.workspace['net1'], eng.workspace['net2'], eng.workspace['net3']]
            self.engine = eng
        else:
            self.engine = None

    def make_prediction(self, filename):
        return (
            self.engine.single_predict(filename)
            if self.engine
            else "MatLab is not currently available"
        )


ehr_matlab_predictor = EHRMatlabPredictor(FILE_HOLDING)
metagenomic_predictor = MetagenomicPredictor(FILE_HOLDING)


def ehr_allowed_filename(filename):
    return filename.split(".")[-1] in EHR_ALLOWED_EXTENSIONS


def mg_allowed_filename(filename):
    return filename.split(".")[-1] in MG_ALLOWED_EXTENSIONS


def restarting_the_engine_is_slow(path, file_name):
    eng = matlab.engine.start_matlab()
    eng.cd(PREDICTMOD_APPLICATION_PATH, nargout=0)
    # eng.load("Synth_data_trained_net.mat")
    eng.addpath(PREDICTMOD_APPLICATION_PATH)
    eng.cd(path, nargout=0)
    # nets = [eng.workspace['net1'], eng.workspace['net2'], eng.workspace['net3']]
    return eng.single_predict(file_name)


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

FUNCTION_TESTING = False


def ehr_outstr(str1, str2=None):
    if FUNCTION_TESTING:
        return f"""
<b>Received response:</b>
<br>
Object-oriented result:
    {str1}
<br>
Function-based result:
    {str2}
"""
    else:
        return f"""
<h2>Electronic Health Record Analysis Pipeline</h2>
<b>Received response:</b>
<br>
    {str1}
<br>
"""


def metagenomic_outstr(str1):
    return f"""
<h2>Metagenomic Analysis Pipeline</h2>
<b>Received response:</b>
<br>
    Patient prediction is: {str1}
<br>
"""


@app.route("/mg-upload", methods=["POST"])
def mg_request():
    try:
        if "files" not in request.files:
            return Response(
                f"Metagenomic Analysis - Error! No file uploaded.", status=400
            )
        file = request.files["files"]
        if not file.filename or not mg_allowed_filename(file.filename):
            return Response(f"<b>Illegal filename {file.filename}!</b>")
        file.save(os.path.join(FILE_HOLDING, file.filename))
    except Exception as e:
        return Response(f"Got an error!\n\t{e}")

    prediction = metagenomic_predictor.make_prediction(file.filename)
    return Response(metagenomic_outstr(prediction))


@app.route("/ehr-upload", methods=["POST"])
def request_received():
    try:
        if "files" not in request.files:
            return Response("EHR Analysis - Error! No file uploaded.", status=400)
        file = request.files["files"]
        if not file.filename or not ehr_allowed_filename(file.filename):
            return Response(f"<b>Illegal filename {file.filename}!</b>")
        file.save(os.path.join(FILE_HOLDING, file.filename))

        obj_start = time.time()
        prediction = ehr_matlab_predictor.make_prediction(file.filename)
        obj_elapsed = f"{time.time() - obj_start:.2f}s"
        obj_pred = f"{prediction} - {obj_elapsed}"
        func_start = time.time()
        if FUNCTION_TESTING:
            prediction = restarting_the_engine_is_slow(FILE_HOLDING, file.filename)
            func_elapsed = f"{time.time() - func_start:.2f}s"
            func_pred = f"{prediction} - {func_elapsed}"
        else:
            func_pred = None

        return Response(ehr_outstr(prediction))

    except Exception as e:
        return Response(f"Got an error!\n\t{e}")
