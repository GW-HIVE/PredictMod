from django.urls import path

from . import views

urlpatterns = [
    path("mg-upload/", views.mg_upload, name="mg-upload"),
    path("ehr-upload/", views.ehr_upload, name="ehr-upload"),
    path("ping/", views.ping, name="ping"),
]
