#!/usr/bin/env python3
# /ehr/apis.py

"""EHR APIs
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class UploadEhrAPI(APIView):
    """Upload EHR Record
    """

    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={
            200: "EHR upload is sucessfull.",
            409: "Conflict.",
        },
        tags=["Electronic Healt Records"],
    )

    def post(self, request):
        """POST
        """
        print(request)
        return Response(data={}, status=status.HTTP_200_OK)