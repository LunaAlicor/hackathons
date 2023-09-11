from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Comment, News
from django.contrib.auth.models import User

# python manage.py create_comment 2 1 "Приятного аппетита"


class Command(BaseCommand):
    help = 'Creates a new comment'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User id')
        parser.add_argument('news_id', type=int, help='News id')
        parser.add_argument('content', type=str, help='Comment content')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        news_id = kwargs['news_id']
        content = kwargs['content']

        try:
            user = User.objects.get(id=user_id)
            news = News.objects.get(id=news_id)

            comment = Comment(user=user, news=news, content=content)
            comment.save()

            self.stdout.write(self.style.SUCCESS('Comment created successfully!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with the provided id does not exist!'))
        except News.DoesNotExist:
            self.stdout.write(self.style.ERROR('News with the provided id does not exist!'))
