from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class SiteUser(models.Model):

    class UserCategories(models.IntegerChoices):
        PATIENT = 1, _("Patient")
        CLINICIAN = 2, _("Clinician")
        RESEARCHER = 3, _("Researcher")

    def get_category(self):
        return self.UserCategories(self.category).label

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.PositiveSmallIntegerField(
        choices=UserCategories.choices, default=UserCategories.RESEARCHER
    )


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class TrainedModel(models.Model):

    model_name = models.CharField(max_length=255)
    data_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    label_field = models.CharField(max_length=100)
    drop_fields = models.JSONField(blank=True)
    to_save = models.BooleanField(default=False)
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True)
    flask_id = models.IntegerField()
