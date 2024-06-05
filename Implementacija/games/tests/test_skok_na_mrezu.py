import time

from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.db.models import Sum
from django.contrib.auth.models import User
import pytest

from app.models import OdigranaIgra
from games.routing import websocket_urlpatterns
from lobby.consumers import LobbyConsumer


class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, headers=None, subprotocols=None, user=None):
        super(AuthWebsocketCommunicator, self).__init__(application, path, headers, subprotocols)
        if user is not None:
            self.scope['user'] = user


async def _await_msg(player, type):
    content = await player.receive_json_from()
    assert content['type'] == type
    return content


async def _both_await_msg(player1, player2, type):
    content1 = await _await_msg(player1, type)
    content2 = await _await_msg(player2, type)
    return content1, content2


async def _play_mreza_brojeva_round(blue, orange):
    await _both_await_msg(blue, orange, 'update_ui')
    await _both_await_msg(blue, orange, 'update_timer')

    await blue.send_json_to({
        'type': 'game1_answer',
        'answer': '0'
    })
    await orange.send_json_to({
        'type': 'game1_answer',
        'answer': '0'
    })


async def _play_mreza_brojeva(blue, orange):
    for _ in range(2):
        await _play_mreza_brojeva_round(blue, orange)


async def _get_users():
    blue_user = await User.objects.aget(username='ivan')
    orange_user = await User.objects.aget(username='luka')
    return blue_user, orange_user


async def _get_lobbies(blue_user, orange_user):
    lobby = LobbyConsumer.as_asgi()
    blue_lobby = AuthWebsocketCommunicator(lobby, '/ws/lobby', user=blue_user)
    orange_lobby = AuthWebsocketCommunicator(lobby, '/ws/lobby', user=orange_user)
    blue_connected, _ = await blue_lobby.connect()
    assert blue_connected
    orange_connected, _ = await orange_lobby.connect()
    assert orange_connected
    return blue_lobby, orange_lobby    


async def _join_game(blue_lobby, orange_lobby):
    blue_response = await blue_lobby.receive_json_from()
    orange_response = await orange_lobby.receive_json_from()

    assert blue_response['gameUrl'] == orange_response['gameUrl']
    return '/ws' + blue_response['gameUrl']


async def _get_players(game_url, blue_user, orange_user):
    game = URLRouter(websocket_urlpatterns)
    blue = AuthWebsocketCommunicator(game, game_url, user=blue_user)
    orange = AuthWebsocketCommunicator(game, game_url, user=orange_user)

    blue_connected, _ = await blue.connect()
    assert blue_connected

    orange_connected, _ = await orange.connect()
    assert orange_connected

    return blue, orange


async def _play_skok_na_mrezu_round(blue, orange):
    await _both_await_msg(blue, orange, 'update_ui')
    await _both_await_msg(blue, orange, 'update_timer')

    await blue.send_json_to({
        'type': 'game2_answer',
        'answer': 0,
        'answer_time': int(time.time())
    })
    await orange.send_json_to({
        'type': 'game2_answer',
        'answer': 0,
        'answer_time': int(time.time())
    })


@pytest.mark.asyncio
async def test_skok_na_mrezu():
    blue_user, orange_user = await _get_users()
    blue_lobby, orange_lobby = await _get_lobbies(blue_user, orange_user)
    game_url = await _join_game(blue_lobby, orange_lobby)

    blue, orange = await _get_players(game_url, blue_user, orange_user)

    await _play_mreza_brojeva(blue, orange)

    for _ in range(10):
        await _play_skok_na_mrezu_round(blue, orange)

    @sync_to_async
    def blue_points():
        return OdigranaIgra.objects.filter(Okrsaj__Igrac1__user=blue_user)\
            .aggregate(total_sum=Sum('Igrac1Poeni'))['total_sum']

    @sync_to_async
    def orange_points():
        return OdigranaIgra.objects.filter(Okrsaj__Igrac2__user=orange_user)\
        .aggregate(total_sum=Sum('Igrac2Poeni'))['total_sum']

    points1 = await blue_points()

    assert points1 is not None
    
    points2 = await orange_points()
    assert points2 is not None
