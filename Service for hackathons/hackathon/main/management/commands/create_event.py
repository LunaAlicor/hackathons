from django.core.management.base import BaseCommand
from main.models import Event


class Command(BaseCommand):
    help = 'Создание события'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('organizer', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('photo', type=str)

    def handle(self, *args, **kwargs):
        event = Event.objects.create(
            title=kwargs['title'],
            description=kwargs['description'],
            date=kwargs['date'],
            location=kwargs['location'],
            organizer=kwargs['organizer'],
            content=kwargs['content'],
            photo=kwargs['photo']
        )
        self.stdout.write(self.style.SUCCESS(f'Создано событие: {event}'))
