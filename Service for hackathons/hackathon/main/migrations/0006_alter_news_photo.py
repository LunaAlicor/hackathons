# Generated by Django 3.2 on 2023-09-15 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_news_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(default='main/static/main/img/news_photos/news_def.jpg', upload_to='main/static/main/img/news_photos/%Y'),
        ),
    ]
