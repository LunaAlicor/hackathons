from django.contrib import admin
from .models import News, Event, Comment, Tag, Team, Membership, TeamApplication

admin.site.register(News)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Team)
admin.site.register(Membership)
admin.site.register(TeamApplication)

# Register your models here.
