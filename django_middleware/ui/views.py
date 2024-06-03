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
from django.core import serializers

from .models import ReleasedModel, PendingModel

import json
import logging
import os
import pandas
import requests

FLASK_BACKEND = settings.FLASK_BACKEND

logger = logging.getLogger()


UPLOAD_ENDPOINTS = {
    "mg",
    "ehr",
}


def binary_response_to_json(response):
    return json.loads(response.content.decode("utf-8"))


# XXX - Sanity check
@csrf_exempt
def ping(request):
    logger.debug("---> MAIN APP: Received PING")
    return HttpResponse("PONG\n")


def search(request):
    logger.debug("Received request for MENU items")
    DATA_MODEL = [
        {"name": "MDClone Diet Exercise (Intervention)", "link": "help#current-models"},
        {"name": "MG Exercise (Intervention)", "link": "help#current-models"},
        {"name": "Decision Tree Classifier (Model)", "link": "help#current-models"},
        {
            "name": "Electronic Health Records (EHR) (Data)",
            "link": "help#current-models",
        },
        {"name": "Metagenomic (Data)", "link": "help#current-models"},
        {
            "name": "Glycomics PreDM v1.0 (Anticipated)",
            "link": "help#anticipated-models",
        },
        {"name": "Epilepsy Keto v1.1 (Anticipated)", "link": "help#anticipated-models"},
        {
            "name": "Synthea Exercise v1.1 (Anticipated)",
            "link": "help#anticipated-models",
        },
        {
            "name": "MDClone Diet Counseling v1.2 (Anticipated)",
            "link": "help#anticipated-models",
        },
        {
            "name": "MDClone Semaglutide v1.0 (Anticipated)",
            "link": "help#anticipated-models",
        },
        {
            "name": "MDClone Exercise v1.0 (Anticipated)",
            "link": "help#anticipated-models",
        },
    ]
    return JsonResponse(DATA_MODEL, safe=False)


# TODO: Development of backend search
def queries(request):
    if request.method != "GET":
        return JsonResponse({"error": f"Invalid method {request.METHOD}"})
    logger.debug("---> Received query")
    query = request.GET.get("q", None)
    logger.debug(f"Found query: {query}")
    result = requests.get(f"{FLASK_BACKEND}/query?query={query}")

    return JsonResponse(json.loads(result.content.decode("utf-8")), safe=False)


@csrf_exempt
def live_data(request):
    logger.debug("===> Serving data request <===")
    data = [
        {"name": "Factor 1", "value": 42},
        {"name": "Factor 2", "value": 25},
        {"name": "Factor 3", "value": -12},
    ]
    return JsonResponse(data=data, safe=False)


# /Development
@csrf_exempt
def png_response(request):
    logger.debug("===> Serving data request <===")
    data = {"Factor 1": 42, "Factor 2": 25, "Factor 3": -12}
    return JsonResponse(data=data, safe=False)


def models(request):
    released_models = ReleasedModel.objects.all()
    pending_models = PendingModel.objects.all()
    complete_list = {"released_models": None, "pending_models": None}
    complete_list["released_models"] = serializers.serialize("json", released_models)
    complete_list["pending_models"] = serializers.serialize("json", pending_models)
    return JsonResponse(complete_list, safe=False)


@csrf_exempt
def file_download(request):
    sample_type = request.GET.get("q", None)
    if sample_type is not None:
        response = requests.get(f"{FLASK_BACKEND}/download?q={sample_type}")
        if response.status_code != 200:
            return JsonResponse({"error": response.content.decode("utf-8")})
        return JsonResponse(json.loads(response.content.decode("utf-8")), safe=False)
    return JsonResponse({"error": f"Unknown sample type: {sample_type}"}, status=500)


def file_upload(request):
    if request.method == "POST":

        try:
            target = request.GET.get("q", None)
            if not target or target not in UPLOAD_ENDPOINTS:
                return JsonResponse(
                    {"error": f"Invalid upload target {target}"}, status=404
                )
            data = json.loads(request.body)
            # logger.debug(f"---> Request received data: {data}")
            response = requests.post(f"{FLASK_BACKEND}/upload?q={target}", json=data)
            response = json.loads(response._content.decode("utf-8"))
            return JsonResponse(response, status=200, safe=False)
        except ConnectionRefusedError:
            return JsonResponse(
                {"error": f"Flask error: Is the Flask server running?"},
                status=404,
                safe=False,
            )
        except Exception as error:
            return JsonResponse(
                {"error": f"Django error: {error}"}, status=500, safe=False
            )
    else:
        return JsonResponse(
            {"error": f"Unsupported request type: {request.method}"},
            status=400,
            safe=False,
        )
