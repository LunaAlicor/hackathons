from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import NewsViewSet, CommentViewSet, LikeViewSet, EventViewSet, TagViewSet, TeamViewSet, MembershipViewSet, \
    TeamApplicationViewSet


router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'events', EventViewSet)
router.register(r'tags', TagViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'teamapplications', TeamApplicationViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('login', views.login_views, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('create_news/', views.create_news, name='create_news'),
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('create_event/', views.create_event, name='create_event'),
    path('create_team/', views.create_team, name='create_team'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('send_application/<int:team_id><int:event_id>/', views.send_application, name='send_application'),
    path('team_application/<int:team_id>', views.team_application, name='team_application'),
    path('approve_application/<int:application_id>/', views.approve_application, name='approve_application'),
    path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    path('create_team_in_edit', views.create_team_in_edit, name='create_team_in_edit'),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='API Documentation')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
