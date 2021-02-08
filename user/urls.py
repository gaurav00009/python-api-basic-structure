# from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views  # import this
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('api/users/', include('user.api')),
]
