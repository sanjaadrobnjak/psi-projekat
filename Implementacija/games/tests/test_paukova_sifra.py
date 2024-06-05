import pytest

from .test_skok_na_mrezu import _get_users
from .test_skok_na_mrezu import _get_lobbies
from .test_skok_na_mrezu import _join_game
from .test_skok_na_mrezu import _get_players
from .test_skok_na_mrezu import _play_mreza_brojeva
from .test_skok_na_mrezu import _play_skok_na_mrezu_round
from .test_skok_na_mrezu import _both_await_msg


async def _play_paukova_sifra_round(active, passive):
    await _both_await_msg(active, passive, 'update_ui')
    await _both_await_msg(active, passive, 'update_timer')
    await active.send_json_to({
        'type': 'game3_answer',
        'word': 'avion',
        'attempts': 1
    })
    await _both_await_msg(active, passive, 'guess')


@pytest.mark.asyncio
async def test_paukova_sifra():
    blue_user, orange_user = await _get_users()
    blue_lobby, orange_lobby = await _get_lobbies(blue_user, orange_user)
    game_url = await _join_game(blue_lobby, orange_lobby)

    blue, orange = await _get_players(game_url, blue_user, orange_user)

    await _play_mreza_brojeva(blue, orange)

    for _ in range(10):
        await _play_skok_na_mrezu_round(blue, orange)


    await _play_paukova_sifra_round(blue, orange)
    # await _play_paukova_sifra_round(orange, blue)
