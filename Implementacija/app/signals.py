"""
    Ivan Cancar 2021/0604,
    Sanja Drobnjak 2021/0492
    Tanja Kvascev 2021/0031
    Luka Skoko 2021/0497
"""
from .models import MrezaBrojeva
from .models import SkokNaMrezu
from .models import PaukovaSifra
from .models import Umrezavanje
from .models import UtekniPauku
from .models import Okrsaj
from .models import OdigranaIgra
from django.db.models.signals import post_save
from django.dispatch import receiver


"""
    funkcija se pokrece nakon sto se kreira nova instanca modela Okrsaj,
    ako je instanca kreirana, generise se nasumicna kombinacija igara iz 
    razlicitih modela (MrezaBrojeva, SkokNaMrezu i PaukovaSifra), i zatim 
    se kreiraju i cuvaju odgovarajuce instance modela OdigranaIgra koje su 
    povezane sa novim Okrsaj objektom

"""
@receiver(post_save, sender=Okrsaj)
def okrsaj_post_save(sender, instance, created, **kwargs):
    if not created or kwargs['raw']:
        return

    rounds = [
        *MrezaBrojeva.sample(2),
        *SkokNaMrezu.sample(10),
        *PaukovaSifra.sample(2),
        *UtekniPauku.sample(2)
        #*Umrezavanje.sample(2)
    ]
    for i, round in enumerate(rounds, start=1):
        OdigranaIgra(Okrsaj=instance, Igra=round, RedniBrojIgre=i).save()


