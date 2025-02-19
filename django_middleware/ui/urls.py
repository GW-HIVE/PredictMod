from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.file_upload, name="upload"),
    path("download/", views.file_download, name="download"),
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
]
