from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.template.response import TemplateResponse
from django.views.decorators.csrf import (
    requires_csrf_token,
    ensure_csrf_cookie,
    csrf_exempt,
)
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers

from .models import ReleasedModel, PendingModel, Condition, Intervention, InputDataType

from utilities.internal_routing import lookup_backend

from users.models import SiteUser, TrainedModel
from users.serializers import TrainedModelFullSerializer

from base64 import b64decode

import json
import logging
import os
import pandas
import requests

logger = logging.getLogger()


# UPLOAD_ENDPOINTS = {
#     "mg",
#     "ehr",
# }


def binary_response_to_json(response):
    return json.loads(response.content.decode("utf-8"))


# def get_anlaysis_urls():
#     try:
#         models = ReleasedModel.objects.all()
#         return {m.name: f"http://{m.backend}:4243" for m in models}
#     except Exception as e:
#         logger.critical("=" * 80)
#         logger.critical(f"Exception: {e}")
#         logger.critical("=" * 80)
#         return {"None": "No models found in database"}


# ANALYSIS_BACKENDS = get_anlaysis_urls()


# def lookup_backend(model_name: str):
#     if settings.DJANGO_MODE == "dev":
#         return "http://localhost:5000"
#     de_modified_model_name = model_name.replace("-", " ")
#     logger.debug("-" * 40)
#     logger.debug(f"ANALYSIS BACKENDS: {ANALYSIS_BACKENDS}")
#     logger.debug(f"Searching for {de_modified_model_name}")
#     logger.debug("-" * 40)
#     return ANALYSIS_BACKENDS.get(de_modified_model_name, None)


# XXX - Sanity check
@csrf_exempt
def ping(request):
    logger.debug("---> MAIN APP: Received PING")
    return HttpResponse("PONG\n")


def search(request):
    logger.debug("Received request for MENU items")
    released_models = ReleasedModel.objects.all()
    pending_models = PendingModel.objects.all()
    complete_list = [
        {"name": k.name.replace("-", " ").replace("_", " "), "link": k.link}
        for k in released_models
    ]
    complete_list.extend(
        [
            {
                "name": k.name.replace("-", " ").replace("_", " ") + " (Anticipated)",
                "link": k.link,
            }
            for k in pending_models
        ]
    )

    return JsonResponse(complete_list, safe=False)


# TODO: Development of backend search
def queries(request):
    if request.method != "GET":
        return JsonResponse({"error": f"Invalid method {request.METHOD}"})
    logger.debug("---> Received query")
    query = request.GET.get("q", None)
    logger.debug(f"Found query: {query}")

    result = requests.get(f"{lookup_backend(query)}/query?query={query}")

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


def query_conditions(request):
    intervention = request.GET.get("i", None)
    input_data_type = request.GET.get("dt", None)
    conditions = Condition.objects.all()
    # if intervention is not None:
    #     conditions = conditions.filter(intervention_id == intervention)
    return JsonResponse(serializers.serialize("json", conditions), safe=False)


def query_interventions(request):
    condition_name = request.GET.get("c", None)
    if condition_name is None or condition_name == "null":
        return JsonResponse({"error": f"Condition was not found in query"}, safe=False)
    else:
        logger.debug(f"Got request for interventions of {condition_name}")
    condition = Condition.objects.filter(name=condition_name).first()
    interventions_set = serializers.serialize("json", condition.interventions.all())
    # logger.debug(f"Found interventions: {interventions_set}")
    return JsonResponse(interventions_set, safe=False)


def query_input_data(request):
    condition_name = request.GET.get("c", None)
    if condition_name is None:
        return JsonResponse({"error": f"Condition was not found in query"}, safe=False)
    else:
        logger.debug(f"Got request for input data types of {condition_name}")
    condition = Condition.objects.filter(name=condition_name).first()
    # logger.debug("*"*80)
    # logger.debug(f"{condition}")
    # logger.debug("*"*80)
    input_types_set = serializers.serialize("json", condition.input_data_types.all())
    # logger.debug(f"Found data types: {input_types_set}")
    return JsonResponse(input_types_set, safe=False)


def query_model_endpoints(request):
    condition_name = request.GET.get("c", None)
    intervention_name = request.GET.get("i", None)
    input_data_type = request.GET.get("dt", None)
    logger.debug(
        f"===> Attempting to filter models based on: Condition {condition_name} Intervention: {intervention_name} Data Type: {input_data_type}"
    )
    all_models = ReleasedModel.objects.all()

    # TODO/XXX logger.debug(all_models)
    models = (
        all_models.filter(condition__name=condition_name)
        .filter(intervention__name=intervention_name)
        .filter(input_type__name=input_data_type)
    )
    # Should only be one model now
    # TODO/XXX 
    # logger.debug(f"---> Found models: {models}")
    # for m in all_models:
    #     logger.debug("*"*80)
    #     logger.debug(f"Condition: {m.condition.name} Intervention: {m.intervention.name} Data type: {m.data_type}")
    #     logger.debug("*"*80)
    models_available = serializers.serialize("json", models)
    return JsonResponse(models_available, safe=False)


