from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('home-view')
    return render(request, 'app/index.html')
