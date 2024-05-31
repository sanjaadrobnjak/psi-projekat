"""
    Ivan Cancar 2021/0604,
    Sanja Drobnjak 2021/0492
    Luka Skoko 2021/0497
"""

from django.contrib.auth.models import User
import random
from django.db import models
from django.db.models import Sum
from .mixins import RandomSampleMixin


class Korisnik(models.Model):
    """\
    Ova klasa sadrzi dodatne informacije o korisniku sajta. Koristi model `auth.User`
    za cuvanje podataka za logovanje.
    """

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
    """\
    Bazna klasa za sve tipove igre. Koristi se u `app.OdigranaIgra`
    """

    pass


class MrezaBrojeva(Igra, RandomSampleMixin):
    """\
    Ova klasa predstavlja model za igru mreza brojeva. Njena polja sadrze trazeni broj i pomocne brojeve za datu igru.
    """

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
        """\
        Ova metoda izracunava pobednickog igraca i njegove poene na osnovu odogvora oba igraca i broja runde.
        """
        player1_diff = abs(player1_answer - self.TrazeniBroj)
        player2_diff = abs(player2_answer - self.TrazeniBroj)

        if player1_diff != player2_diff:
            winner = "blue" if player1_diff < player2_diff else "orange"
            winner_diff = min(player1_diff, player2_diff)
        else:
            winner = "blue" if round == 1 else "orange"
            winner_diff = player1_diff

        return winner, self._calculate_score(winner_diff)

    def _calculate_score(self, diff):
        """\
        Metoda za racunanje broja osvojenih poena na osnovu udaljenosti od tacnog
        odgovora
        """
        if diff == 0:
            return 30
        elif diff == 1:
            return 20
        elif diff <= 5:
            return 10
        elif diff <= 10:
            return 5
        return 0

    def get_player_points(self, player1_answer, player2_answer, round, to1, to2):
        """\
        Ova metoda izracunava broj osvojenih poena za oba igraca na osnovu njihovih odogvora, broja runde i informacije
        o tome da li je nekom od igraca isteklo vreme.
        """
        if to1 and to2:
            print("both timeout")
            return 0, 0
        if to1:
            print("t1 timeout")
            return 0, self._calculate_score(abs(player2_answer - self.TrazeniBroj))
        if to2:
            print("t2 timeout")
            return self._calculate_score(abs(player1_answer - self.TrazeniBroj)), 0
        print("no timeout")
        winner_color, winner_score = self.get_winner_and_score(
            player1_answer, player2_answer, round
        )
        if winner_color == "blue":
            return winner_score, 0
        return 0, winner_score

    @property
    def nums(self):
        """\
        Svojstvo nums vraca pomocne brojeve kao listu, radi lakse upotrebe.
        """
        return [
            self.PomocniBroj1,
            self.PomocniBroj2,
            self.PomocniBroj3,
            self.PomocniBroj4,
            self.PomocniBroj5,
            self.PomocniBroj6,
        ]


class SkokNaMrezu(Igra, RandomSampleMixin):
    """
    ova klasa predstavlja model igre Skok Na Mrezu i nasledjuje funkcionalnosti iz klasa Igra i RandomSampleMixin;
    polja klase Postavka i Odgovor su tekstualno i celobrojno polje koje predstavljaju postavku igre i tacan odgovor za postavku igre, respektivno
    """

    Postavka = models.TextField()
    Odgovor = models.IntegerField()

    class Meta:
        verbose_name = "SkokNaMrezu"
        verbose_name_plural = "SkokNaMrezu"

    def get_winner_and_score(
        self, player1_answer, player2_answer, player1_time, player2_time
    ):
        """
        odredjuje pobednika igre i vraca njegov rezultat na osnovu odgovora oba igraca i vremena kad asu pritisnuli dugme za potvrdu;
        metoda vraca tuple (winner, winner_score), gde je winner boja pobednika a winner_score rezultat
        """
        player1_answer = int(player1_answer)
        player2_answer = int(player2_answer)
        if player1_answer == 0 and player2_answer == 0:
            return None, 0
        player1_diff = abs(player1_answer - self.Odgovor)
        player2_diff = abs(player2_answer - self.Odgovor)
        winner_score = 0

        if player1_diff != player2_diff:  # pobednik je ko je blizi odgovoru
            winner = "blue" if player1_diff < player2_diff else "orange"
            winner_score = 3
        else:  # ko je brze kliknuo
            if player1_time < player2_time:
                winner = "blue"
                winner_score = 3
            elif player1_time > player2_time:
                winner = "orange"
                winner_score = 3
            else:
                winner = None
                winner_score = 0

        return winner, winner_score

    def get_player_points(
        self, player1_answer, player2_answer, player1_time, player2_time, to1, to2
    ):
        """
        odredjuje poene oba igraca na osnovu njih odgovora, vremena kada su pritisnuli dugme za potvrdu i informacije da li im je isteklo vreme pre nego sto su pritisnuli dugme za potvrdu,
        (ukoliko je igracu automatski osvaja 0 poena, dok u drugim slucajevima se poziva metoda get_winner_and_score za odredjivanje osvojenih poena za svakog igraca);
        metoda vraca tuple (player1_points, player2_points) koji predstavlja osvojene poene prvoog i drugog igraca
        """
        if to1 and to2:
            print("both timeout")
            return 0, 0
        if to1:
            if player2_answer != 0:
                return 0, 3
            return 0, 0
        if to2:
            if player1_answer != 0:
                return 3, 0
            return 0, 0

        winner_color, winner_score = self.get_winner_and_score(
            player1_answer, player2_answer, player1_time, player2_time
        )
        if winner_color == "blue":
            return winner_score, 0
        return 0, winner_score


