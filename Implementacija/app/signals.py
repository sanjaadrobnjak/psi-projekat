from .models import MrezaBrojeva
from .models import SkokNaMrezu
from .models import PaukovaSifra
from .models import Umrezavanje
from .models import Okrsaj
from .models import OdigranaIgra
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Okrsaj)
def okrsaj_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    rounds = [
        *MrezaBrojeva.sample(2),
        *SkokNaMrezu.sample(10),
        *PaukovaSifra.sample(2),
        *Umrezavanje.sample(2)
    ]
    for i, round in enumerate(rounds, start=1):
        OdigranaIgra(Okrsaj=instance, Igra=round, RedniBrojIgre=i).save()

