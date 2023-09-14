from django.shortcuts import render, HttpResponse, redirect
from django.template.response import TemplateResponse
from django.conf import settings

import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

import os
import getpass
import requests

logger = logging.getLogger()


OPERATING_MODE = os.environ.get("OPERATING_MODE", "local")

if OPERATING_MODE == "local":
    APPLICATION_URLS = {
        "EHR_UPLOAD": "ehr-upload/",
        "MG_UPLOAD": "mg-upload/",
    }
    FLASK_HOST = "localhost:5000"
else:
    APPLICATION_URLS = {
        "EHR_UPLOAD": "predictmod/ehr-upload/",
        "MG_UPLOAD": "predictmod/mg-upload/",
    }
    FLASK_HOST = "host.docker.internal:4243"


# Create your views here.
def index(request):
    # TBD: request.META["CSRF_COOKIE_USED"] = True
    if request.method == "GET":
        return TemplateResponse(request, "index.html")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

def ehr(request):
    if request.method == "GET":
        return TemplateResponse(request, "EHR.html", APPLICATION_URLS)
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")

def metagenomic(request):
    if request.method == "GET":
        return TemplateResponse(request, "Metagenomic.html", APPLICATION_URLS)
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
                f"http://{FLASK_HOST}/ehr-upload", files=request.FILES
            )
            # ctx = APPLICATION_URLS
            ctx = {}
            ctx["ehr_result"] = result.content.decode('utf-8')
            return TemplateResponse(request, "EHR.html", ctx)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")


def mg_upload(request):
    if request.method == "POST":
        try:
            result = requests.post(
                f"http://{FLASK_HOST}/mg-upload", files=request.FILES
            )
            # ctx = APPLICATION_URLS
            ctx = {}
            ctx["mg_result"] = result.content.decode('utf-8')
            return TemplateResponse(request, "Metagenomic.html", ctx)
        except Exception as error:
            return HttpResponse(f"Django error:\n\t{error}")
    else:
        return HttpResponse(f"Unsupported request type: {request.method}")
