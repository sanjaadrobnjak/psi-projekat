from app.models import MrezaBrojeva
from app.models import OdigranaIgra
from app.models import Okrsaj
from channels.generic.websocket import JsonWebsocketConsumer
from collections import defaultdict
from .evaluator import EvaluatorError
from .evaluator import evaluate
from operator import methodcaller

from app.models import SkokNaMrezu
from app.models import PaukovaSifra
from django.http import JsonResponse

import time

consumers = defaultdict(dict)

class GameConsumer(JsonWebsocketConsumer):
    PUBLIC_METHODS = ('game1_answer', 'game2_answer', 'game3_answer', 'time_ran_out')

    def connect(self):
        game_id = self.scope['url_route']['kwargs']['game']
        game = Okrsaj.objects.get(pk=game_id)
        self.game = game
        username = self.scope['user'].username
        if username != game.Igrac1.user.username and username != game.Igrac2.user.username:
            return
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
        next_round = consumers[self.game.id]['round'] + 1
        if next_round == 2:
            mb = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=2).Igra.mrezabrojeva
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
            self.send_both({'type': 'update_timer', 'data': {'value': 60}})
        elif 3<=next_round<=12:
            next_game = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=next_round).Igra.skoknamrezu
            update_ui={
                'type': 'update_ui',
                'data': {
                    'game2-helper1': next_game.Postavka,
                    'blue-player-score': self.game.blue_player_score(),
                    'orange-player-score': self.game.orange_player_score()
                },
                'ui': 'game2'
            }
            self.send_both(update_ui)
            self.send_both({'type': 'update_timer', 'data': {'value': 15}})

        elif 13<=next_round<=14:
            next_game=OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=next_round).Igra.paukovasifra
            active_player = 'blue' if next_round % 2 != 0 else 'orange'
            passive_player = 'orange' if active_player == 'blue' else 'blue'
            update_ui={
                'type' : 'update_ui',
                'data' : {
                    'is_active':True,
                    'blue-player-score': self.game.blue_player_score(),
                    'orange-player-score': self.game.orange_player_score()
                },
                'ui' : 'game3'
            }

            self.send_json_to_player(update_ui, active_player)
            self.send_json_to_player(update_ui, passive_player, is_active=False)
            #self.send_both(update_ui)
            self.send_both({'type': 'update_timer', 'data': {'value': 60}})

        else:
            ...#sledeca igra
        consumers[self.game.id]['round'] = next_round

    def send_json_to_player(self, update_ui, player_color, is_active=True):
        if player_color == 'blue':
            update_ui['data']['is_active'] = is_active
            consumers[self.game.id]['blue'].send_json(update_ui)
        else:
            update_ui['data']['is_active'] = is_active
            consumers[self.game.id]['orange'].send_json(update_ui)

    def receive_json(self, content):
        if 'type' not in content:
            return
        method_name = content['type']
        if method_name in self.PUBLIC_METHODS:
            methodcaller(method_name, content)(self)
        elif method_name=='game3_key_input':
            self.send_both({
                'type' : 'game3_key_input',
                'data' : content['data']
            })

    
    def game1_answer(self, content):
        round_num = consumers[self.game.id]['round']
        round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        mb: MrezaBrojeva = round.Igra.mrezabrojeva

        try:
            self.answer = evaluate(content['answer'], mb.nums) # izracunaj izraz
        except EvaluatorError:
            self.answer = 0

        if self.opponent.answer is None:
            return

        player1_answer = self.answer if self.color == 'blue' else self.opponent.answer
        player2_answer = self.answer if self.color == 'orange' else self.opponent.answer

        round.Igrac1Poeni, round.Igrac2Poeni = mb.get_player_points(player1_answer, player2_answer, round_num)
        round.save()
        self.answer = None
        self.opponent.answer = None
        self.load_next_round()

    def time_ran_out(self, content):
        round_num = consumers[self.game.id]['round']
        if round_num in (1, 2): # vrijeme isteklo za igru MrezaBrojeva
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
            self.answer = -999
        if round_num in (3,12):  
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
            self.answer=-99999
        if round_num in (13,14):  
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
            self.answer=-99999


    def game2_answer(self, content):
        round_num = consumers[self.game.id]['round']
        try:
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        except OdigranaIgra.DoesNotExist:
            print(f"OdigranaIgra with Okrsaj={self.game.id} and RedniBrojIgre={round_num} does not exist.")
            return
        snm: SkokNaMrezu=round.Igra.skoknamrezu
        self.answer=content['answer']
        answer_time=content['answer_time']

        print(f'game2_answer: {self.answer=}, {self.opponent.answer=}')
        if self.opponent.answer is None:
            self.answer_time=answer_time
            return

        player1_answer = self.answer if self.color == 'blue' else self.opponent.answer
        player2_answer = self.answer if self.color == 'orange' else self.opponent.answer

        player1_time = answer_time if self.color == 'blue' else self.opponent.answer_time
        player2_time = answer_time if self.color == 'orange' else self.opponent.answer_time

        round.Igrac1Poeni, round.Igrac2Poeni=snm.get_player_points(player1_answer, player2_answer, round_num, player1_time, player2_time)
        round.save()
        self.answer = None
        self.opponent.answer = None
        self.load_next_round()

    def game3_answer(self, content):
        round_num = consumers[self.game.id]['round']
        #round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        try:
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        except OdigranaIgra.DoesNotExist:
            print(f"OdigranaIgra with Okrsaj={self.game.id} and RedniBrojIgre={round_num} does not exist.")
            return
        ps: PaukovaSifra = round.Igra.paukovasifra
        my_guess=content['word']
        attempts=content['attempts']
        feedback=ps.get_feedback(my_guess)
        self.color, points=ps.get_player_and_score(attempts, my_guess, self.color)
        finished=feedback==["pogodjenoNaMestu"]*5

        active_player = 'blue' if round_num % 2 != 0 else 'orange'
        passive_player = 'orange' if active_player == 'blue' else 'blue'

        print(f'game3_answer: {feedback=}, {finished=}, {self.color=}, {points=}, {my_guess=}, {attempts=}') # Dodajte ovaj red za proveru

        current_row = attempts - 1 if self.color == active_player else 6
        last_chance=True if attempts>=6 else False
        self.send_both({
            'type': 'guess',
            'data': {
                'feedback': feedback,
                'points': points,
                'finished': finished,
                'currentRow' : current_row,
                'targetWord' : ps.TrazenaRec,
                'player' : self.color
                
            },
            'ui': 'game3'
        })

        

        round.save()
        if finished:
            self.load_next_round()
        else:
            if attempts >= 6:
                self.send_json_to_player({
                    'type': 'update_ui',
                    'data': {'is_active': False},
                    'ui': 'game3'
                }, self.color)
                self.send_json_to_player({
                    'type': 'update_ui',
                    'data': {'is_active': True},
                    'ui': 'game3'
                }, self.opponent_color)
            if attempts==7:
                self.load_next_round()
