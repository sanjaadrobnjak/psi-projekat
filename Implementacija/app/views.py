"""
    Ivan Cancar 2021/0604
"""
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout

def index(request):
    """\
    Pocetna stranica sajta. Omogucava kreiranje novog gost-naloga, logovanje i registraciju.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            logout(request)
            return render(request, 'app/index.html')
        return redirect('home-view')
    return render(request, 'app/index.html')

"""
def games5(request):
    return render(request, 'game5.html')
"""