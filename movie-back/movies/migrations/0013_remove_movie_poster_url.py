# Generated by Django 2.2.5 on 2019-11-25 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20191125_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster_url',
        ),
    ]
