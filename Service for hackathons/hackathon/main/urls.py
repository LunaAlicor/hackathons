from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('login', views.login_views, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
]
