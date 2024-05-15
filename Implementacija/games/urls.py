from django.urls import path
from . import views

urlpatterns = [
    path('<int:game>', views.GameView.as_view(), name='game-view'),
]