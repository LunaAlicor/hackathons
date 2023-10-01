from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewsEditForm, EventForm, TeamForm, EditEventForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import News, Comment, Like, Event, Team
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


# Create your views here.


def index(request):
    news = News.objects.all().order_by('-id')
    comments = Comment.objects.all()
    return render(request, 'main/index.html', {'news': news, 'comments': comments})


def about(request):
    return render(request, 'main/about.html')


def events(request):
    events = Event.objects.all().order_by('-id')
    return render(request, 'main/events.html', {'events': events})


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


def news_detail(request, pk):
    post = News.objects.get(id=pk)
    return render(request, 'main/news_detail.html', {'post': post})


def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    teams = event.teams.all()

    accepted_members = {}
    for team in teams:
        accepted_members[team] = [member for member in team.members.all() if
                                  member.membership_set.get(team=team).status == 'принято']

    accepted_members_len = len(accepted_members)
    return render(request, 'main/event_detail.html', {'event': event, 'accepted_members': accepted_members,
                                                      'accepted_members_len': accepted_members_len})


# @login_required
# def like_news(request, news_id):
#     news = News.objects.get(id=news_id)
#     news.like_count += 1
#     news.save()
#
#     return redirect('news_detail', news_id=news_id)


# @login_required
# def comment_news(request, news_id):
#     news = News.objects.get(id=news_id)
#     user = request.user
#     content = request.POST['content']
#
#     comment = Comment(user=user, news=news, content=content)
#     comment.save()
#
#     return redirect('news_detail', news_id=news.id)


def create_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        photo = request.FILES.get('photo')

        if photo is None:
            photo = 'news_def.jpg'

        try:
            news = News(title=title, content=content, author=author, photo=photo)
            news.save()
        except ValidationError as e:
            pass

        return redirect('index')

    return render(request, 'main/create_news.html')


def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsEditForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=pk)
    else:
        form = NewsEditForm(instance=news)
    return render(request, 'main/edit_news.html', {'form': form})


def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if not request.user.is_staff:
        messages.error(request, "У вас нет прав на удаление новости.")
        return redirect('index')

    if request.method == 'POST':
        news.delete()
        messages.success(request, "Новость успешно удалена.")
        return redirect('index')

    return render(request, 'delete_news.html', {'news': news})


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            return redirect('events')
    else:
        form = EventForm()

    return render(request, 'main/create_event.html', {'form': form})


def create_team(request):
    if request.method == 'POST':
        name = request.POST['name']
        num_members = request.POST['num_members']

        try:
            team = Team(name=name, num_members=num_members)
            team.save()
        except ValidationError as e:
            print(e)
            pass
        return redirect(create_event)

    return render(request, 'main/create_event.html')


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not request.user.is_staff:
        messages.error(request, "У вас нет прав на удаление мероприятия.")
        return redirect('events')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Мероприятие успешно удалено.")
        return redirect('events')

    return render(request, 'delete_event.html', {'event': event})


def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EditEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EditEventForm(instance=event)
    return render(request, 'main/edit_event.html', {'form': form})
