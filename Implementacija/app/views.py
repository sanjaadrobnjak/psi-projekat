from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login as login_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Korisnik
import random
import string

# Create your views here.

# @login_required
# def home(request):
#     profile = Korisnik.objects.get(pk=request.user)
#     best_players = list(Korisnik.objects.filter(Tip="I").order_by("-BrojTrofeja")[:5].all())
#     return render(request, 'app/home.html', {"user_profile": profile, "best_players": best_players})


# def guest(request):
#     guest_username = "Gost#" + "".join(random.choices(string.ascii_lowercase, k=8))
#     user = User.objects.create_user(username=guest_username, password=None)
#     guest_profile = Korisnik(user=user, Tip="G")
#     user.korisnik = guest_profile
#     print(f"Created guest with username: {guest_profile.user.username}")
#     guest_profile.save()
#     login_user(request, user)
#     return HttpResponseRedirect('home.html')


def index(request):
    return render(request, 'app/index.html')


# def login(request):
#     return render(request, 'app/login.html')


# def register(request):
#     return render(request, 'app/register.html')


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect('index.html')