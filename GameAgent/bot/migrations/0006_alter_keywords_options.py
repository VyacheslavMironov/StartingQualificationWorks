# Generated by Django 4.0.4 on 2022-05-09 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_keywords_keyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keywords',
            options={'verbose_name': 'Ключевое слово', 'verbose_name_plural': 'Ключевые слова'},
        ),
    ]
