from drf_yasg import openapi
from rest_framework.views import APIView

from packages.response import getdocs


class RegisterSchema():
    params = [
        openapi.Parameter(
            "token",
            openapi.IN_HEADER,
            description="Access Token",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "source",
            openapi.IN_HEADER,
            description="Source [ iOS, ANDROID, WEB, ADMIN ]",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "first_name",
            openapi.IN_FORM,
            description="First Name",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            "last_name",
            openapi.IN_FORM,
            description="Last Name",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "email",
            openapi.IN_FORM,
            description="Email",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            "image",
            openapi.IN_FORM,
            description="Profile Picture",
            type=openapi.TYPE_FILE,
            required=False
        ),
    ]
    response_docs = getdocs()