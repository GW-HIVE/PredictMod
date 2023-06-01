from django.shortcuts import render, HttpResponse, redirect
from django.template.response import TemplateResponse
from django.conf import settings

import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

import os
import getpass
import requests

# import matlab.engine
# import matlab

logger = logging.getLogger()


# Create your views here.
def index(request):
    request.META["CSRF_COOKIE_USED"] = True
    if request.method == "GET":
        args = {"EHR_UPLOAD": "predictmod/ehr-upload/",
                "MG_UPLOAD": "predictmod/mg-upload/"}
        return TemplateResponse(request, "index.html", args)
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

def ehr_upload(request):
    if request.method == "POST":
        try:
            logger.debug("+" * 80)
            logger.debug(f"Request files: {request.FILES}")
            logger.debug(f"Request site path: {request.path}")
            logger.debug("+" * 80)
            result = requests.post(
                f"http://host.docker.internal:4243/ehr-upload", files=request.FILES
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

def mg_upload(request):
    if request.method == 'POST':
        try:
            result = requests.post(
                f"http://host.docker.internal:4243/mg-upload", files=request.FILES
            )
            return HttpResponse(result)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")
