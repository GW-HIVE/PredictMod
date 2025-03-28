import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import routers, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.views import APIView

from rest_framework.renderers import JSONRenderer

from .serializers import (
    SiteUserSerializer,
    UserSerializer,
    TrainedModelDataTypeSerializer,
    TrainedModelPartialSerializer,
)
from .models import SiteUser, TrainedModel
from utilities.internal_routing import lookup_backend

import logging
import requests

logger = logging.getLogger()


class CreateUser(APIView):

    def post(self, request):
        logger.debug("===> CreateUserView pinged with 'POST'")

        new_info = json.loads(request.body)
        new_info["username"] = new_info["email"]

        category = new_info.pop("category", None)

        logger.debug(f"New info:\n\n{new_info}\n\tCategory: {category}")
        # Ensure that there's no conflict of email
        previous_entry = User.objects.filter(email=new_info["email"]).first()
        logger.debug(f"==== {previous_entry} ====")
        if previous_entry:
            logger.error(
                f"=== ERROR: User email {previous_entry.email} already exists ==="
            )
            return JsonResponse(
                {"error": f"User email {previous_entry.email} already exists"}
            )

        new_user_serializer = UserSerializer(data=new_info)
        if not new_user_serializer.is_valid():
            logger.debug("Base user information is not valid")
            logger.debug(f"+" * 40)
            logger.debug(f"{new_user_serializer.errors}")
            logger.debug(f"+" * 40)
        new_user_serializer.save()
        new_user = User.objects.filter(email=new_info["email"]).first()
        base_information = {"user_id": new_user.id}
        base_information["category"] = category

        new_site_user_serializer = SiteUserSerializer(data=base_information)
        if new_site_user_serializer.is_valid():
            logger.debug(f"New user IS VALID!")

            # Correct the DRFs broken password ingestion
            new_user.set_password(new_info["password"])
            new_user.save()
            SiteUser.objects.create(user=new_user, category=category)

            new_site_user = SiteUser.objects.filter(user_id=new_user.id).first()

            if new_user.is_superuser:
                return JsonResponse(
                    {"created": new_user.get_username(), "admin": True}, status=200
                )
            return JsonResponse({"created": new_user.get_username()}, status=200)
        else:
            if "email" in new_user_serializer.errors.keys():
                return JsonResponse({"error": new_user.errors["email"][0]}, status=401)
            for key, msg in new_site_user_serializer.errors.items():
                logger.debug(f"{key}: {msg}")
            return JsonResponse({"error": "Unknown"}, status=500)


class DeleteUser(APIView):

    def post(self, request):
        logger.debug("===> DeleteView pinged with 'POST'")
        user_key = request.data["user_id"]

        user = User.objects.filter(id=user_key)
        user.delete()

        return JsonResponse({"username": None}, status=200)


class UpdateUser(APIView):

    def post(self, request):

        updated_info = request.data

        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "error": "Must provide authentication credentials to perform this update"
                }
            )

        logger.debug(f"Updating user with info:\n\n{updated_info}\n")

        user = User.objects.filter(id=updated_info["user_id"]).first()

        is_admin = request.user.is_superuser
        logger.debug(f"User: {request.user} (Is superuser? {is_admin})")

        if "new_password" in updated_info.keys():
            logger.debug("======== UPDATING PASSWORD ===========")
            if not (user.check_password(updated_info["old_password"]) or is_admin):
                return JsonResponse({"error": "Old password is incorrect"}, status=401)
            user.set_password(updated_info["new_password"])
            user.save()

            if not is_admin:
                # Allow normal users to remain logged in
                login(request, user)

        else:
            logger.debug("======== UPDATING PROFILE ===========")
            password = updated_info.pop("password")

            if not is_admin and not user.check_password(password):
                return JsonResponse({"error": "Password is incorrect"}, status=401)
            if user.email != updated_info["email"]:
                other_users = User.objects.filter(email=updated_info["email"]).first()
                if other_users:
                    return JsonResponse(
                        {
                            "error": f"Updated email {updated_info['email']} already exists"
                        },
                        status=401,
                    )
            updated_info["username"] = updated_info["email"]
            user_pk = updated_info.pop("user_id")
            # Login status is not changed on "update"
            User.objects.filter(id=user_pk).update(**updated_info)

            if is_admin:
                user.set_password(password)
        if user.is_superuser:
            return JsonResponse(
                {"update": user.get_username(), "admin": True}, status=200
            )

        return JsonResponse({"update": user.get_username()}, status=200)


