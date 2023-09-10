from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def events(request):
    return render(request, 'main/events.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            error_massage = 'Неправильный логин или пароль'
    else:
        error_massage = None
    return render(request, 'main/login.html', {'error_message': error_massage})
