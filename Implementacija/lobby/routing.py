from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/lobby/', consumers.LobbyConsumer.as_asgi(), name='lobby'),
]