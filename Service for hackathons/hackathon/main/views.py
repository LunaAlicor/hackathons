from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewsEditForm, EventForm, TeamForm, EditEventForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import News, Comment, Like, Event, Team, TeamApplication, Membership, Tag
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets, status
from .serializers import NewsSerializer, CommentSerializer, LikeSerializer, EventSerializer, TagSerializer, TeamSerializer, MembershipSerializer, TeamApplicationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.


def index(request):
    news = News.objects.all().order_by('-id')
    comments = Comment.objects.all()
    return render(request, 'main/index.html', {'news': news, 'comments': comments})


def about(request):
    return render(request, 'main/about.html')


def events(request):
    events = Event.objects.all().order_by('-id')
    now = timezone.localdate()
    for event in events:
        if now < event.registration_date:
            event.status = 'Активно'
            event.save()
        elif event.registration_date <= now < event.date:
            event.status = 'регистрация'
            event.save()
        elif now > event.date:
            event.status = 'Архив'
            event.save()

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

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'main/register.html')

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

    free_spots = {}
    for team in teams:
        num_members = team.num_members
        accepted_count = len(accepted_members[team])
        free_spots[team] = range(num_members - accepted_count)

    accepted_members_len = len(accepted_members)
    return render(request, 'main/event_detail.html', {'event': event, 'accepted_members': accepted_members,
                                                      'accepted_members_len': accepted_members_len,
                                                      'free_spots': free_spots})


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


def create_team_in_edit(request):
    if request.method == 'POST':
        name = request.POST['name']
        num_members = request.POST['num_members']

        try:
            team = Team(name=name, num_members=num_members)
            team.save()
        except ValidationError as e:
            print(e)
            pass

        return redirect(request.META.get('HTTP_REFERER', '/default-url/'))

    return render(request, 'main/events.html')


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


def send_application(request, team_id, event_id):
    if request.method == 'POST':
        user = request.user
        team = Team.objects.get(pk=team_id)

        if team.members.filter(pk=user.id).exists() or team.members.count() >= team.num_members:
            pass
        else:
            application, created = TeamApplication.objects.get_or_create(user=user, team=team)

        try:
            event = Event.objects.get(pk=event_id)
            return redirect(reverse('event_detail', kwargs={'pk': event.id}))
        except AttributeError:
            pass

    return redirect('events')


def team_application(request, team_id):
    team = Team.objects.get(pk=team_id)
    team_applications = TeamApplication.objects.filter(team_id=team_id)

    return render(request, 'main/team_application.html', {'team_applications': team_applications, 'team': team})


def approve_application(request, application_id):
    application = get_object_or_404(TeamApplication, pk=application_id)
    application.status = 'принято'
    application.save()
    membership, created = Membership.objects.get_or_create(user=application.user, team=application.team)
    membership.status = 'принято'
    membership.save()

    return redirect('team_application', team_id=application.team.id)


def reject_application(request, application_id):
    application = get_object_or_404(TeamApplication, pk=application_id)
    application.status = 'отклонено'
    application.save()
    membership, created = Membership.objects.get_or_create(user=application.user, team=application.team)
    membership.status = 'отклонено'
    membership.save()

    return redirect('team_application', team_id=application.team.id)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class TeamApplicationViewSet(viewsets.ModelViewSet):
    queryset = TeamApplication.objects.all()
    serializer_class = TeamApplicationSerializer





@csrf_exempt
def like_news(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        like, created = Like.objects.get_or_create(user=request.user, news=news)

        if not created:
            # Пользователь уже поставил лайк, уберите его
            like.delete()
        else:
            # Увеличьте счетчик лайков
            news.like_count += 1
            news.save()

        return JsonResponse({'message': 'Liked successfully'})
    except News.DoesNotExist:
        return JsonResponse({'message': 'News not found'})


@csrf_exempt
def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        like, created = Like.objects.get_or_create(user=request.user, comment=comment)

        if not created:
            # Пользователь уже поставил лайк, уберите его
            like.delete()
        else:
            # Увеличьте счетчик лайков для комментария в базе данных
            comment.like_count += 1
            comment.save()

        return JsonResponse({'message': 'Liked successfully'})
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'Comment not found'})


@api_view(['POST'])
def leave_comment(request, news_id):
    if request.method == 'POST':
        content = request.data.get('content')  # Изменим на request.data
        user = request.user
        news = News.objects.get(id=news_id)
        like_count = 0
        comment = Comment.objects.create(user=user, news=news, content=content, like_count=like_count)
        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
    return redirect('index')


def del_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not request.user.is_staff:
        return JsonResponse({"success": False, "message": "У вас недостаточно прав для удаления чужого комментария!"})

    if request.method == "POST":
        comment.delete()
        return JsonResponse({"success": True, "message": "Комментарий удален!"})

    return JsonResponse({"success": False, "message": "Недопустимый метод запроса"})
