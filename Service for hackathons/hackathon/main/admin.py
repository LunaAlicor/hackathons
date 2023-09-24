from django.contrib import admin
from .models import News, Event, Comment, Tag, Team

admin.site.register(News)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Team)

# Register your models here.