class PaukovaSifra(Igra, RandomSampleMixin):
    """
    ova klasa predstavlja model igre Paukova Sifra i nasledjuje osnovne funkcionalnosti iz klsa Igra i RandomSampleMixin;
    polje klase TrazenaRec predstavlja tekstualno polje za rec koju igraci treba da pogode
    """

    TrazenaRec = models.CharField(max_length=20)

    class Meta:
        verbose_name = "PaukovaSifra"
        verbose_name_plural = "PaukovaSifra"

    def get_feedback(
        self, guess
    ):  # proverava stanje pokusaja igraca sa zadatom reci iz baze
        """
        proverava pokusaj igraca (ulazni parametar guess) u odnosu na zadatu rec,
        tako sto poredi svaki karakter u pokusaju sa odgovarajucim karakterom u trazenoj reci;
        kao rezultat vraca povratnu informaciju o tacnosti svakog slova u pokusaju
        """
        rec = self.TrazenaRec.upper()
        guess = guess.upper()
        feedback = []

        for i, letter in enumerate(guess):
            if rec[i] == letter:
                feedback.append("pogodjenoNaMestu")
            elif letter in rec:
                feedback.append("pogodjenoNijeNaMestu")
            else:
                feedback.append("nijePogodjeno")

        return feedback

    def get_score(self, attempts):
        """
        odredjuje broj poena na osnovu broja pokusaja (ulazni parametar attempts) potrebnih da se pogodi rec;
        kao rezultat vraca odgovarajuci broj poena u zavisnosti od broja pokusaja
        """
        if attempts == 1 or attempts == 2:
            return 20
        elif attempts in (3, 4, 5):
            return 15
        elif attempts in (6, 7):
            return 10
        return 0

    def get_player_and_score(
        self, player_attempts, player_guess
    ):  # racuna osvojene poene za jednu rec tj jedan pokusaj
        """
        racuna osvojene poene za jednog igraca na osnovu njegovih pokusaja zadate reci,
        ukoliko je pokusaj tacan, kao rezultat metoda vraca broj poena na osnovu broja pokusaja pozivanjem metode get_score,
        inace kao rezultat vraca nulu
        """
        player_correct = self.get_feedback(player_guess) == ["pogodjenoNaMestu"] * 5
        if player_correct == False:
            return 0
        return self.get_score(player_attempts)


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

    


class UtekniPauku(Igra, RandomSampleMixin):
    TrazenaRec = models.CharField(max_length=20)

    class Meta:
        verbose_name = "UtekniPauku"
        verbose_name_plural = "UtekniPauku"


class Okrsaj(models.Model):
    """\
    Cuva podatke o okrsaju izmedju 2 igraca. Ukupni poeni se racunaju sumiranjem
    poena individuanih odigranih igara tipa `app.OdigranaIgra`
    """

    Igrac1 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")
    Igrac2 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")

    """\
    Metoda za izracunavanje broja poena plavog igraca.
    """

    def blue_player_score(self):
        return (
            OdigranaIgra.objects.filter(Okrsaj=self).aggregate(
                total_sum=Sum("Igrac1Poeni")
            )["total_sum"]
            or 0
        )

    """\
    Metoda za izracunavanje broja poena narandzastog igraca.
    """

    def orange_player_score(self):
        return (
            OdigranaIgra.objects.filter(Okrsaj=self).aggregate(
                total_sum=Sum("Igrac2Poeni")
            )["total_sum"]
            or 0
        )


class OdigranaIgra(models.Model):
    """\
    Cuva podatke o tome koja igra se igrala, u kojoj rundi, za koji okrsaj kao i
    broj osvojenih poena za svakog od igraca.
    """

    Okrsaj = models.ForeignKey(Okrsaj, on_delete=models.RESTRICT)
    Igra = models.ForeignKey(Igra, on_delete=models.RESTRICT)
    RedniBrojIgre = models.IntegerField()  # 1 i 2 su MrezaBrojeva, ...
    Igrac1Poeni = models.IntegerField(null=True)
    Igrac2Poeni = models.IntegerField(null=True)
