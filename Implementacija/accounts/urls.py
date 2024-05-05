from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login-view'),
    path('guest', views.GuestCreateView.as_view(), name='guest-create-view'),
    path('register', views.RegisterView.as_view(), name='register-view'),
    path('home', views.HomeView.as_view(), name='home-view'),
    path('logout', views.LogoutView.as_view(), name='logout-view'),
    path('profile', views.ProfileView.as_view(), name='profile-view'),
]