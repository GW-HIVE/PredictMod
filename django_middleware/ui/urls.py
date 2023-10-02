from django.urls import path

from . import views

urlpatterns = [
    path("mg-upload/", views.mg_upload, name="mg-upload"),
    path("predictmod/mg-upload/", views.mg_upload, name="pm-mg-upload"),
    path("ehr-upload/", views.ehr_upload, name="ehr-upload"),
    path("predictmod/ehr-upload/", views.ehr_upload, name="pm-ehr-upload"),
    path("mg-sample/", views.mg_sample, name="mg-sample"),
    path("predictmod/mg-sample/", views.mg_sample, name="pm-mg-sample"),
    path("ehr-sample/", views.ehr_sample, name="ehr-sample"),
    path("predictmod/ehr-sample/", views.ehr_sample, name="pm-ehr-sample"),
    path("ping/", views.ping, name="ping"),
]
