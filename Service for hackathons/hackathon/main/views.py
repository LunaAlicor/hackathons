from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def events(request):
    return render(request, 'main/events.html')


def login_views(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('index'))
            else:
                error_message = 'Неправильный логин или пароль'
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form, 'error_message': error_message})


def profile(request):
    return render(request, 'main/profile.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)

        user = authenticate(request, username=username, password=password)
        login(request, user)

        return redirect('index')

    return render(request, 'main/register.html')
