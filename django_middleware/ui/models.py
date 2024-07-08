from django.db import models


# Create your models here.
class ReleasedModel(models.Model):
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=24)
    release_date = models.DateField()
    data_type = models.CharField(max_length=24)
    model_type = models.CharField(max_length=256)
    data_meta = models.JSONField()
    # A map of the above sets of information into what is
    # displayed to the user at the WebUI
    information_mapping = models.JSONField(null=True)
    additional_details = models.JSONField(null=True)
    backend = models.URLField()
    link = models.URLField()


class PendingModel(models.Model):
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=24)
    data_type = models.CharField(max_length=24)
    link = models.URLField()
