from app.models import MrezaBrojeva
from app.models import OdigranaIgra
from app.models import Okrsaj
from channels.generic.websocket import JsonWebsocketConsumer
from collections import defaultdict

consumers = defaultdict(dict)

class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        game_id = self.scope['url_route']['kwargs']['game']
        game = Okrsaj.objects.get(pk=game_id)
        self.game = game
        username = self.scope['user'].username
        self.color = 'blue' if username == game.Igrac1.user.username else 'orange'
        consumers[game.id][self.color] = self
        consumers[game.id]['round'] = 1
        self.answer = None
        self.accept()
        mb = OdigranaIgra.objects.get(Okrsaj=game, RedniBrojIgre=1).Igra.mrezabrojeva
        self.send_json({
            'type': 'update_ui',
            'data': {
                'game1-helper1': mb.PomocniBroj1,
                'game1-helper2': mb.PomocniBroj2,
                'game1-helper3': mb.PomocniBroj3,
                'game1-helper4': mb.PomocniBroj4,
                'game1-helper5': mb.PomocniBroj5,
                'game1-helper6': mb.PomocniBroj6,
                'game1-wanted': mb.TrazeniBroj
            },
            'ui': 'game1'
        })

    @property
    def opponent_color(self):
        return 'blue' if self.color == 'orange' else 'orange'

    @property
    def opponent(self):
        return consumers[self.game.id][self.opponent_color] 

    def send_both(self, msg):
        self.send_json(msg)
        self.opponent.send_json(msg)
    
    def load_next_round(self):
        if consumers[self.game.id]['round'] < 2:
            mb = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=2).Igra.mrezabrojeva
            consumers[self.game.id]['round'] += 1
            update_ui = {
                'type': 'update_ui',
                'data': {
                    'game1-helper1': mb.PomocniBroj1,
                    'game1-helper2': mb.PomocniBroj2,
                    'game1-helper3': mb.PomocniBroj3,
                    'game1-helper4': mb.PomocniBroj4,
                    'game1-helper5': mb.PomocniBroj5,
                    'game1-helper6': mb.PomocniBroj6,
                    'game1-wanted': mb.TrazeniBroj,
                    'blue-player-score': self.game.blue_player_score(),
                    'orange-player-score': self.game.orange_player_score(),
                },
                'ui': 'game1'
            }
            self.send_both(update_ui)
        else:
            next_game = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=3)
            ... # Poslati ui naredne igre

    def receive_json(self, content):
        round_num = consumers[self.game.id]['round']
        if content['type'] == 'game1-answer':
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
            mb: MrezaBrojeva = round.Igra.mrezabrojeva
            my_answer = eval(content['answer']) # izracunaj izraz

            if self.opponent.answer is None:
                self.answer = my_answer
                return

            player1_answer = my_answer if self.color == 'blue' else self.opponent.answer
            player2_answer = my_answer if self.color == 'orange' else self.opponent.answer

            round.Igrac1Poeni, round.Igrac2Poeni = mb.get_player_points(player1_answer, player2_answer, round_num)
            round.save()
            self.load_next_round()

        elif content['type'] == 'time_ran_out':
            if round_num in (1, 2): # vrijeme isteklo za igru MrezaBrojeva
                round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
                self.answer = -999