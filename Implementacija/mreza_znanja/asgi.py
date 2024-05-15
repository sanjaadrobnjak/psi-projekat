from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from lobby.routing import websocket_urlpatterns as lobby_urls
from games.routing import websocket_urlpatterns as games_urls
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mreza_znanja.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(lobby_urls + games_urls)))
})
