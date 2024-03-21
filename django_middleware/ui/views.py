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

DOWNLOAD_ENDPOINTS = {
    "mg",
    "ehr",
}

UPLOAD_ENPOINTS = {
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


# Development
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


# TODO
@csrf_exempt
def file_download(request):
    sample_type = request.GET.get("q", None)
    if sample_type is not None and sample_type in DOWNLOAD_ENDPOINTS:
        # TODO - Error handling should be down at the flask level
        # response = requests.get(f"{FLASK_BACKEND}/download?q={sample_type}")
        if sample_type == "mg":
            df = pandas.read_excel(MG_EXAMPLE)
            return JsonResponse(df.to_json(orient="records"), safe=False)
        elif sample_type == "ehr":
            df = pandas.read_excel(MG_EXAMPLE)
            return JsonResponse(df.to_json(orient="records"), safe=False)
        else:
            return JsonResponse(
                {"error": f"bad sample type: {sample_type}"}, status=404
            )
    return JsonResponse({"error": f"Unknown sample type: {sample_type}"}, status=404)


# # XXX
# @csrf_exempt
# def mg_sample(request):
#     # See SO: https://stackoverflow.com/a/36394206
#     logger.debug("=" * 40)
#     logger.debug(f"\tATTEMPTING DOWNLOAD!!")
#     logger.debug("=" * 40)
#     mg_df = pandas.read_excel(MG_EXAMPLE)
#     return JsonResponse(mg_df.to_json(orient="records"), safe=False)


# @csrf_exempt
# def ehr_sample(request):
#     # See also SO: https://stackoverflow.com/a/36394206
#     ehr_df = pandas.read_csv(EHR_EXAMPLE)
#     return JsonResponse(ehr_df.to_json(orient="records"), safe=False)


def file_upload(request):
    if request.method == "POST":

        try:
            target = request.GET.get("q", None)
            if not target or target not in UPLOAD_ENPOINTS:
                return JsonResponse(
                    {"error": f"Invalid upload target {target}"}, status=404
                )
            data = json.loads(request.body)
            logger.debug(f"---> Request received data: {data}")
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


# XXX
# @requires_csrf_token
# @ensure_csrf_cookie
# def ehr_upload(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({"error": "Must be logged in for analysis"}, status=200)
#     if request.method == "POST":
#         logger.debug("===> Found an uploaded EHR POST call")
#         try:
#             data = json.loads(request.body)
#             # raw_data = json.loads(lines[3].decode("utf-8"))
#             logger.debug(f"EHR Request:\n{data}")
#             result = requests.post(f"{FLASK_BACKEND}/ehr-upload", json=data)
#             result = json.loads(result._content.decode("utf-8"))
#             return JsonResponse(result, status=200, safe=False)
#         except ConnectionRefusedError:
#             return JsonResponse(
#                 {"error": f"Flask error: Is the Flask server running?"},
#                 status=404,
#                 safe=False,
#             )
#         except Exception as error:
#             return JsonResponse(
#                 {"error": f"Django error: {error}"}, status=500, safe=False
#             )
#     else:
#         return JsonResponse(
#             {"error": f"Unsupported request type: {request.method}"},
#             status=400,
#             safe=False,
#         )


# XXX
# @ensure_csrf_cookie
# @requires_csrf_token
# def mg_upload(request):
#     if not request.user.is_authenticated:
#         return HttpResponse("Must be logged in for analysis!", status=200)
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             # XXX
#             # logger.debug('-'*40)
#             # logger.debug(f"Request:\n{type(raw_data)}")
#             # logger.debug('-'*40)
#             result = requests.post(f"{FLASK_BACKEND}/mg-upload", json=data)
#             result = json.loads(result._content.decode("utf-8"))
#             return JsonResponse(result, status=200, safe=False)
#         except Exception as error:
#             return JsonResponse(
#                 {"error": f"Django error:\n\t{error}"}, status=400, safe=False
#             )
#     else:
#         return JsonResponse(
#             {"error": f"Unsupported request type: {request.method}"},
#             status=500,
#             safe=False,
#         )
