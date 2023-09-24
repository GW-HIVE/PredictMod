from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie, csrf_exempt

import requests

import logging

import json

FLASK_HOST = "predict-backend:4245"

MG_EXAMPLE = "./ui/assets/unknown_response.csv"
EHR_EXAMPLE = "./ui/assets/single_patient_data_1.xls"

logger = logging.getLogger()

# XXX - Sanity check
@csrf_exempt
def ping(request):
    return HttpResponse("PONG\n")

import os

@csrf_exempt
def mg_sample(request):
    # See SO: https://stackoverflow.com/a/36394206
    logger.debug("="*40)
    logger.debug(f"\tATTEMPTING DOWNLOAD!!")
    logger.debug("="*40)
    with open(MG_EXAMPLE, "r") as fp:
        response = HttpResponse(fp.read(), content_type="text/csv")
        response['Content-Disposition'] = "inline; filename=metagenomic_example_data.csv"
        return response

@csrf_exempt
def ehr_sample(request):
    # See SO: https://stackoverflow.com/a/36394206
    with open(EHR_EXAMPLE, "rb") as fp:
        response = HttpResponse(fp.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = "inline; filename=ehr_example_data.xls"
        return response

# XXX
# @ensure_csrf_cookie
# @requires_csrf_token
@csrf_exempt
def ehr_upload(request):
    if request.method == "POST":
        try:
            raw_data = json.loads(json.loads(request.readlines()[0].decode('utf-8'))['json'])
            # logger.debug(f"EHR Request:\n{raw_data}")
            result = requests.post(
                f"http://{FLASK_HOST}/ehr-upload", json=raw_data
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")
# XXX
# @ensure_csrf_cookie
# @requires_csrf_token
@csrf_exempt
def mg_upload(request):
    if request.method == "POST":
        try:
            raw_data = json.loads(json.loads(request.readlines()[0].decode('utf-8'))['json'])
            # XXX
            # logger.debug('-'*40)
            # logger.debug(f"Request:\n{type(raw_data)}")
            # logger.debug('-'*40)
            result = requests.post(
                f"http://{FLASK_HOST}/mg-upload", json=raw_data
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

