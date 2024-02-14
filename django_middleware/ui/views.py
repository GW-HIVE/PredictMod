from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import (
    requires_csrf_token,
    ensure_csrf_cookie,
    csrf_exempt,
)
from django.contrib.auth.decorators import login_required
from django.conf import settings


import json
import logging
import os
import pandas
import requests

FLASK_BACKEND = settings.FLASK_BACKEND

MG_EXAMPLE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "assets/mg_sample_data.xlsx")
)
EHR_EXAMPLE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "assets/ehr_sample_data.csv")
)

logger = logging.getLogger()


# XXX - Sanity check
@csrf_exempt
def ping(request):
    logger.debug("---> MAIN APP: Received PING")
    return HttpResponse("PONG\n")


@csrf_exempt
def mg_sample(request):
    # See SO: https://stackoverflow.com/a/36394206
    logger.debug("=" * 40)
    logger.debug(f"\tATTEMPTING DOWNLOAD!!")
    logger.debug("=" * 40)
    mg_df = pandas.read_excel(MG_EXAMPLE)
    return JsonResponse(mg_df.to_json(orient="records"), safe=False)


@csrf_exempt
def ehr_sample(request):
    # See also SO: https://stackoverflow.com/a/36394206
    ehr_df = pandas.read_csv(EHR_EXAMPLE)
    return JsonResponse(ehr_df.to_json(orient="records"), safe=False)


# XXX
# @ensure_csrf_cookie
# @requires_csrf_token
@csrf_exempt
def ehr_upload(request):
    if not request.user.is_authenticated:
        return HttpResponse("Must be logged in for analysis", status=200)
    if request.method == "POST":
        try:
            lines = request.readlines()
            raw_data = json.loads(lines[3].decode("utf-8"))
            # logger.debug(f"EHR Request:\n{raw_data}")
            result = requests.post(f"{FLASK_BACKEND}/ehr-upload", json=raw_data)
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
    if not request.user.is_authenticated:
        return HttpResponse("Must be logged in for analysis!", status=200)
    if request.method == "POST":
        try:
            lines = request.readlines()
            raw_data = json.loads(lines[3].decode("utf-8"))
            # XXX
            # logger.debug('-'*40)
            # logger.debug(f"Request:\n{type(raw_data)}")
            # logger.debug('-'*40)
            result = requests.post(f"{FLASK_BACKEND}/mg-upload", json=raw_data)
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}", status=500)