# class ModelsByDataTypeView(APIView):
#     def get(self, request):
#         user = request.user
#         logged_in = request.user.is_authenticated

#         if not logged_in:
#             return JsonResponse({"models_by_data_type": []})
#         user_models = TrainedModel.objects.filter(siteuser__user=user.all())

#


def model_updates(request):
    try:
        logger.debug("-" * 80)
        logger.debug("Model updates: Got request")
        logger.debug("-" * 80)

        if request.method != "POST":
            return JsonResponse(
                {"error": f"Method {request.method} is not support on update"},
                safe=False,
            )

        query = request.GET.get("q", None)
        if not query:
            return JsonResponse({"error": "Invalid request URL arguments"})
        if query == "model_updates":
            updates = {}
            # Get the body and validate
            updated_models = json.loads(request.body)
            logger.debug(f"---> UPDATING {updated_models}")
            tm_manager = TrainedModel.objects

            for m in updated_models:
                tm = tm_manager.filter(id=m["id"]).first()
                tm.all_user_shared = m["allUserShared"]
                tm.save()
                updates[tm.id] = TrainedModelPartialSerializer(tm).data

            for id, data in updates.items():
                logger.debug(f"{id}: New data: {data}")

            return JsonResponse(updates, safe=False)

    except Exception as e:
        return JsonResponse({"error": f"Unknwon error {e}"}, safe=False)


class ModelListView(APIView):
    def get(self, request):
        user = request.user
        logged_in = request.user.is_authenticated

        logger.debug(f"Found user {user} ({'not ' if not logged_in else ''}logged in)")

        if not logged_in:
            return JsonResponse({"models_available": []})

        if "action" in request.GET.keys():
            action = request.GET["action"]
            target = request.GET.get("target", None)
            if action == "delete_model_family":
                family_model_name = request.GET.get("data_type", None)
                if not family_model_name or not target:
                    return JsonResponse(
                        {
                            "error": "Malformed request. Missing family model name or target parameter"
                        },
                        status=400,
                    )
                logger.debug(
                    f"---> Looking to delete models of family {family_model_name}"
                )
                models_to_delete = TrainedModel.objects.filter(
                    siteuser__user=user
                ).filter(data_name=family_model_name)
                flask_ids = []
                for m in models_to_delete:
                    flask_ids.append(m.flask_id)
                response = requests.post(
                    f"{lookup_backend(target)}/delete",
                    json=flask_ids,
                )

                complete_response = response.json()

                logger.debug(f"Found deletion response: {complete_response}")

                if "deleted" not in complete_response.keys():
                    # Error handling
                    ...
                    return JsonResponse({"error": "Error on delete, investigate"})

                models_to_delete.delete()

                return JsonResponse({"deleted": family_model_name})
            elif action == "delete_model":

                model_to_delete = request.GET.get("model_id", None)
                if not model_to_delete:
                    return JsonResponse({"error": "No model found for deletion"})

                model = TrainedModel.objects.filter(id=model_to_delete).first()

                flask_id = model.flask_id

                response = requests.post(
                    f"{lookup_backend(target)}/delete",
                    json=[flask_id],
                )

                complete_response = response.json()

                logger.debug(f"---> Got complete response {complete_response}")

                model.delete()

                return JsonResponse({"deleted": model_to_delete})
            else:
                return JsonResponse(
                    {"error": f"Unhandled arg '{action}' detected"}, status=400
                )

        data_type_query = request.GET.get("q", None)
        shared_models = request.GET.get("shared", None)
        if shared_models:
            models = TrainedModel.objects.filter(all_user_shared=True).all()
        else:
            models = TrainedModel.objects.filter(siteuser__user=user).all()

        if data_type_query:
            data_types = [TrainedModelDataTypeSerializer(m).data for m in models]
            unique_data_types = sorted(list(set(dt["data_name"] for dt in data_types)))
            data_types = [{"name": str(dt)} for dt in unique_data_types]
            return JsonResponse(data_types, safe=False)

        data_type_name = request.GET.get("data_type", None)
        if data_type_name is None:
            return JsonResponse({"error": "Unsupported request parameters"}, safe=False)

        model_to_return = {
            "models_available": [
                TrainedModelPartialSerializer(m).data for m in models.filter(data_name=data_type_name)
            ]
        }
        # logger.debug(f"Model list view: Accessing models for user {user}")
        # logger.debug(f"Found user models {selected_models}")

        return JsonResponse(model_to_return, safe=False)


