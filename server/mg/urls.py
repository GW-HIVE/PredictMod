#!/usr/bin/env python3
"""URLs for the Metagenomic endpoints
"""

from django.urls import path, re_path
from mg.apis import UploadMetagenomicAPI

urlpatterns = [
    path("upload", UploadMetagenomicAPI.as_view()),
]