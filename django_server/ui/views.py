from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie, csrf_exempt

import requests

import logging

import json

FLASK_HOST = "localhost:4245"

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
            data = json.loads(request.readlines()[3].decode('utf-8'))
            result = requests.post(
                f"http://{FLASK_HOST}/ehr-upload", json=data
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
            data = json.loads(request.readlines()[3].decode('utf-8'))
            # XXX
            # logger.debug('-'*40)
            # logger.debug(f"Data 3 Type: {type(data)}")
            # logger.debug('-'*40)
            result = requests.post(
                f"http://{FLASK_HOST}/mg-upload", json=data
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

