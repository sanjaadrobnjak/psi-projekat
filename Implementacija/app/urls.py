"""
    Ivan Cancar 2021/0604
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index-view"),
]
