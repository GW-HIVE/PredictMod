from django.contrib.auth.models import User

from .models import SiteUser, TrainedModel

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


# Serializers define the API representation.
class SiteUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = SiteUser
        fields = "__all__"


class TrainedModelDataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainedModel
        fields = ["data_name"]


class TrainedModelPartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainedModel
        fields = ["model_name", "id", "created", "updated", "to_save"]
