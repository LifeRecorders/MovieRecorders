# Generated by Django 2.2.5 on 2019-11-25 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20191125_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genreType',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
