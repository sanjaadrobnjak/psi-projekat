from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout

def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            logout(request)
            return render(request, 'app/index.html')
        return redirect('home-view')
    return render(request, 'app/index.html')
