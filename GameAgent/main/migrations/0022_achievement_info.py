# Generated by Django 4.0.1 on 2022-05-09 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_aboutuser_passed_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='info',
            field=models.TextField(default='', max_length=200),
        ),
    ]
