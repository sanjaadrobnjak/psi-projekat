from app.models import Korisnik
from app.models import Okrsaj
from channels.generic.websocket import WebsocketConsumer
import json


_queued_consumer = None

class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope['user'].is_authenticated:
            self.close()
            return
        global _queued_consumer
        self.accept()
        if _queued_consumer is None:
            _queued_consumer = self
        else:
            k1 = Korisnik.objects.get(pk=_queued_consumer.scope['user'])
            k2 = Korisnik.objects.get(pk=self.scope['user'])
            game = Okrsaj(Igrac1=k1, Igrac2=k2)
            game.save()
            self.send(text_data=json.dumps({'gameUrl': f'/games/{game.id}'}))
            _queued_consumer.send(text_data=json.dumps({'gameUrl': f'/games/{game.id}'}))
            _queued_consumer = None
    
    def disconnect(self, code):
        if _queued_consumer:
            _queued_consumer = None
