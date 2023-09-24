from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='image/%Y', default='image/news_def.jpg', null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def has_comments(self):
        return self.comment_set.exists()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True)
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.comment:
            return f"Like by {self.user.username} on comment: {self.comment.content}"
        else:
            return f"Like by {self.user.username} on news: {self.news.title}"


class Event(models.Model):
    STATUS_CHOICES = (
        ('Активно', 'Активно'),
        ('в архиве', 'В архиве'),
        ('регистрация', 'Регистрация'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(upload_to='event_photos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Активно')
    tags = models.ManyToManyField('Tag')
    registration_date = models.DateField(default=timezone.now)
    teams = models.ManyToManyField('Team', blank=True, related_name='events')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, through='Membership')
    num_members = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('ожидание', 'Ожидание'),
        ('принято', 'Принято'),
        ('отклонено', 'Отклонено'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ожидание')

    def __str__(self):
        return f'{self.user.username} - {self.team.name} ({self.status})'


class TeamApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('ожидание', 'Ожидание'),
        ('принято', 'Принято'),
        ('отклонено', 'Отклонено'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ожидание')

    def __str__(self):
        return f'{self.user.username} - {self.team.name} ({self.status})'
