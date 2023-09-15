from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie, csrf_exempt

import requests

import logging

import json

FLASK_HOST = "predict-backend:4245"

logger = logging.getLogger()

# Create your views here.
def index(request):
    return HttpResponse("Away we go ... again")

def ui(request):
    return render(request, "ui/index.html")

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

