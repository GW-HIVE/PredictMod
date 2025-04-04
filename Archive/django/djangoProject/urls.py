"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from predictmod import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Predict Mod",
        default_version="v1.0",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mazumder_lab@gwu.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # re_path('gfkb/predict.*/admin/', admin.site.urls),
    # re_path('gfkb/predict.*/index/', views.index),
    # re_path('gfkb/predict.*/upload/', views.index),
    # re_path('gfkb/predict.*/', views.index),
    path("admin/", admin.site.urls),
    path("index/", views.index),
    path("EHR/", views.ehr),
    path("MG/", views.metagenomic),
    path("EHR/ehr-upload/", views.ehr_upload),
    path("MG/mg-upload/", views.mg_upload),
    path("", views.index),
    path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
