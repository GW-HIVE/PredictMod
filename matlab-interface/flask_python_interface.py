from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS, cross_origin

import os
import time
import json
import logging
import pickle
import xlrd

import pandas as pd
import io

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.path.dirname(app.instance_path), "downloads")

app.logger.setLevel(logging.DEBUG)

def ehr_outstr(str1, str2=None):
    return f"""
<h2>Electronic Health Record Analysis Pipeline</h2>
<b>EHR: REMARKS COMPLETE</b>
"""


def metagenomic_outstr(str1):
    return f"""
<h2>Metagenomic Analysis Pipeline</h2>
<b>MG: REMARKS COMPLETE</b>
"""

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

@app.route("/mg-upload", methods=["POST"])
@cross_origin()
def mg_request():
    try:
        # XXX
        # app.logger.debug(f"---> Collected request at >>> MG <<<")
        # app.logger.debug(f"---> Method is {request.method}")
        json_package = json.loads(request.get_json()['json'])
        # app.logger.debug(f"---> JSON Data:\n{json_package}")

        headers, data = json_package[0], json_package[1]

        # app.logger.debug(f"---> Headers: {headers}")
        # app.logger.debug(f"---> Data: {data}")

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
    return Response("EHR: Analysis Loop Completed\n")
