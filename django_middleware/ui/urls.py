from django.urls import path

from . import views

urlpatterns = [
    # path("mg-upload/", views.mg_upload, name="mg-upload"),
    # path("ehr-upload/", views.ehr_upload, name="ehr-upload"),
    path("upload/", views.file_upload, name="upload"),
    path("download/", views.file_download, name="download"),
    # path("mg-sample/", views.mg_sample, name="mg-sample"),
    # path("ehr-sample/", views.ehr_sample, name="ehr-sample"),
    path("ping/", views.ping, name="ping"),
    path("live-data/", views.live_data, name="live-data"),
    path("query/", views.queries, name="queries"),
    path("query-conditions/", views.query_conditions, name="query-conditions"),
    path("query-interventions/", views.query_interventions, name="query-interventions"),
    path("query-input-data/", views.query_input_data, name="query-input-data"),
    path(
        "query-model-endpoints/",
        views.query_model_endpoints,
        name="query-model-endpoints",
    ),
    path("models/", views.models, name="models"),
    path("model-details/", views.model_details, name="model-details"),
    path("search/", views.search, name="search"),
    # path("predictmod/mg-upload/", views.mg_upload, name="pm-mg-upload"),
    # path("predictmod/ehr-upload/", views.ehr_upload, name="pm-ehr-upload"),
    # path("predictmod/mg-sample/", views.mg_sample, name="pm-mg-sample"),
    # path("predictmod/ehr-sample/", views.ehr_sample, name="pm-ehr-sample"),
    # path("predictmod/ping/", views.ping, name="ping"),
]
