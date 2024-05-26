from app.models import OdigranaIgra
from app.models import Okrsaj
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
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

class GameResultsView(View):
    def _player_score(self, game, rounds):
        s = OdigranaIgra.objects.filter(Okrsaj=game, RedniBrojIgre__in=rounds).aggregate(
            blue_sum=Sum('Igrac1Poeni'),
            orange_sum=Sum('Igrac2Poeni')
        )
        return s['blue_sum'] or 0, s['orange_sum'] or 0

    def get(self, request, game):
        game = Okrsaj.objects.get(pk=game)
        blue_player_mb, orange_player_mb = self._player_score(game, (1, 2))
        blue_player_snm, orange_player_snm = self._player_score(game, tuple(range(3, 13)))
        blue_player_ps, orange_player_ps = self._player_score(game, (13, 14))
        blue_player_u, orange_player_u = self._player_score(game, (15, 16))
        blue_player_up, orange_player_up = self._player_score(game, (17, 18))
        return render(request, 'games/results.html', {
            'blue_player_score': game.blue_player_score(),
            'orange_player_score': game.orange_player_score(),
            'blue_player': game.Igrac1,
            'orange_player': game.Igrac2,
            'blue_player_mb': blue_player_mb,
            'orange_player_mb': orange_player_mb,
            'blue_player_snm': blue_player_snm,
            'orange_player_snm': orange_player_snm,
            'blue_player_ps': blue_player_ps,
            'orange_player_ps': orange_player_ps,
            'blue_player_u': blue_player_u,
            'orange_player_u': orange_player_u,
            'blue_player_up': blue_player_up,
            'orange_player_up': orange_player_up
        })