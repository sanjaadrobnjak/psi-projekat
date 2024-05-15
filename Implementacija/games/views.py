from django.shortcuts import render
from django.views import View
from app.models import Okrsaj
# Create your views here.

class GameView(View):
    def get(self, request, game):
        game = Okrsaj.objects.get(pk=game)
        my_color = 'blue' if request.user.username == game.Igrac1.user.username else 'orange'
        return render(request, 'games/game_main.html', {
            'blue_player': game.Igrac1,
            'orange_player': game.Igrac2,
            'my_color': my_color
        })