def model_details(request):
    try:
        model_name = request.GET.get("q", None)
        logger.debug(f"===> Requested details for model {model_name}")
        if model_name is None:
            return JsonResponse({"error": f"Unknown model name: {model_name}"})
        response = requests.get(
            f"{lookup_backend(model_name)}/model-details?q={model_name}"
        )
        logger.debug(f"Response: {response.status_code}")
        if response.status_code == 404:
            logger.debug("===> Response was 404 <===")
            return JsonResponse({"results": "complete"}, status=200, safe=False)
        response = json.loads(response._content.decode("utf-8"))
        return JsonResponse(response, status=200, safe=False)
    except ConnectionRefusedError:
        return JsonResponse(
            {"error": f"Flask error: Is the Flask server running?"},
            status=404,
            safe=False,
        )
    except Exception as error:
        return JsonResponse({"error": f"Django error: {error}"}, status=500, safe=False)


@csrf_exempt
def file_download(request):
    model_name = request.GET.get("q", None)
    if model_name is not None:
        response = requests.get(f"{lookup_backend(model_name)}/download?q={model_name}")
        if response.status_code != 200:
            return JsonResponse({"error": response.content.decode("utf-8")})
        return JsonResponse(json.loads(response.content.decode("utf-8")), safe=False)
    return JsonResponse({"error": f"Unknown model name: {model_name}"}, status=500)


def file_upload(request):
    if request.method == "POST":

        try:
            target = request.GET.get("q", None)
            file_name = request.GET.get("name", None)
            user = request.user

            site_user = SiteUser.objects.filter(user=user).first()
            username = f"{site_user.user.first_name} {site_user.user.last_name}"
            user_email = site_user.user.email
            # if not target or target not in UPLOAD_ENDPOINTS:
            #     return JsonResponse(
            #         {"error": f"Invalid upload target {target}"}, status=404
            #     )
            for k in request.GET.keys():
                logger.debug(f"{k}: {request.GET[k]}")
            file = request.body
            logger.debug(
                f"---> USER {user}: Got a request with file (type {type(file)})"
            )
            logger.debug(
                f"---> Attempting to write to shared folder: {settings.SHARED_FILE_LOCATION} | {user} | {file_name}"
            )

            user_storage_folder = os.path.join(settings.SHARED_FILE_LOCATION, f"{user}")

            if not os.path.exists(user_storage_folder):
                os.makedirs(user_storage_folder)

            full_file_path = os.path.join(user_storage_folder, file_name)
            if os.path.exists(full_file_path):
                os.remove(full_file_path)

            with open(full_file_path, "wb") as fp:
                fp.write(file)
            fp.close()

            if target == "pipeline":
                data_type = request.GET.get("data_name", None)
                if data_type is None:
                    return JsonResponse(
                        {"error": "Data type for model must be specified"}
                    )
                # Logged-in user is required for launching the pipeline
                user = request.user
                if not user.is_authenticated:
                    return JsonResponse(
                        {"error": "Login required to use the automated pipeline"},
                        safe=False,
                        status=403,
                    )
                model_mode = request.GET["method"]
                logger.debug(f"Uploading file with algorithm mode: {model_mode}")
                other_args = ""

                for arg in request.GET.keys():
                    logger.debug(
                        f"---> Request received arg: {arg} -- {request.GET[arg]}"
                    )
                    if arg == "q" or arg == "data_type":
                        continue
                    other_args += f"&{arg}={request.GET[arg]}"

                if model_mode == "training":
                    logger.debug("=" * 80)
                    logger.debug(f"---> Modeling: Found user {user_email}")
                    arg_dict = {"label": "", "drop": ""}
                    for arg in arg_dict.keys():
                        other_args += f"&{arg}={request.GET[arg]}"
                        arg_dict[arg] = request.GET[arg]
                    response = requests.post(
                        f"{lookup_backend(target)}/upload?q={target}&user={username}&email={user_email}&file_name={file_name}{other_args}",
                    )
                    response = json.loads(response._content.decode("utf-8"))
                    if type(response) is dict and "error" in response.keys():
                        logger.debug(f"---> Found response: {response}")
                        return JsonResponse(response, status=500)
                    for model in response:
                        logger.debug(
                            f"Name: {model['name']} -- flask_id: {model['flask_id']}"
                        )
                        TrainedModel.objects.create(
                            flask_id=model["flask_id"],
                            model_name=model["name"],
                            data_name=data_type,
                            label_field=request.GET.get("label"),
                            drop_fields=request.GET.get("drop"),
                            siteuser=site_user,
                        )
                    logger.debug("=" * 80)
                    return JsonResponse(response, status=200, safe=False)
                elif model_mode == "newSample":
                    model_ids = json.loads(request.GET.get("model_ids", None))
                    logger.debug(f"Collected model IDs: {model_ids}")
                    models = TrainedModel.objects.filter(id__in=set(model_ids))
                    flask_ids = [m.flask_id for m in models]
                    m = models[0]
                    # models = []
                    # for m in model_ids:
                    #     # XXX - Shipping models this way is almost physically painful
                    #     models.append()
                    payload = {
                        "models": flask_ids,
                        "label": m.label_field,
                        "drop": m.drop_fields,
                    }
                    response = requests.post(
                        f"{lookup_backend(target)}/upload?q={target}&new_sample=true&user={username}&email={user_email}&file_name={file_name}",
                        json=payload,
                    )
                    response_json = response.json()
                    # logger.debug(f"---> Got a response! {response_json}")
                    return JsonResponse(response_json, status=200, safe=False)
                else:
                    # Default, error
                    logger.debug(f"---> model_mode fatal error: {model_mode}")

            else:

                response = requests.post(
                    f"{lookup_backend(target)}/upload?q={target}&user={user}&email={user_email}&file_name={file_name}"
                )
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
