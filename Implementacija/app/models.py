from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from .mixins import RandomSampleMixin


class Korisnik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    TIP = [("A", "Admin"), ("M", "Moderator"), ("I", "Igrac"), ("G", "Gost")]
    Tip = models.CharField(max_length=1, choices=TIP)

    Ime = models.CharField(max_length=255, null=True)
    Prezime = models.CharField(max_length=255, null=True)
    BrojTrofeja = models.IntegerField(default=0)
    BrojPoena = models.IntegerField(default=0)


class Turnir(models.Model):
    pass


class Ucestvuje(models.Model):
    Korisnik = models.ForeignKey(Korisnik, on_delete=models.RESTRICT)
    Turnir = models.ForeignKey(Turnir, on_delete=models.RESTRICT)
    OsvojenoMesto = models.IntegerField(default=0)
    OsvojeniBrojTrofeja = models.IntegerField(default=0)


class Igra(models.Model):
    pass


class MrezaBrojeva(Igra, RandomSampleMixin):
    TrazeniBroj = models.IntegerField()
    PomocniBroj1 = models.IntegerField()
    PomocniBroj2 = models.IntegerField()
    PomocniBroj3 = models.IntegerField()
    PomocniBroj4 = models.IntegerField()
    PomocniBroj5 = models.IntegerField()
    PomocniBroj6 = models.IntegerField()

    class Meta:
        verbose_name = "MrezaBrojeva"
        verbose_name_plural = "MrezaBrojeva"

    def get_winner_and_score(self, player1_answer, player2_answer, round):
        player1_diff = abs(player1_answer - self.TrazeniBroj)
        player2_diff = abs(player2_answer - self.TrazeniBroj)

        if player1_diff != player2_diff:
            winner = 'blue' if player1_diff < player2_diff else 'orange'
            winner_diff = min(player1_diff, player2_diff)
        else:
            winner= 'blue' if round == 1 else 'orange'
            winner_diff = player1_diff
        
        return winner, self._calculate_score(winner_diff)

    def _calculate_score(self, diff): 
        if diff == 0:
            return 30
        elif diff == 1:
            return 20
        elif diff <= 5:
            return 10
        elif diff <= 10:
            return 5
        return 0

    def get_player_points(self, player1_answer, player2_answer, round):
        winner_color, winner_score = self.get_winner_and_score(player1_answer, player2_answer, round)
        if winner_color == 'blue':
            return winner_score, 0
        return 0, winner_score


class SkokNaMrezu(Igra, RandomSampleMixin):
    Postavka = models.TextField()
    Odgovor = models.IntegerField()

    class Meta:
        verbose_name = "SkokNaMrezu"
        verbose_name_plural = "SkokNaMrezu"

    def get_winner_and_score(self, player1_answer, player2_answer, round, player1_time, player2_time):
        player1_answer=int(player1_answer)
        player2_answer=int(player2_answer)
        player1_diff = abs(player1_answer - self.Odgovor)
        player2_diff = abs(player2_answer - self.Odgovor)
        winner_score=0

        if player1_diff != player2_diff:
            # pobednik je ko je blizi odgovoru
            winner = 'blue' if player1_diff < player2_diff else 'orange'
            winner_score=3
        else:
            #ko je brze kliknuo
            #PROVVERITI
            if player1_time < player2_time:
                winner = 'blue'
                winner_score = 3
            elif player1_time > player2_time:
                winner = 'orange'
                winner_score = 3
            else:
                winner=None
                winner_score=0

        return winner, winner_score

    def get_player_points(self, player1_answer, player2_answer, round, player1_time, player2_time):
        winner_color, winner_score = self.get_winner_and_score(player1_answer, player2_answer, round, player1_time, player2_time)
        if winner_color == 'blue':
            return winner_score, 0
        return 0, winner_score




class PaukovaSifra(Igra, RandomSampleMixin):
    TrazenaRec = models.CharField(max_length=20)

    class Meta:
        verbose_name = "PaukovaSifra"
        verbose_name_plural = "PaukovaSifra"


class Umrezavanje(Igra, RandomSampleMixin):
    TekstPitanja = models.TextField()
    Postavka1 = models.CharField(max_length=20)
    Odgovor1 = models.CharField(max_length=20)
    Postavka2 = models.CharField(max_length=20)
    Odgovor2 = models.CharField(max_length=20)
    Postavka3 = models.CharField(max_length=20)
    Odgovor3 = models.CharField(max_length=20)
    Postavka4 = models.CharField(max_length=20)
    Odgovor4 = models.CharField(max_length=20)
    Postavka5 = models.CharField(max_length=20)
    Odgovor5 = models.CharField(max_length=20)
    Postavka6 = models.CharField(max_length=20)
    Odgovor6 = models.CharField(max_length=20)
    Postavka7 = models.CharField(max_length=20)
    Odgovor7 = models.CharField(max_length=20)
    Postavka8 = models.CharField(max_length=20)
    Odgovor8 = models.CharField(max_length=20)
    Postavka9 = models.CharField(max_length=20)
    Odgovor9 = models.CharField(max_length=20)
    Postavka10 = models.CharField(max_length=20)
    Odgovor10 = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Umrezavanje"
        verbose_name_plural = "Umrezavanje"

    def calculate_points(self, player1_answers, player2_answers):
        #odgovori igrača su mi recnici (kljuc: postavka, vrednost: odgovor)
        # Ucitavam odgovore iz baze
        correct_answers = {
            'Postavka1': self.Odgovor1,
            'Postavka2': self.Odgovor2,
            'Postavka3': self.Odgovor3,
            'Postavka4': self.Odgovor4,
            'Postavka5': self.Odgovor5,
            'Postavka6': self.Odgovor6,
            'Postavka7': self.Odgovor7,
            'Postavka8': self.Odgovor8,
            'Postavka9': self.Odgovor9,
            'Postavka10': self.Odgovor10,
        }

        player1_score = 0
        player2_score = 0

        for postavka, odgovor in player1_answers.items():
            if correct_answers.get(postavka) == odgovor:
                player1_score += 3

        for postavka, odgovor in player2_answers.items():
            if correct_answers.get(postavka) == odgovor:
                player2_score += 3

        return player1_score, player2_score


class UtekniPauku(Igra, RandomSampleMixin):
    TrazenaRec = models.CharField(max_length=20)

    class Meta:
        verbose_name = "UtekniPauku"
        verbose_name_plural = "UtekniPauku"


class Okrsaj(models.Model):
    Igrac1 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")
    Igrac2 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")

    def blue_player_score(self):
        return OdigranaIgra.objects.filter(Okrsaj=self).aggregate(total_sum=Sum('Igrac1Poeni'))['total_sum']
    
    def orange_player_score(self):
        return OdigranaIgra.objects.filter(Okrsaj=self).aggregate(total_sum=Sum('Igrac2Poeni'))['total_sum']


class OdigranaIgra(models.Model):
    Okrsaj = models.ForeignKey(Okrsaj, on_delete=models.RESTRICT)
    Igra = models.ForeignKey(Igra, on_delete=models.RESTRICT)
    RedniBrojIgre = models.IntegerField() # 1 i 2 su MrezaBrojeva, ...
    Igrac1Poeni = models.IntegerField(null=True)
    Igrac2Poeni = models.IntegerField(null=True)


