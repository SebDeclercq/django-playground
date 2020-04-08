"""biblio_support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from typing import List
from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLPattern
from rest_framework import routers
from csv_to_genie2 import views


from rest_framework_simplejwt import views as jwt_views

router: routers.DefaultRouter = routers.DefaultRouter()
router.register('standards', views.StandardViewSet)
router.register('files', views.FileViewSet)

app_name: str = 'genie2'

urlpatterns: List[URLPattern] = [
    path('api/', include(router.urls)),
    path(
        'api/token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]
