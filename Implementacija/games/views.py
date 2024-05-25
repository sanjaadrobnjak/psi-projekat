from app.models import Okrsaj
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class GameView(View):
    @method_decorator(login_required)
    def get(self, request, game):
        game = Okrsaj.objects.get(pk=game)
        player1 = game.Igrac1.user.username
        player2 = game.Igrac2.user.username
        if request.user.username not in (player1, player2):
            return HttpResponseNotAllowed()
        return render(request, 'games/game_main.html', {
            'blue_player': game.Igrac1,
            'orange_player': game.Igrac2,
        })
