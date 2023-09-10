from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('login', views.login, name='login'),
]
