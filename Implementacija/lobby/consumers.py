from app.models import Korisnik
from app.models import Okrsaj
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    _queued_consumer = None

    async def connect(self):
        if 'user' not in self.scope or not self.scope['user'].is_authenticated:
            await self.close()
            return
        await self.accept()
        if LobbyConsumer._queued_consumer is None:
            LobbyConsumer._queued_consumer = self
        else:
            blue_user = LobbyConsumer._queued_consumer.scope['user']
            orange_user = self.scope['user']
            k1 = await Korisnik.objects.aget(pk=blue_user)
            k2 = await Korisnik.objects.aget(pk=orange_user)
            game = Okrsaj(
                Igrac1=k1,
                Igrac2=k2,
            )
            await game.asave()
            game_url = {
                'gameUrl': f'/games/{game.id}'
            }
            await self.send_json(game_url)
            await LobbyConsumer._queued_consumer.send_json(game_url)
            LobbyConsumer._queued_consumer = None

    async def disconnect(self, code):
        if LobbyConsumer._queued_consumer:
            LobbyConsumer._queued_consumer = None
