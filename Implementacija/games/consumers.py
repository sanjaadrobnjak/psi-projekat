"""
    Ivan Cancar 2021/0604,
    Sanja Drobnjak 2021/0492
"""

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
from django.urls import reverse

import time

consumers = defaultdict(dict)

class GameConsumer(JsonWebsocketConsumer):
    PUBLIC_METHODS = ('game1_answer', 'game2_answer', 'game3_answer', 'time_ran_out')

    def connect(self):
        game_id = self.scope['url_route']['kwargs']['game']
        game = Okrsaj.objects.get(pk=game_id)
        self.game = game
        self.answer = None
        self.timeout = False
        username = self.scope['user'].username
        if username not in (game.Igrac1.user.username, game.Igrac2.user.username):
            return
        self.color = 'blue' if username == game.Igrac1.user.username else 'orange'
        consumers[game.id][self.color] = self
        self.round_num = 0
        self.answer_time=0      #za drugu igru
        self.attempts=0         #za trecu igru
        self.my_guess=None      #za trecu igru

        self.accept()
        if self.opponent_color in consumers[self.game.id]:
            self.load_next_round()

    @property
    def opponent_color(self):
        return 'blue' if self.color == 'orange' else 'orange'

    @property
    def opponent(self):
        return consumers[self.game.id][self.opponent_color] 

    @property
    def round_num(self):
        return consumers[self.game.id]['round']

    @round_num.setter
    def round_num(self, value):
        consumers[self.game.id]['round'] = value

    def send_both(self, msg):
        self.send_json(msg)
        self.opponent.send_json(msg)

    
    """
        omogucava pravilno upravljanje prelaskom izmedju rundi, azuriranje korisnickog 
        interfejsa i tajmera, kao i rukovanje zavrsetkom  tako sto se izracuna broj sledece 
        runde, i onda ako je:
        ♥ broj runde 1 ili 2, dohvataju se podaci za igru Mreza Brojeva, azurira se 
        korisnicki interfejs sa podacima o pomocnim brojevima i trazenom broju, azuriraju 
        se osvojeni poeni za oba igraca i ti azurirani podaci se salju klijentima, takodje, 
        postavlja se tajmer
        ♥broj runde u opsegu [3,12], dohvataju se podaci za igru Skok Na Mrezu, azurira se 
        korisnicki interfejs sa postavkom igre i osvojenim poenima za oba igraca i ti azurirani
        podaci se salju klijentima nakon cega se postavlja tajmer
        ♥broj runde je 13 ili 14, dohvataju se podaci za igru Paukova Sira, odredjuje se aktivni igrac, 
        tj igrac koji je na potezu, kao i pasivni igrac-igrac koji ceka da dodje na red, azurira se 
        korisnicki interfejs i salju se podaci aktivnom i pasivnom igracu, takodje postavlja se tajmer
        ♥ukoliko je broj runde van opsega, salje se klijentima poruka za preusmeravanje na stranicu sa 
        rezultatima, zatvara se WebSocket konekcija za oba igraca
        I na kraju, bez obzira na broj runde, broj trenutne runde se azurira na sledeci broj runde
    """
    def load_next_round(self):
        next_round = consumers[self.game.id]['round'] + 1
        if 1 <= next_round <= 2:
            mb = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=next_round).Igra.mrezabrojeva
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
            self.send_both({'type': 'update_timer', 'data': {'value': 20}})
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
            self.send_both({'type': 'update_timer', 'data': {'value': 10}})

        else:
            self.send_both({
                'type': 'redirect',
                'pathname': reverse('game-results-view', kwargs={'game':self.game.id})
            })
            self.close()
            self.opponent.close()
            del consumers[self.game.id]
        consumers[self.game.id]['round'] = next_round


    """
        koristi se za slanje azuriranja interfejsa odredjenom igracu putem WebSocket-a u trecoj igri Paukova Sifra,
        tako sto postavlja informaciju o tome da li je igrac aktivan pre slanja poruke;
        kao ulazne parametre prima JSON objekat koji sadrzi podatke za azuriranje korisnickog interfejsa, player-color tj boju igraca kojem se salje poruka i is_active koja odredjuje da li je igrac aktivan 
    """
    def send_json_to_player(self, update_ui, player_color, is_active=True):
        if player_color == 'blue':
            update_ui['data']['is_active'] = is_active
            consumers[self.game.id]['blue'].send_json(update_ui)
            print(f'Sending to blue: {update_ui}')
        else:
            update_ui['data']['is_active'] = is_active
            consumers[self.game.id]['orange'].send_json(update_ui)
            print(f'Sending to blue: {update_ui}')


    """
        rukuje primljenim JSON porukama od klijenta;
        kao ulazni parametar prima JSON objekat koji sadrzi podatke primljene od klijenta 
        tako sto na osnovu tipa poruke poziva odgovarajuce metode (game1_answer, game2_answer, game3_answer, time_ran_out) sa content kao argumentom
        ili salje poruku obojici igraca sa odgovarajucim podacima putem WebSocket-a ukoliko je tip poruke game3_key_input ili
        ako je tip poruke end_turn gde igracima u trecoj igri obrce aktivnog i pasivnog igraca, odnosno igrac koji je do sada bio aktivan onemogucava mu se dalji unos, dok se drugom igracu omogucava
    """
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
        elif method_name=='end_turn':
            player = content['player']
            opponent_color = 'orange' if player == 'blue' else 'blue'
            print(f'Ending turn for {player}, opponent is {opponent_color}')
            end_turn_update={
                'type': 'end_turn_update',
                'data': {
                    'is_active': True
                },
                'ui': 'game3'
            }
            
            self.send_json_to_player(end_turn_update, player, is_active=False)
            self.send_json_to_player(end_turn_update, opponent_color)
       

    def game1_calculate_score(self):
        round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=self.round_num)
        mb = round.Igra.mrezabrojeva

        for player in (self, self.opponent):
            try:
                player.answer = evaluate(player.answer, mb.nums) if player.answer is not None else 0
            except EvaluatorError:
                player.answer = 0

        ans1 = self.answer if self.color == 'blue' else self.opponent.answer
        ans2 = self.answer if self.color == 'orange' else self.opponent.answer

        to1 = self.timeout if self.color == 'blue' else self.opponent.timeout
        to2 = self.timeout if self.color == 'orange' else self.opponent.timeout

        round.Igrac1Poeni, round.Igrac2Poeni = mb.get_player_points(ans1, ans2, self.round_num, to1, to2)
        round.save()

    def game1_round_over(self):

        self.game1_calculate_score()

        self.answer = None
        self.opponent.answer = None
        self.timeout = False
        self.opponent.timeout = False

        self.load_next_round()

    def game1_answer(self, content):
        self.answer = content['answer']
        if self.opponent.answer is not None or self.opponent.timeout:
            self.game1_round_over()


    """
        rukuje situacijom kada istekne vreme u rundi, 
        tako sto postavlja promenljivu timeout na True za trenutnog igraca ako nije dao odgovor;
        ukoliko je protivniku vec isteklo vreme ili je dao odgovor poziva se odgovarajuca funkcija 
        (game1_round_over, game2_round_over, game3_round_over) da zavrsi trenutnu rundu igre
    """
    def time_ran_out(self, content):
        round_num = consumers[self.game.id]['round']
        if round_num in (1, 2): # vrijeme isteklo za igru MrezaBrojeva
            if self.answer is None:
                self.timeout = True
            if self.opponent.timeout or self.opponent.answer is not None:
                self.game1_round_over()
        if 3<=round_num<=12:  
            if self.answer is None:
                self.timeout = True
            if self.opponent.timeout or self.opponent.answer is not None:
                self.game2_round_over()
        if 13<=round_num<=14:  
            self.timeout=True
            self.game3_round_over()


    """
        zavrsava trenutnu rundu igre Skok Na Mrezu 
        tako sto racuna poene za oba igraca na osnovu njihovih odgovora, vremena odgovora i informacije da li im je isteklo vreme ili ne
        i resetuje odgovore i informaciju da li im je isteklo vreme ili ne i ucitava sledecu rundu
    """
    def game2_round_over(self):
        round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=self.round_num)
        snm=round.Igra.skoknamrezu
        player1_answer = self.answer if self.color == 'blue' else self.opponent.answer
        player2_answer = self.answer if self.color == 'orange' else self.opponent.answer

        player1_time = self.answer_time if self.color == 'blue' else self.opponent.answer_time
        player2_time = self.answer_time if self.color == 'orange' else self.opponent.answer_time

        to1 = self.timeout if self.color == 'blue' else self.opponent.timeout
        to2 = self.timeout if self.color == 'orange' else self.opponent.timeout

        print(f'game2_answer: {player1_answer=}, {player2_answer=}, {player1_time=}, {player2_time=},{to1=}, {to2=}')

        round.Igrac1Poeni, round.Igrac2Poeni=snm.get_player_points(player1_answer, player2_answer, player1_time, player2_time, to1, to2)
        round.save()
        self.answer = None
        self.answer_time=0
        self.opponent.answer = None
        self.timeout = False
        self.opponent.timeout = False
        self.load_next_round()

    """
        prima odgovor i vreme odgovora igraca 
        i proverava da li je protivnik vec poslao odgovor ili je isteklo vreme pre nego sto je pritisnuo dugme za potvrdu 
        i ukoliko jeste, poziva game2_round_over za zavrsetak runde
    """
    def game2_answer(self, content):
        #proveravam odgovor i ako je prazan, postavljam ga na 0
        self.answer = content['answer'] if content['answer'] else 0
        self.answer_time=content['answer_time']

        
        print(f'game2_answer:{self.opponent.answer=},{self.opponent.timeout=}')
        if self.opponent.answer is not None or self.opponent.timeout:
            self.game2_round_over()


    """
        zavrsava trenutnu rundu igre Paukova Sifra
        tako sto proverava da li je igracu isteklo vreme pre nego sto je iskoristio sve pokusaje i ukoliko jeste
        postavlja povratne informacije kao da je runda zavrsena (ako igracu nije isteklo vreme podtsvlja povratne informacije na osnovu odgovora igraca)
        i azurira poene na osnovu odgovora igraca, salje informacije o rundi obojici igraca, resetuje status runde i ucitava sledecu rundu
    """
    def game3_round_over(self):
        round_num = consumers[self.game.id]['round']
        try:
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        except OdigranaIgra.DoesNotExist:
            print(f"OdigranaIgra with Okrsaj={self.game.id} and RedniBrojIgre={round_num} does not exist.")
            return

        ps: PaukovaSifra = round.Igra.paukovasifra

        if self.timeout:
            my_guess = ''
            attempts = 7
            feedback = [""] * 5  # prazna povratna informacija jer nije bilo stvarnog pokušaja
            finished = False
        else:
            my_guess = self.my_guess
            attempts = self.attempts
            feedback = ps.get_feedback(my_guess)
            finished = feedback == ["pogodjenoNaMestu"] * 5

        active_player = 'blue' if round_num % 2 != 0 else 'orange'
        passive_player = 'orange' if active_player == 'blue' else 'blue'

        current_row = attempts - 1 if self.color == active_player else 6

        self.send_both({
            'type': 'guess',
            'data': {
                'feedback': feedback,
                'finished': finished,
                'currentRow': current_row,
                'targetWord': ps.TrazenaRec,
                'player': self.color
            },
            'ui': 'game3'
        })

        if attempts < 7:
            if self.color == 'blue':
                round.Igrac1Poeni = ps.get_player_and_score(attempts, my_guess)
            else:
                round.Igrac2Poeni = ps.get_player_and_score(attempts, my_guess)
        else:
            if self.color == 'orange' and self.color == passive_player:
                round.Igrac2Poeni = ps.get_player_and_score(attempts, my_guess)
            elif self.color == 'blue' and self.color == passive_player:
                round.Igrac1Poeni = ps.get_player_and_score(attempts, my_guess)

        round.save()
        self.load_next_round()


    """
        funkcija obradjuje odgovor igraca u trecoj igri Paukova Sifra, 
        tako sto najpre cuva rec koju je igrac pogodio kao i broj pokusaja iz poruke klijenta, 
        dohvata potrebne informacije o rundi iz objekta OdigranaIgra kao i informacije da li je igac pogodio zadatu rec pomocu objekta PaukovaSifra;
        zatim salje poruku klijentima, koja sadrzi povratne informacije o tacnosti reci koju je korisnik uneo, da li je runda gotova, trenutnom redu, zadatoj reci,igracu koji je na potezu;
        nakon toga se azuriraju poeni igracu koji je na potezu u zavisnosti tacnosti reci koju je uneo;
        i na kraju se cuva stanje i prelazi na sledecu rundu ukoliko su iskorisceni svi pokusaji ili ukoliko je zadata  rec pogodjena
    """
    def game3_answer(self, content):
        
        self.my_guess=content['word']
        self.attempts=content['attempts']
        
        round_num = consumers[self.game.id]['round']
        try:
            round = OdigranaIgra.objects.get(Okrsaj=self.game, RedniBrojIgre=round_num)
        except OdigranaIgra.DoesNotExist:
            print(f"OdigranaIgra with Okrsaj={self.game.id} and RedniBrojIgre={round_num} does not exist.")
            return
        ps: PaukovaSifra = round.Igra.paukovasifra
        feedback=ps.get_feedback(self.my_guess)
        #self.color, points=ps.get_player_and_score(attempts, my_guess, self.color)
        finished=feedback==["pogodjenoNaMestu"]*5

        active_player = 'blue' if round_num % 2 != 0 else 'orange'
        passive_player = 'orange' if active_player == 'blue' else 'blue'
        

        print(f'game3_answer: {feedback=}, {finished=}, {self.color=}, {self.my_guess=}, {self.attempts=}') # Dodat red za proveru

        current_row = self.attempts - 1 if self.color == active_player else 6
        
        self.send_both({
            'type': 'guess',
            'data': {
                'feedback': feedback,
                'finished': finished,
                'currentRow' : current_row,
                'targetWord' : ps.TrazenaRec,
                'player' : self.color
                
            },
            'ui': 'game3'
        })
        
        if self.attempts < 7:
            if self.color == 'blue':
                round.Igrac1Poeni = ps.get_player_and_score(self.attempts, self.my_guess)
                print(f'game3_answer: {round.Igrac1Poeni=}, {round.Igrac2Poeni=}')
            else:
                round.Igrac2Poeni = ps.get_player_and_score(self.attempts, self.my_guess)
                print(f'game3_answer: {round.Igrac1Poeni=}, {round.Igrac2Poeni=}')
        else:  # Ovo je sedmi pokusaj
            if self.color == 'orange' and self.color==passive_player:
                # Protivnicki igrac je 'orange', njemu se dodaju poeni
                round.Igrac2Poeni = ps.get_player_and_score(self.attempts, self.my_guess)
                print(f'game3_answer (sedmi pokusaj): {round.Igrac1Poeni=}, {round.Igrac2Poeni=}')
            elif self.color=='blue' and self.color==passive_player:
                # Protivnicki igrac je 'blue', njemu se dodaju poeni
                round.Igrac1Poeni = ps.get_player_and_score(self.attempts, self.my_guess)
                print(f'game3_answer (sedmi pokusaj): {round.Igrac1Poeni=}, {round.Igrac2Poeni=}')


        round.save()
        if finished or self.attempts==7:
            #self.game3_round_over()
            self.load_next_round()

        