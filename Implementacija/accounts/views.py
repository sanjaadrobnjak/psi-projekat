"""
    Ivan Cancar 2021/0604
"""
from app.models import Korisnik
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
import random
import string


class LoginView(View):
    """\
    Pogled za logovanje korisnika. Ukoliko su podaci ispravni,
    vrsi se redirekcija na Home stranicu.
    """
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "accounts/login.html",
                {"message": "Pogresno korisnicko ime ili sifra"},
            )
        login(request, user)
        return redirect("home-view")


class GuestCreateView(View):
    """\
    Kreira novi gost-nalog i prebacuje korisnika na Home stranicu.
    """

    def get(self, request):
        username = "Gost#" + "".join(random.choices(string.ascii_lowercase, k=8))
        user = User.objects.create_user(username=username, password=None)
        profile = Korisnik(user=user, Tip="G")
        user.korisnik = profile
        print(f"Created guest with username: {profile.user.username}")
        profile.save()
        login(request, user)
        return redirect("home-view")


class RegisterForm(forms.Form):
    template_name = "accounts/register_form.html"
    firstname = forms.CharField(required=True, label="Ime")
    lastname = forms.CharField(required=True, label="Prezime")
    username = forms.CharField(required=True, label="Korisničko ime")
    password = forms.CharField(
        required=True, min_length=8, label="Lozinka", widget=forms.PasswordInput()
    )
    passwordrepeat = forms.CharField(
        required=True,
        min_length=8,
        label="Potvrdi lozinku",
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordrepeat = cleaned_data.get("passwordrepeat")
        if password != passwordrepeat:
            self.add_error("password", "Lozinke se ne podudaraju")
            self.add_error("passwordrepeat", "Lozinke se ne podudaraju")
            raise ValidationError("Lozinke se ne podudaraju")


class RegisterView(View):
    """\
    Pogled za registraciju novog korisnika. Ukoliko su svi podaci u redu,
    kreira se novi nalog, loguje i prelazi na Home stranicu. 
    """

    def get(self, request):
        return render(request, "accounts/register.html", {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "accounts/register.html", {"form": form}, status=400)
        firstname = form.cleaned_data["firstname"]
        lastname = form.cleaned_data["lastname"]
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            form.add_error("username", "Nalog sa tim korisničkim imenom vec postoji")
            return render(request, "accounts/register.html", {"form": form}, status=400)
        profile = Korisnik(user=user, Tip="I", Ime=firstname, Prezime=lastname)
        try:
            profile.save()
        except Exception as ex:
            user.delete()
            print(ex)
            return render(request, "accounts/register.html", {"form": form}, status=400)
        login(request, user)
        return redirect("home-view")


class HomeView(View):
    """\
    Stranica na kojoj se omogucava igranje okrsaja, pregled profila. Takodje pruza
    mogucnost korisniku da se izloguje.
    """
    @method_decorator(login_required)
    def get(self, request):
        profile = Korisnik.objects.get(pk=request.user)
        best_players = list(
            Korisnik.objects.filter(Tip="I").order_by("-BrojTrofeja")[:5].all()
        )
        return render(
            request,
            "accounts/home.html",
            {"user_profile": profile, "best_players": best_players},
        )


class LogoutView(View):
    """\
    Pozivanjem ovog pogleda, trenutno ulogovani korisnik ce biti izlogovan
    """
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect("index-view")


class ProfileView(View):
    """\
    Pogled za pregled profila trenutno ulogovanog korisnika.
    """
    @method_decorator(login_required)
    def get(self, request):
        profile = Korisnik.objects.get(pk=request.user)
        if profile.BrojPoena < 10:
            title = "Pauk Početnik"
        elif profile.BrojPoena < 25:
            title = "Pauk Pametnica"
        else:
            title = "Pauk Predsednik"
        return render(
            request, "accounts/profile.html", {"profile": profile, "title": title}
        )
