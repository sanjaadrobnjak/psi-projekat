from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/games/<int:game>', consumers.GameConsumer.as_asgi()),
    path('ws/games/', consumers.GameConsumer.as_asgi()),
]