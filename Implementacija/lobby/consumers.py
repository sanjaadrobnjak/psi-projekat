from app.models import Korisnik, SkokNaMrezu
from app.models import MrezaBrojeva
from app.models import OdigranaIgra
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
            game = Okrsaj(
                Igrac1=k1,
                Igrac2=k2,
            )
            game.save()
            mb1, mb2 = MrezaBrojeva.sample(2)
            OdigranaIgra(Okrsaj=game, Igra=mb1, RedniBrojIgre=1).save()
            OdigranaIgra(Okrsaj=game, Igra=mb2, RedniBrojIgre=2).save()

            #dodajem 10 pitanja za skok na mrezu
            """snm_games=SkokNaMrezu.sample(2)
            for i, snm_game in enumerate(snm_games, start=3):   #3-12 redni brojevi bi trebalo al sad je 2
                OdigranaIgra(Okrsaj=game, Igra=snm_game, RedniBrojIgre=i).save()"""
            snm1, snm2, snm3, snm4, snm5, snm6, snm7, snm8, snm9, snm10=SkokNaMrezu.sample(10)
            OdigranaIgra(Okrsaj=game, Igra=snm1, RedniBrojIgre=3).save()
            OdigranaIgra(Okrsaj=game, Igra=snm2, RedniBrojIgre=4).save()
            OdigranaIgra(Okrsaj=game, Igra=snm3, RedniBrojIgre=5).save()
            OdigranaIgra(Okrsaj=game, Igra=snm4, RedniBrojIgre=6).save()
            OdigranaIgra(Okrsaj=game, Igra=snm5, RedniBrojIgre=7).save()
            OdigranaIgra(Okrsaj=game, Igra=snm6, RedniBrojIgre=8).save()
            OdigranaIgra(Okrsaj=game, Igra=snm7, RedniBrojIgre=9).save()
            OdigranaIgra(Okrsaj=game, Igra=snm8, RedniBrojIgre=10).save()
            OdigranaIgra(Okrsaj=game, Igra=snm9, RedniBrojIgre=11).save()
            OdigranaIgra(Okrsaj=game, Igra=snm10, RedniBrojIgre=12).save()

            game.save()
            self.send(text_data=json.dumps({'gameUrl': f'/games/{game.id}'}))
            _queued_consumer.send(text_data=json.dumps({'gameUrl': f'/games/{game.id}'}))
            _queued_consumer = None

    def disconnect(self, code):
        global _queued_consumer
        if _queued_consumer:
            _queued_consumer = None
