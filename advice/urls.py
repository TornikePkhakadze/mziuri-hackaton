"""
URL configuration for advice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (TokenObtainPairView,)


schema_view = get_schema_view(
    openapi.Info(
        title=" API for E-Commerce platform",
        default_version='v1',
        description='E-Commerce project for Mziuri'

    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name= 'swagger-ui'),
    path('admin/', admin.site.urls),
    path("", include("users.urls")),
    path("", include("products.urls")),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
