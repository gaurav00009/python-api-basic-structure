import datetime

from rest_framework import serializers


from .models import (
    User
)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("id", "password", "username", 'api_key', 'date_of_birth')