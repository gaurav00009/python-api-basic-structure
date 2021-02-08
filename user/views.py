from django.shortcuts import render
from django.conf.urls import url
from rest_framework.parsers import JSONParser

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from packages.exceptions import EmailExistException, FieldRequiredException, UnauthorizedException
from packages.request import validator
from packages.response import parsejson
from .models import (
    User
)
from .schemas import (
    RegisterSchema
)
from .serializers import (
    RegisterUserSerializer
)


# Create your views here.
class RegisterApiView(APIView):
    @swagger_auto_schema(
        operation_id="Register Parent",
        operation_summary="Register a parent",
        operation_decription="Register a parent",
        manual_parameters=RegisterSchema.params,
        response=RegisterSchema.response_docs,
    )
    @validator(api=False)
    def post(self, request, userdetail=None, verson=None, format=None):
        data = request.data
        if not data.get("first_name") or not data.get("email"):
            field = "First name" if not data.get("first_name") else ("email")
            raise FieldRequiredException(field + " is required")
        if User.getUserByEmail(data.get("email")):
            raise EmailExistException("This email address already exists in our system.")
       
        user_serializer = RegisterUserSerializer(
            data=data,
        )
        if user_serializer.is_valid():
            source = request.META["HTTP_SOURCE"]
            userObj = user_serializer.save(
                is_active=False,
                role_id=1,
                username=data.get("email"),
                password="",
            )
            userObj.register_from = source
            userObj.save()
            return Response(
                parsejson("User registration successful", {}, 200),
                status=status.HTTP_201_CREATED,
            )
        copy_errors = user_serializer.errors.copy()
        return Response(
            parsejson(copy_errors, "", status=400), status=status.HTTP_200_OK
        )