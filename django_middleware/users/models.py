from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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


class TrainedModel(models.Model):

    model_name = models.CharField(max_length=255)
    serialized_model = models.BinaryField()
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True)
