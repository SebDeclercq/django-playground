from typing import List
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name: str = 'polls'
urlpatterns: List[URLPattern] = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
