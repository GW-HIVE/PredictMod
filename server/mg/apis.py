#!/usr/bin/env python3
# /ehr/apis.py

"""MG APIs
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class UploadMetagenomicAPI(APIView):
    """Upload Metagenomic Record
    """

    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={
            200: "Metagenomic upload is sucessfull.",
            409: "Conflict.",
        },
        tags=["Metagenomic Records"],
    )

    def post(self, request):
        """POST
        """
        print(request)
        return Response(data={}, status=status.HTTP_200_OK)