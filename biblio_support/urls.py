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
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns: List[URLPattern] = [
    path('admin/', admin.site.urls),
    path('genie2/', include('csv_to_genie2.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
