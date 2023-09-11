from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import News


# python manage.py create_news "Название новости" "Содержание новости" "Имя автора"

class Command(BaseCommand):
    help = 'Create a new news'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='The title of the news')
        parser.add_argument('content', type=str, help='The content of the news')
        parser.add_argument('author', type=str, help='The username of the author')

    def handle(self, *args, **kwargs):
        title = kwargs['title']
        content = kwargs['content']
        author_username = kwargs['author']

        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username {author_username} does not exist'))
            return

        news = News(title=title, content=content, author=author)
        news.save()

        self.stdout.write(self.style.SUCCESS('News created successfully'))
