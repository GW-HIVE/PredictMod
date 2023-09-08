#!/usr/bin/env python3
"""URLs for the Electronic Health Record endpoints
"""

from django.urls import path, re_path
from ehr.apis import UploadEhrAPI

urlpatterns = [
    path("upload", UploadEhrAPI.as_view()),
]