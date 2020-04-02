from typing import List
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name: str = 'polls'
urlpatterns: List[URLPattern] = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.details, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
