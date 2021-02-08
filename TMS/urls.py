"""TMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views #import this

schema_view = get_schema_view(
    openapi.Info(
        title="Edflow API",
        default_version="v1",
        description="Provide REST API for Edflow application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path("", include("user.urls")),
    path("schema/", schema_view.with_ui("swagger", cache_timeout=0), name="schema"),

] + router.urls
