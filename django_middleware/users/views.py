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

from .serializers import UserSerializer

import logging

logger = logging.getLogger()


class CreateUser(APIView):

    def post(self, request):
        logger.debug("===> CreateUserView pinged with 'POST'")

        new_info = json.loads(request.body)
        new_info["username"] = new_info["email"]

        logger.debug(f"New info:\n\n{new_info}\n")
        # Ensure that there's no conflict of email
        previous_entry = User.objects.filter(email=new_info["email"]).first()
        logger.debug(f"==== {previous_entry} ====")
        if previous_entry:
            return JsonResponse(
                {"error": f"User email {previous_entry.email} already exists"}
            )

        new_user = UserSerializer(data=new_info)
        if new_user.is_valid():
            logger.debug(f"New user IS VALID!")
            new_user.save()

            user = User.objects.filter(email=new_info["email"]).first()
            # Correct the DRFs broken password ingestion
            user.set_password(new_info["password"])
            user.save()
            if user.is_superuser:
                return JsonResponse(
                    {"created": user.get_username(), "admin": True}, status=200
                )
            return JsonResponse({"created": user.get_username()}, status=200)
        else:
            if "email" in new_user.errors.keys():
                return JsonResponse({"error": new_user.errors["email"][0]}, status=401)
            for key, msg in new_user.errors.items():
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


class UserListView(APIView):

    def get(self, request):
        user = request.user
        logged_in = request.user.is_authenticated

        if not logged_in:
            return JsonResponse(
                {"error": "You must be logged in to view user information"}, status=401
            )

        user = User.objects.filter(email=user.email).first()

        if not user.is_staff:
            serialized_data = UserSerializer(user).data
            return JsonResponse([serialized_data], safe=False, status=200)

        users = User.objects.all()
        serialized_data = UserSerializer(users, many=True).data
        logger.debug(f"{serialized_data}")

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
    if user.is_superuser:
        return JsonResponse(
            {"username": user.get_username(), "admin": True}, status=200
        )
    return JsonResponse({"username": user.get_username(), "authenticated": True})


def logout_view(request):
    logger.debug(f"---> Caught request! Body: {request.body}")
    logger.debug(f"---> User info? {request.user}")
    users = User.objects.all()

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)

    return JsonResponse({"detail": "Successfully logged out."})


def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    headers = request.headers

    # XXX
    # for h in headers:
    #     logger.debug(f"===> {h}")

    if request.user.is_superuser:
        return JsonResponse(
            {"username": request.user.username, "admin": True}, status=200
        )

    return JsonResponse({"username": request.user.username}, status=200)
