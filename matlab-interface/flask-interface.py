from flask import Flask, request, Response

import os
import time
import logging

import matlab.engine

OPERATING_MODE = os.environ.get("OPERATING_MODE", "local")

if OPERATING_MODE == "local":
    PREDICTMOD_APPLICATION_PATH = os.path.expanduser(
        "~/gwu-src/predictmod-project/PredictMod/predictmod/"
    )
else:
    PREDICTMOD_APPLICATION_PATH = os.path.expanduser("~/gwu-src/PredictMod/predictmod/")

FILE_HOLDING = os.path.expanduser("~/tmp/")
ALLOWED_EXTENSIONS = {"xlsx", "xls"}


class MatlabRunner:
    def __init__(self, path):
        eng = matlab.engine.start_matlab()
        eng.cd(PREDICTMOD_APPLICATION_PATH, nargout=0)
        # eng.load("Synth_data_trained_net.mat")
        eng.addpath(PREDICTMOD_APPLICATION_PATH)
        eng.cd(path, nargout=0)
        # self.nets = [eng.workspace['net1'], eng.workspace['net2'], eng.workspace['net3']]
        self.engine = eng

    def make_prediction(self, filename):
        return self.engine.single_predict(filename)


runner = MatlabRunner(FILE_HOLDING)


def allowed_filename(filename):
    return filename.split(".")[-1] in ALLOWED_EXTENSIONS


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


def outstr(str1, str2=None):
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
<b>Received response:</b>
<br>
    {str1}
<br>
"""


@app.route("/mg-upload", methods=["POST"])
def mg_request():
    output_str = "<h1>Meta-genomic prediction toolchain coming soon!</h1><br>"
    if "files" not in request.files:
        return Response(
            f"{output_str}  - Error: No file uploaded.",
        status=400)
    else:
        file = request.files["files"]
        return Response(
            f"{output_str} - Recieved file {file.filename}", status=200
        )


@app.route("/ehr-upload", methods=["POST"])
def request_received():
    try:
        if "files" not in request.files:
            keys_list = ",".join([fk for fk in request.files.keys()])
            return Response(
                f"<b>No file received!</b><br>Files was {keys_list}", status=400
            )
        file = request.files["files"]
        if not file.filename or not allowed_filename(file.filename):
            return Response(f"<b>Illegal filename {file.filename}!</b>")
        file.save(os.path.join(FILE_HOLDING, file.filename))

        obj_start = time.time()
        prediction = runner.make_prediction(file.filename)
        obj_elapsed = f"{time.time() - obj_start:.2f}s"
        obj_pred = f"{prediction} - {obj_elapsed}"
        func_start = time.time()
        if FUNCTION_TESTING:
            prediction = restarting_the_engine_is_slow(FILE_HOLDING, file.filename)
            func_elapsed = f"{time.time() - func_start:.2f}s"
            func_pred = f"{prediction} - {func_elapsed}"
        else:
            func_pred = None

        # app.logger.debug("-" * 80)
        # app.logger.debug(f"---> Runner output: {prediction}")
        # app.logger.debug("-" * 80)
        return Response(outstr(obj_pred, func_pred))

    except Exception as e:
        return Response(f"Got an error!\n\t{e}")
