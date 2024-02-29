from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse

# from django_rest_passwordreset.signals import reset_password_token_created
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework_jwt.settings import api_settings
# from authentication.services import custom_jwt_handler
# from users.services import ProfileSerializer
# from users.selectors import user_from_username, profile_from_username
# from users.services import profile_update
# from bcodb.selectors import get_all_bcodbs
# from bcodb.services import add_authentication, remove_authentication


# def get(self, request):
# """ TODO
# get request in here so that when you visit localhost:8000/user-list
# you can see all the users. This could be used for BCO population
# """
#     serializer = UserSerializerWithToken.objects.all()
#     return Reponse(serializer.data)


class ChangePasswordApi(APIView):
    """An endpoint for changing password."""

    model = User
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """Serializer for password change endpoint."""

        model = User
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

    def get_object(self, queryset=None):
        import pdb

        pdb.set_trace()
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateApi(APIView):
    """
    This allows you to post data on successful registration to the backend to
    confirm and store a user to the site.
    passed through the serializer UserSerializerWithToken
    """

    permission_classes = (permissions.AllowAny,)

    responses = (
        {
            201: "Registration is successful.",
            400: "Bad request.",
            409: "Conflict. A user with that email already exists.",
        },
    )
    tags = (["Account Management"],)

    def post(self, request, format=None):
        user_serializer = UserSerializerWithToken(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        profile_serializer = ProfileSerializer(data=request.data)
        if (
            profile_serializer.is_valid()
            and len(User.objects.filter(email=request.data["email"])) == 0
        ):
            user_serializer.save()
            profile_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_409_CONFLICT)


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    register and login to pass through the JSON token and user data
    """

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        """
        need to tell it to pass through the token in this model as that is not
        included within the internal workings of the User class, so we
        create the def get_token method
        """

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """Create Serialized User

        Parameters
        ----------
        validated_data: dict
            A dictionary of user values.
        Returns
        -------
        instance: django.contrib.auth.models.User
            Returns a User object
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("token", "username", "password", "email")


class UserUpdateApi(APIView):
    """API view for updating user profile information.

    Allowed HTTP methods: POST.
    """

    class ProfileUpdateSerializer(serializers.Serializer):
        """Serializer class for validating user profile information."""

        username = serializers.CharField()
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        email = serializers.EmailField()
        public = serializers.BooleanField(default=False, initial=False)
        affiliation = serializers.CharField(allow_blank=True)
        orcid = serializers.URLField(allow_blank=True)

    def post(self, request):
        """Update user profile information.

        This API endpoint allows a user to update their profile information. The
        request should include a valid JWT token in the authorization header,
        and the request body should include the user's new profile information.

        Returns the updated user information in the response body.
        """

        token = request.headers["Authorization"].removeprefix("Bearer ")
        profile_payload = self.ProfileUpdateSerializer(data=request.data)
        profile_payload.is_valid(raise_exception=True)
        data = profile_payload.data
        username = data["username"]
        user = user_from_username(username)
        profile = profile_from_username(username)
        if profile.orcid != data["orcid"]:
            bcodbs = get_all_bcodbs(profile)
            if data["orcid"] == "":
                auth_obj = {
                    "iss": "https://" + profile.orcid.split("/")[-2],
                    "sub": profile.orcid.split("/")[-1],
                }
                print("Remove")
                for bcodb in bcodbs:
                    remove_authentication(token, auth_obj, bcodb)
            else:
                auth_obj = {
                    "iss": "https://" + data["orcid"].split("/")[-2],
                    "sub": data["orcid"].split("/")[-1],
                }
                for bcodb in bcodbs:
                    add_authentication(token, auth_obj, bcodb)
        profile_update(user, profile, data)
        user_info = custom_jwt_handler(token, user)

        return Response(status=status.HTTP_200_OK, data=user_info)


class UserInfoApi(APIView):
    """Get user info"""

    def post(self, request):
        user_info = custom_jwt_handler(
            request._auth, user_from_username(request.user.username)
        )
        return Response(status=status.HTTP_200_OK, data=user_info)


class UserRetrieveApi(APIView):
    """
    allows you to post data on successful registration to the backend to
    confirm and store a user to the site.
    passed through the serializer UserSerializerWithToken
    """

    def get(self, request):
        nameset = User.objects.all()
        serializer = UserSerializerWithToken(nameset, many=True)
        return Response(serializer.data)
