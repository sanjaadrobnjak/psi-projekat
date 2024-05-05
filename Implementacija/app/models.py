from django.contrib.auth.models import User
from django.db import models

# Create your models here.


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


class Okrsaj(models.Model):
    Igrac1 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")
    Igrac2 = models.ForeignKey(Korisnik, on_delete=models.RESTRICT, related_name="+")


class Igra(models.Model):
    pass


class MrezaBrojeva(Igra):
    TrazeniBroj = models.IntegerField()
    PomocniBroj1 = models.IntegerField()
    PomocniBroj2 = models.IntegerField()
    PomocniBroj3 = models.IntegerField()
    PomocniBroj4 = models.IntegerField()
    PomocniBroj5 = models.IntegerField()
    PomocniBroj6 = models.IntegerField()


class SkokNaMrezu(Igra):
    Postavka = models.TextField()
    Odgovor = models.IntegerField()


class PaukovaSifra(Igra):
    TrazenaRec = models.CharField(max_length=20)


class Umrezavanje(Igra):
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


class UtekniPauku(Igra):
    TrazenaRec = models.CharField(max_length=20)


class OdigranaIgra(models.Model):
    Okrsaj = models.ForeignKey(Okrsaj, on_delete=models.RESTRICT)
    Igra = models.ForeignKey(Igra, on_delete=models.RESTRICT)
    Igrac1Poeni = models.IntegerField()
    Igrac2Poeni = models.IntegerField()
