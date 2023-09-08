#!/usr/bin/env python3

"""PredictMod Server URL Configuration
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

VERSION = settings.VERSION

schema_view = get_schema_view(
    openapi.Info(
        title="PredictMod API",
        default_version=VERSION,
        description="PredictMod is a web app created to inform physicians'"
            "decisions. PredictMod takes metagenomic gastrointestinal (GI) "
            "microbiome and electronic health record (EHR) data as input and "
            "uses a machine learning algorithm to form predictions of whether "
            "the ketogenic diet may be successful.",
        terms_of_service="https://github.com/GW-HIVE/PredictMod/blob/main/LICENSE",
        contact=openapi.Contact(email="mazumder_lab@gwu.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Here
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("admin/", admin.site.urls),
    path("ehr/", include("ehr.urls")),
    path("mg/", include("mg.urls")),
]