class UserListView(APIView):

    def get(self, request):
        logger.debug("=" * 80)
        user = request.user
        logged_in = request.user.is_authenticated

        if not logged_in:
            return JsonResponse(
                {"error": "You must be logged in to view user information"}, status=401
            )

        # user = User.objects.filter(email=user.email).first()
        siteuser = SiteUser.objects.filter(user=user).first()

        if not user.is_staff:
            serialized_site_info = SiteUserSerializer(siteuser).data
            serialized_site_info["category"] = siteuser.get_category()
            logger.debug(f"===> Data: {serialized_site_info}")
            return JsonResponse([serialized_site_info], safe=False, status=200)

        siteusers = SiteUser.objects.all()
        serialized_data = []
        for su in siteusers:
            data = SiteUserSerializer(su).data
            data["category"] = su.get_category()
            serialized_data.append(data)
        logger.debug(f"{serialized_data}")
        logger.debug("=" * 80)

        return JsonResponse(serialized_data, safe=False, status=200)


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"detail": "False"}, status=599)
    data = json.loads(request.body)
    logger.debug(f"---> Caught request! Data?: {data}")
    username = data.get("email")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse(
            {"detail": "Please provide username and password."}, status=400
        )

    # Failed authentication yields an HTTP 400 error code
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=400)

    # log_info(request, user)

    logger.debug(f"Got user: {user}")

    users = User.objects.all()
    for u in users:
        logger.debug(f"DB User: {u} ---> Authenticated? {u.is_authenticated}")

    # logger.debug("=" * 80)
    # session_keys = {
    #     "_auth_user_id": "SESSION_KEY",
    #     "_auth_user_backend": "BACKEND_SESSION_KEY",
    #     "_auth_user_hash": "HASH_SESSION_KEY",
    # }
    # for k, v in session_keys.items():
    #     if k in request.session.keys():
    #         logger.debug(
    #             f"---> Session info - {k}:\n{request.session[k]} (session 'key' {v})"
    #         )
    #     else:
    #         logger.debug(f"---> Key {k} not in session info!! <---")
    # logger.debug(f"---> Computed user info: {user._meta.pk.value_to_string(user)}")
    # logger.debug("=" * 80)

    login(request, user)

    users = User.objects.all()
    for u in users:
        logger.debug(
            f"Refreshed (?) DB User: {u} ---> Authenticated? {u.is_authenticated}"
        )
    site_user = SiteUser.objects.filter(user=user).first()
    user_category = site_user.get_category()

    if user.is_superuser:
        return JsonResponse(
            {
                "username": user.get_username(),
                "role": user_category,
                "admin": True,
                "authenticated": True,
            },
            status=200,
        )
    return JsonResponse(
        {"username": user.get_username(), "role": user_category, "authenticated": True}
    )


def logout_view(request):
    logger.debug(f"---> Caught request! Body: {request.body}")
    logger.debug(f"---> User info? {request.user}")
    users = User.objects.all()

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)

    return JsonResponse({"detail": "Successfully logged out."})


def whoami_view(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    # headers = request.headers

    # XXX
    # for h in headers:
    #     logger.debug(f"===> {h}")

    site_user = SiteUser.objects.filter(user=user).first()
    category = site_user.get_category()

    if user.is_superuser:
        return JsonResponse(
            {"username": request.user.username, "role": category, "admin": True},
            status=200,
        )

    return JsonResponse(
        {"username": request.user.username, "role": category}, status=200
    )
