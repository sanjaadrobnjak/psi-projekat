"""
    Ivan Cancar 2021/0604
"""
from django.urls import path
from . import views

urlpatterns = [
    path('<int:game>', views.GameView.as_view(), name='game-view'),
    path('<int:game>/results', views.GameResultsView.as_view(), name='game-results-view'),
]