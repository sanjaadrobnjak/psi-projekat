import pytest
import asyncio

from .test_skok_na_mrezu import (
    _get_users,
    _get_lobbies,
    _join_game,
    _get_players,
    _play_mreza_brojeva,
    _play_skok_na_mrezu_round,
    _both_await_msg
)
from .test_paukova_sifra import _play_paukova_sifra_round

async def _play_utekni_pauku_round(active, passive, letter=None, word=None):
    await _both_await_msg(active, passive, 'update_ui')
    await _both_await_msg(active, passive, 'update_timer')

    if letter:
        await active.send_json_to({
            'type': 'game5_answer',
            'letter': letter
        })
        await _both_await_msg(active, passive, 'guessed_letter')
    elif word:
        await active.send_json_to({
            'type': 'game5_answer',
            'word': word
        })
        await _both_await_msg(active, passive, 'guessed_word')


@pytest.mark.asyncio
async def test_utekni_pauku():
    blue_user, orange_user = await _get_users()
    blue_lobby, orange_lobby = await _get_lobbies(blue_user, orange_user)
    game_url = await _join_game(blue_lobby, orange_lobby)

    blue, orange = await _get_players(game_url, blue_user, orange_user)

    await _play_mreza_brojeva(blue, orange)

    for _ in range(10):
        await _play_skok_na_mrezu_round(blue, orange)

    await _play_paukova_sifra_round(blue, orange)
    await _play_paukova_sifra_round(orange, blue)


    await _play_utekni_pauku_round(blue, orange, letter='a')
    await _play_utekni_pauku_round(blue, orange, letter='v')
    await _play_utekni_pauku_round(blue, orange, letter='i')
    await _play_utekni_pauku_round(blue, orange, letter='n')
    await _play_utekni_pauku_round(blue, orange, letter='o')
    await _play_utekni_pauku_round(blue, orange, letter='g')
    await _play_utekni_pauku_round(blue, orange, letter='u')
    await _play_utekni_pauku_round(blue, orange, word='nepoztac')
    await _play_utekni_pauku_round(blue, orange, word='vinograd')
    
    # await _play_utekni_pauku_round(orange, blue, letter='a')
    # await _play_utekni_pauku_round(orange, blue, letter='v')
    # await _play_utekni_pauku_round(orange, blue, letter='i')
    # await _play_utekni_pauku_round(orange, blue, letter='n')
    # await _play_utekni_pauku_round(orange, blue, letter='o')
    # await _play_utekni_pauku_round(orange, blue, letter='g')
    # await _play_utekni_pauku_round(orange, blue, letter='u')
    # await _play_utekni_pauku_round(orange, blue, word='nepoztac')
    # await _play_utekni_pauku_round(orange, blue, word='vinograd')
    