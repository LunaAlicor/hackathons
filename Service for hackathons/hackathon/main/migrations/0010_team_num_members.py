# Generated by Django 3.2 on 2023-09-24 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20230924_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='num_members',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
