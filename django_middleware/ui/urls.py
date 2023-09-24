from django.urls import path

from . import views

urlpatterns = [
    path("mg-upload/", views.mg_upload, name="mg-upload"),
    path("ehr-upload/", views.ehr_upload, name="ehr-upload"),
    path("mg-sample/", views.mg_sample, name="mg-sample"),
    path("ehr-sample/", views.ehr_sample, name="ehr-sample"),
    path("ping/", views.ping, name="ping"),
]
