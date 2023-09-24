from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewsEditForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import News, Comment, Like, Event
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
