# Generated by Django 3.2 on 2023-09-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_news_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, default='image/news_def.jpg', null=True, upload_to='image/%Y'),
        ),
    ]
