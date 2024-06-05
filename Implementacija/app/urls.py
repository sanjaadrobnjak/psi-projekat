"""
    Ivan Cancar 2021/0604
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-view"),

    # iz igre 4 ka igri 5
    # path('game5/', views.game5, name='game5'),
]